"""ファイル出力
"""


def strlist2file(strlist, filepath):
    """文字列リストをファイルに書き込む"""
    with open(filepath, "w") as f:
        for num, block in enumerate(strlist):
            f.write(f"===({num})============================\n")
            f.write(block)
            f.write("==\n")
