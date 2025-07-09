"翻译转 TXT 转换脚本"

# 本文件是 syosetu_downloader 的一部分
# SPDX-FileCopyrightText: 2025 thiliapr <thiliapr@tutanota.com>
# SPDX-FileContributor: thiliapr <thiliapr@tutanota.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

import pathlib
import orjson
import argparse
from tqdm import tqdm


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将翻译变成txt格式。")
    parser.add_argument("-n", "--novel-dir", default=pathlib.Path("downloads"), help="小说目录，包含章节文件，默认为 %(default)s")
    parser.add_argument("-t", "--translated-dir", default=pathlib.Path("translated"), help="翻译目录，包含章节翻译文件，默认为 %(default)s")
    parser.add_argument("-r", "--result-dir", default=pathlib.Path("results"), help="结果目录，生成的章节文件将存放在此目录，默认为 %(default)s")
    args = parser.parse_args()

    # 确保目录存在
    args.result_dir.mkdir(parents=True, exist_ok=True)

    # 获取已经翻译的章节和已经生成结果的章节，避免重复处理
    translated_chapters = {file.stem for file in args.translated_dir.glob("*.json")}
    result_chapters = {file.stem for file in args.result_dir.glob("*.txt")}

    # 处理每个章节文件（如果已经翻译过且结果未生成）
    for chapter_file in tqdm([file for file in args.novel_dir.glob("*.txt") if file.stem not in result_chapters]):
        # 如果章节没有翻译文件，则跳过
        if chapter_file.stem not in translated_chapters:
            print("skip:", chapter_file.stem)
            continue

        # 读取原章节内容和翻译内容，并生成结果文件
        with open(chapter_file, encoding="utf-8") as orignal, open(args.translated_dir / (chapter_file.stem + ".json"), encoding="utf-8") as translated, open(args.result_dir / chapter_file.name, "w", encoding="utf-8") as result:
            # 读取原章节内容
            content = orignal.read()

            # 使用 orjson 解析翻译内容
            for msg in orjson.load(translated):
                # 如果翻译消息中有 "target"，则替换原内容中的 "source" 为 "target"
                if "target" in msg:
                    content = content.replace(msg["source"], msg["target"])

            # 写入结果文件
            result.write(content)


if __name__ == "__main__":
    main()
