import os
import asyncio
import aiohttp
import requests
from aiofiles import open as aio_open

class M3U8Downloader:
    def __init__(self, m3u8_url, save_dir, retry_limit=3, max_connections=10):
        self.m3u8_url = m3u8_url
        self.save_dir = save_dir
        self.base_url = os.path.dirname(m3u8_url)
        self.retry_limit = retry_limit
        self.max_connections = max_connections

    def fetch_m3u8(self):
        """同步请求获取 m3u8 文件内容"""
        response = requests.get(self.m3u8_url,headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_m3u8(self, content):
        """解析 m3u8 文件，提取 ts 文件的链接"""
        ts_urls = []
        for line in content.splitlines():
            if line and not line.startswith("#"):
                ts_url = line if line.startswith("http") else f"{self.base_url}/{line}"
                ts_urls.append(ts_url)
        return ts_urls

    async def download_ts(self, session, ts_url, save_path):
        """异步下载单个 ts 文件，支持断点续传和重试"""
        retries = 0
        while retries < self.retry_limit:
            try:
                # 检查是否已部分下载
                headers = {}
                if os.path.exists(save_path):
                    file_size = os.path.getsize(save_path)
                    headers['Range'] = f"bytes={file_size}-"
                    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

                async with session.get(ts_url, headers=headers) as response:
                    response.raise_for_status()
                    mode = "ab" if 'Range' in headers else "wb"  # 追加写入或覆盖写入
                    async with aio_open(save_path, mode) as f:
                        async for chunk in response.content.iter_chunked(1024):
                            await f.write(chunk)
                print(f"Downloaded: {os.path.basename(save_path)}")
                return  # 下载成功后退出循环
            except Exception as e:
                retries += 1
                print(f"Retry {retries}/{self.retry_limit} for {ts_url}: {e}")
        print(f"Failed to download {ts_url} after {self.retry_limit} retries")

    async def download_all(self, ts_urls):
        """异步下载所有 ts 文件，使用信号量控制并发"""
        os.makedirs(self.save_dir, exist_ok=True)
        semaphore = asyncio.Semaphore(self.max_connections)
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.download_with_semaphore(semaphore, session, ts_url, os.path.join(self.save_dir, f"{i}.ts"))
                for i, ts_url in enumerate(ts_urls)
            ]
            await asyncio.gather(*tasks)

    async def download_with_semaphore(self, semaphore, session, ts_url, save_path):
        """通过信号量限制并发下载"""
        async with semaphore:
            await self.download_ts(session, ts_url, save_path)

    def merge_ts(self):
        """合并 ts 文件为一个 mp4 文件"""
        output_path = os.path.join(self.save_dir, "00output.mp4")
        ts_files = [os.path.join(self.save_dir, f) for f in os.listdir(self.save_dir) if f.endswith(".ts")]
        ts_files.sort(key=lambda x: int(os.path.basename(x).split(".")[0]))  # 按文件名排序
        with open(output_path, "wb") as merged:
            for ts_file in ts_files:
                with open(ts_file, "rb") as ts:
                    merged.write(ts.read())
        print(f"Merged video saved to: {output_path}")

    def run(self):
        """主流程"""
        # 获取和解析 m3u8 文件
        print("Fetching m3u8 content...")
        content = self.fetch_m3u8()
        ts_urls = self.parse_m3u8(content)
        print(f"Found {len(ts_urls)} ts files.")

        # 异步下载 ts 文件
        print("Downloading ts files...")
        asyncio.run(self.download_all(ts_urls))

        # 合并 ts 文件
        print("Merging ts files...")
        self.merge_ts()
        print("Download and merge completed!")


if __name__ == "__main__":
    # m3u8_url = input("Enter the m3u8 URL: ").strip()
    # save_dir = input("Enter the directory to save files: ").strip()
    m3u8_url = 'https://s8-e1.pipecdn.vip/ppot/_definst_/mp4:s16/gvod/lxj-yyyxd2j-04-011FB110D.mp4/chunklist.m3u8?vendtime=1735902014&vhash=BIPRTwv7RBVWDEEEp3itIJ623rikEudtuo9K5Ji0Uys=&vCustomParameter=0_61.221.110.227_TW_0_0&lb=83d6cacef313f2ddde76a894a612a0f9'
    save_dir = 'output'
    downloader = M3U8Downloader(m3u8_url, save_dir)
    downloader.run()
