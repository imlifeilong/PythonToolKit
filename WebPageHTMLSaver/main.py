import os
import re
import requests
import mimetypes
import hashlib
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


class WebPageSaver:
    def __init__(self, url, output_dir="saved_webpage", max_workers=10):
        self.url = url
        self.base_url = url
        self.output_dir = output_dir
        self.resource_dir = os.path.join(output_dir, "resources")
        self.visited_urls = set()
        self.resource_map = {}
        self.max_workers = max_workers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.resource_dir, exist_ok=True)

        # 初始化MIME类型
        mimetypes.init()

    def sanitize_filename(self, url):
        """创建安全的文件名"""
        # 提取URL中的文件名部分
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)

        # 如果没有文件名，使用默认名称
        if not filename or '.' not in filename:
            filename = "resource"

        # 移除非法字符
        filename = re.sub(r'[\\/*?:"<>|]', "_", filename)

        # 如果文件名太长，截断并添加哈希
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            name_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"{name[:70]}_{name_hash}{ext}"

        return filename

    def get_extension_from_content_type(self, content_type):
        """根据Content-Type获取文件扩展名"""
        if not content_type:
            return ""

        # 获取可能的扩展名列表
        extensions = mimetypes.guess_all_extensions(content_type.split(';')[0].strip())
        return extensions[0] if extensions else ""

    def download_resource(self, url, referer=None):
        """下载单个资源"""
        if url in self.visited_urls:
            return None

        self.visited_urls.add(url)

        try:
            headers = self.headers.copy()
            if referer:
                headers["Referer"] = referer

            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            # 确定文件扩展名
            content_type = response.headers.get('Content-Type', '')
            filename = self.sanitize_filename(url)

            # 如果没有扩展名或扩展名不正确，尝试从Content-Type获取
            if '.' not in filename or not filename.split('.')[-1]:
                ext = self.get_extension_from_content_type(content_type)
                if ext:
                    filename += ext

            # 创建唯一文件名
            file_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{file_hash}{ext}" if name else f"resource_{file_hash}{ext}"
            save_path = os.path.join(self.resource_dir, unique_filename)

            # 保存文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"下载资源: {url} -> {save_path}")
            return (url, save_path, content_type)

        except Exception as e:
            print(f"下载失败: {url} - {str(e)}")
            return None

    def parse_and_download(self, html_content, base_url):
        """解析HTML并下载所有资源"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # 需要处理的资源标签
        resource_tags = [
            ('link', 'href', ['stylesheet', 'icon', 'preload']),
            ('script', 'src', []),
            ('img', 'src', []),
            ('img', 'srcset', []),
            ('source', 'src', []),
            ('source', 'srcset', []),
            ('video', 'src', []),
            ('audio', 'src', []),
            ('object', 'data', []),
            ('embed', 'src', []),
            ('iframe', 'src', []),
            ('meta', 'content', ['og:image', 'twitter:image'])
        ]

        # 收集所有资源URL
        resource_urls = []

        for tag, attr, filters in resource_tags:
            for element in soup.find_all(tag):
                if tag == 'link' and filters:
                    rel = element.get('rel', [])
                    if not any(r in rel for r in filters):
                        continue

                if tag == 'meta' and filters:
                    property_val = element.get('property', '') or element.get('name', '')
                    if property_val.lower() not in filters:
                        continue

                # 处理srcset属性（包含多个URL）
                if attr == 'srcset':
                    srcset = element.get(attr, '')
                    if not srcset:
                        continue

                    # 解析srcset格式：url1 1x, url2 2x
                    for part in srcset.split(','):
                        part = part.strip()
                        if not part:
                            continue

                        # 提取URL（忽略描述符）
                        url_part = part.split()[0]
                        full_url = urljoin(base_url, url_part)
                        if full_url not in self.visited_urls:
                            resource_urls.append((full_url, base_url))

                # 处理其他属性
                else:
                    url = element.get(attr)
                    if not url:
                        continue

                    # 跳过data URL和内联资源
                    if url.startswith(('data:', 'javascript:', 'mailto:', 'tel:')):
                        continue

                    full_url = urljoin(base_url, url)
                    if full_url not in self.visited_urls:
                        resource_urls.append((full_url, base_url))

        # 并行下载所有资源
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for url, referer in resource_urls:
                futures.append(executor.submit(self.download_resource, url, referer))

            for future in as_completed(futures):
                result = future.result()
                if result:
                    url, save_path, content_type = result
                    # 保存映射关系
                    self.resource_map[url] = os.path.relpath(save_path, self.output_dir).replace('\\', '/')

                    # 如果是CSS文件，需要解析其内容
                    if content_type and 'text/css' in content_type:
                        self.process_css_file(save_path, base_url)

        # 更新HTML中的资源引用
        for tag, attr, filters in resource_tags:
            for element in soup.find_all(tag):
                if tag == 'link' and filters:
                    rel = element.get('rel', [])
                    if not any(r in rel for r in filters):
                        continue

                if tag == 'meta' and filters:
                    property_val = element.get('property', '') or element.get('name', '')
                    if property_val.lower() not in filters:
                        continue

                # 处理srcset属性
                if attr == 'srcset':
                    srcset = element.get(attr, '')
                    if not srcset:
                        continue

                    new_srcset = []
                    for part in srcset.split(','):
                        part = part.strip()
                        if not part:
                            continue

                        # 提取URL（忽略描述符）
                        url_part = part.split()[0]
                        full_url = urljoin(base_url, url_part)

                        if full_url in self.resource_map:
                            new_url = self.resource_map[full_url]
                            new_srcset.append(f"{new_url} {part.split()[1]}")
                        else:
                            new_srcset.append(part)

                    element[attr] = ', '.join(new_srcset)

                # 处理其他属性
                else:
                    url = element.get(attr)
                    if not url:
                        continue

                    # 跳过data URL和内联资源
                    if url.startswith(('data:', 'javascript:', 'mailto:', 'tel:')):
                        continue

                    full_url = urljoin(base_url, url)
                    if full_url in self.resource_map:
                        element[attr] = self.resource_map[full_url]

        # 处理内联样式
        for style in soup.find_all('style'):
            if style.string:
                new_css = self.process_css_content(style.string, base_url)
                style.string = new_css

        return str(soup)

    def process_css_file(self, css_path, base_url):
        """处理CSS文件中的资源"""
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()

            new_css = self.process_css_content(css_content, base_url)

            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(new_css)
        except Exception as e:
            print(f"处理CSS文件失败: {css_path} - {str(e)}")

    def process_css_content(self, css_content, base_url):
        """处理CSS内容中的url()引用"""
        pattern = r"url\(['\"]?(.*?)['\"]?\)"

        def replace_url(match):
            url = match.group(1).strip()

            # 跳过data URL
            if url.startswith('data:'):
                return match.group(0)

            # 处理相对URL
            full_url = urljoin(base_url, url)

            # 如果已经下载过该资源
            if full_url in self.resource_map:
                return f"url('{self.resource_map[full_url]}')"

            # 如果尚未下载，尝试下载
            result = self.download_resource(full_url, base_url)
            if result:
                resource_url, save_path, _ = result
                relative_path = os.path.relpath(save_path, self.output_dir).replace('\\', '/')
                self.resource_map[resource_url] = relative_path
                return f"url('{relative_path}')"

            return match.group(0)

        return re.sub(pattern, replace_url, css_content)

    def save(self):
        """保存整个网页"""
        try:
            print(f"开始下载网页: {self.url}")

            # 下载主HTML
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            # 更新基础URL（处理重定向）
            self.base_url = response.url

            # 处理网页内容
            html_content = response.text
            processed_html = self.parse_and_download(html_content, self.base_url)

            # 保存主HTML文件
            main_filename = "index.html"
            main_filepath = os.path.join(self.output_dir, main_filename)
            with open(main_filepath, 'w', encoding='utf-8') as f:
                f.write(processed_html)

            print(f"网页保存成功: {main_filepath}")
            print(f"资源保存在: {self.resource_dir}")
            print(f"总计下载资源: {len(self.resource_map)}个")

            return main_filepath

        except Exception as e:
            print(f"保存网页失败: {str(e)}")
            return None


if __name__ == "__main__":
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="网页保存工具 - 模拟浏览器'另存为'功能")
    # parser.add_argument("url", help="要保存的网页URL")
    # parser.add_argument("-o", "--output", default="saved_webpage",
    #                     help="输出目录 (默认: saved_webpage)")
    # parser.add_argument("-t", "--threads", type=int, default=10,
    #                     help="并发下载线程数 (默认: 10)")
    #
    # args = parser.parse_args()
    #
    # print(f"开始保存网页: {args.url}")
    # print(f"输出目录: {args.output}")
    # print(f"并发线程: {args.threads}")
    # print("-" * 50)
    url = 'https://www.sohu.com/a/917955713_115239?edtsign=017EEB1AC6C0BBEBB4C64E33034A953C3B272E0F&edtcode=urgGg3lvqugR8UK%2BHjigtw%3D%3D&scm=thor.280_14-200000.0.0.&spm=smpc.home.top-news2.8.17535920499339FEPs8P_1467'
    saver = WebPageSaver(url)
    saver.save()

    # print("-" * 50)
    # print("操作完成！在浏览器中打开 index.html 查看保存的网页")