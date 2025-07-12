"TXT 导出为待翻译任务。"
# 本文件是 syosetu_downloader 的一部分
# SPDX-FileCopyrightText: 2025 thiliapr <thiliapr@tutanota.com>
# SPDX-FileContributor: thiliapr <thiliapr@tutanota.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

import pathlib
import orjson
import argparse
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description="将小说内容导出为待翻译任务的格式（tktransl格式）。")
    parser.add_argument("-n", "--novel-dir", default=pathlib.Path("downloads"), help="小说目录，包含章节文件，默认为 %(default)s")
    parser.add_argument("-t", "--translated-dir", default=pathlib.Path("translated"), help="翻译目录，包含章节翻译文件，默认为 %(default)s")
    parser.add_argument("-k", "--task-dir", default=pathlib.Path("tasks"), help="任务目录，生成的待翻译任务章节文件将存放在此目录，默认为 %(default)s")
    args = parser.parse_args()

    # 确保目录存在
    args.task_dir.mkdir(parents=True, exist_ok=True)

    # 获取已经翻译的章节，避免重复处理
    translated_chapters = set()
    if args.translated_dir.is_dir():
        translated_chapters = {file.stem for file in args.translated_dir.glob("*.json")}

    # 处理每个章节文件（如果未翻译过）
    for chapter_file in tqdm([file for file in args.novel_dir.glob("*.txt") if file.stem not in translated_chapters]):
        with open(chapter_file, encoding="utf-8") as rfile, open(args.task_dir / (chapter_file.stem + ".json"), "wb") as wfile:
            # 读取原章节内容并转换为待翻译任务格式
            wfile.write(orjson.dumps([
                {"source": line}  # 将每行文本转换为待翻译任务格式
                for line in rfile
                if line  # 过滤掉空行
            ]))


if __name__ == "__main__":
    main()
