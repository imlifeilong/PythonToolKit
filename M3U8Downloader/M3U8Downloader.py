import os
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor


class M3U8Downloader:
    def __init__(self, m3u8_url, save_dir):
        self.m3u8_url = m3u8_url
        self.save_dir = save_dir
        self.base_url = os.path.dirname(m3u8_url)

    def fetch_m3u8(self):
        """同步请求获取 m3u8 文件内容"""
        response = requests.get(self.m3u8_url, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
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
        """异步下载单个 ts 文件"""
        try:
            async with session.get(ts_url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }) as response:
                response.raise_for_status()
                with open(save_path, "wb") as f:
                    while chunk := await response.content.read(1024):
                        f.write(chunk)
            print(f"Downloaded: {os.path.basename(save_path)}")
        except Exception as e:
            print(f"Failed to download {ts_url}: {e}")

    async def download_all(self, ts_urls):
        """异步下载所有 ts 文件"""
        os.makedirs(self.save_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.download_ts(session, ts_url, os.path.join(self.save_dir, f"{i}.ts"))
                for i, ts_url in enumerate(ts_urls)
            ]
            await asyncio.gather(*tasks)

    def merge_ts(self):
        """合并 ts 文件为一个 mp4 文件"""
        output_path = os.path.join(self.save_dir, "output.mp4")
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

    m3u8_url = 'https://s8-e1.pipecdn.vip/ppot/_definst_/mp4:s16/gvod/lxj-yyyxd2j-02-0289FD94B.mp4/chunklist.m3u8?vendtime=1735901402&vhash=khWbJxibzau89gW0cKtU2LiijCncXXlDXhXOHeqOgFI=&vCustomParameter=0_61.221.110.227_TW_0_0&lb=acbeffe4699d4f777dfce6a1ba02d5d1'
    save_dir = 'output'
    downloader = M3U8Downloader(m3u8_url, save_dir)
    downloader.run()
