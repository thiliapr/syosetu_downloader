"下载 Syosetu 小说。"
# 本文件是 syosetu_downloader 的一部分
# SPDX-FileCopyrightText: 2025 thiliapr <thiliapr@tutanota.com>
# SPDX-FileContributor: thiliapr <thiliapr@tutanota.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

import pathlib
import argparse
import requests
import tqdm
from typing import Optional
from bs4 import BeautifulSoup


def fetch(url: str, proxy: Optional[str] = None) -> BeautifulSoup:
    """
    请求页面内容并返回解析后的BeautifulSoup对象

    Args:
        url: 要访问的页面
        proxy: 代理
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }
    proxies = {"https": proxy} if proxy else {}

    response = requests.get(url, proxies=proxies, headers=headers)
    response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
    return BeautifulSoup(response.content, "html.parser")


def fetch_chapters_list(url: str, proxy: Optional[str] = None) -> tuple[list[tuple[str, str]], Optional[str]]:
    """
    获取指定小说页的章节列表

    Args:
        url: 目录的URL
        proxy: 代理

    Returns:
        章节的标题和链接的列表、下一页的URL
    """
    soup = fetch(url, proxy)

    # 获取章节列表
    chapters = []
    for sublist in soup.select(".p-eplist__sublist"):
        subtitle = sublist.select_one(".p-eplist__subtitle")
        chapters.append((subtitle.text.strip(), "https://ncode.syosetu.com" + subtitle.get("href")))

    # 下一页的URL获取
    href = soup.select_one(".c-pager__item--next").get("href")
    next_page_url = "https://ncode.syosetu.com" + href if href else None

    return chapters, next_page_url


def fetch_chapter_content(chapter_url: str, proxy: Optional[str] = None):
    "获取单个章节的内容"
    soup = fetch(chapter_url, proxy)
    document = soup.select_one(".p-novel__text")
    paragraphs = [p.text.strip() for p in document.select("p")]
    return "\n".join(paragraphs)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="下载小说的章节内容")
    parser.add_argument("novelid", help="小说的ID, 例如: n2267be")
    parser.add_argument("-p", "--proxy", help="设置代理, 例如: socks5h://127.0.0.1:7890")
    parser.add_argument("-n", "--novel-dir", default=pathlib.Path("downloads"), help="将小说保存到哪个位置。如果没有，默认使用`downloads`目录")
    args = parser.parse_args()

    # 获取标题
    print(fetch(f"https://ncode.syosetu.com/{args.novelid}", args.proxy).select_one(".p-novel__title").text.strip())

    # 存储章节
    all_chapters: list[str, str] = []

    # 获取小说所有章节
    progress_bar = tqdm.tqdm(desc="检索章节列表", unit="页")
    next_page_url = f"https://ncode.syosetu.com/{args.novelid}"

    while True:
        chapters, next_page_url = fetch_chapters_list(next_page_url, args.proxy)
        all_chapters.extend(chapters)

        # 如果没有下一页，停止
        if next_page_url is None:
            break

        progress_bar.update()
    progress_bar.close()

    # 将所有章节下载并保存到文件中
    args.novel_dir.mkdir(parents=True, exist_ok=True)

    # 滤除已经下载的章节
    all_chapters = [(title, url) for title, url in all_chapters if not (args.novel_dir / (title + ".txt")).exists()]

    # 下载章节内容
    for title, url in tqdm.tqdm(all_chapters, desc="下载并保存章节",):
        chapter_file = args.novel_dir / (title.replace("/", "_").replace('"', "_") + ".txt")

        try:
            content = fetch_chapter_content(url, proxy=args.proxy)
        except Exception as e:
            print(f"跳过对章节 {title} 的获取: {e}")
            continue

        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    main()
