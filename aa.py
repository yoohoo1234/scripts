#!/usr/bin/env python3
# srt_join_lines.py
# 功能：将 SRT 字幕同一时间轴内的多行文本合并为一行
# 用法：
#   python srt_join_lines.py input.srt             -> 生成 output.srt
#   python srt_join_lines.py input.srt custom.srt  -> 生成 custom.srt

import argparse
import sys
import os

def join_srt_lines(text: str) -> str:
    # 移除 BOM 头，统一换行符
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    out = []
    i = 0
    n = len(lines)

    while i < n:
        # 1. 跳过块与块之间的空行
        while i < n and lines[i].strip() == "":
            i += 1
        if i >= n:
            break

        # 2. 读取序号 (Index)
        idx = lines[i].rstrip()
        i += 1
        if i >= n:
            out.append(idx)
            break

        # 3. 读取时间轴 (Timestamp)
        timeline = lines[i].rstrip()
        i += 1

        # 4. 读取并合并字幕文本 (Text)
        # 收集该块内的所有非空文本行
        text_lines = []
        while i < n and lines[i].strip() != "":
            text_lines.append(lines[i].strip())
            i += 1

        # 用空格连接多行文本
        joined_text = " ".join([s for s in text_lines if s])

        # 写入新块结构：序号 -> 时间轴 -> 合并后的文本 -> 空行
        out.extend([idx, timeline, joined_text, ""])

    # 确保文件以换行结束，且不留多余空行
    return "\n".join(out).rstrip("\n") + "\n"

def main():
    parser = argparse.ArgumentParser(description="Join multi-line subtitle text into one line per timestamp.")

    # input 是必须参数
    parser.add_argument("input", help="Path to input .srt file")

    # output 是可选参数 (nargs='?')，默认值为 'output.srt'
    parser.add_argument("output", nargs="?", default="output.srt",
                        help="Path to output .srt file (default: output.srt)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = join_srt_lines(content)

        with open(args.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)

        print(f"Success: '{args.input}' -> '{args.output}'")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
