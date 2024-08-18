import re
from commonlibs.str.manipulation import whitespace2space

_SQL_START_WORDS = ["SELECT", "INSERT", "UPDATE", "DELETE", "WITH"]
_SQL_SELECT_STATEMENT_WORDS = ["SELECT", "INSERT", "UPDATE", "DELETE", "WITH"]
_SQL_END_OF_STATEMENT = [";", "GO"]


def is_blankline(line: str) -> bool:
    """
    文字列が空行かどうかを判定する
    空行の特徴は、空白文字のみまたは改行文字のみで構成されること
    ※str.strip()で改行文字や全角スペース、タブ文字などが空白文字として除去される
    Args:
        s (str): 判定対象の文字列
    Returns:
        bool: 空行の場合はTrue、それ以外はFalse
    """
    return not bool(line.strip())


# def is_sql_statement(line: str) -> bool:
#     """
#     文字列がSQL文かどうかを判定する
#     SQL文の特徴は、最初のキーワードがSELECT, INSERT, UPDATE, DELETE, WITHのいずれかであること
#     Args:
#         s (str): 判定対象の文字列
#     Returns:
#         bool: SQL文の場合はTrue、それ以外はFalse
#     """
#     _RE_SQL_KEYWORD = re.compile(r"^\s*(" + "|".join(_SQL_START_WORDS) + ")", re.I)
#     return bool(_RE_SQL_KEYWORD.match(line.strip()))


def is_sql_commentline(line: str) -> bool:
    """
    文字列がSQLコメントかどうかを判定する
    SQLコメントの特徴は、最初のキーワードが--であること
    Args:
        s (str): 判定対象の文字列
    Returns:
        bool: SQLコメントの場合はTrue、それ以外はFalse
    """
    _RE_SQL_COMMENT = re.compile(r"^\s*--")
    return bool(_RE_SQL_COMMENT.match(line.strip()))


def is_end_of_sql_statement(line: str) -> bool:
    """
    文字列がSQL文の終了かどうかを判定する
    SQL文の終了の特徴は、最初のキーワードが;またはGOであること
    Args:
        s (str): 判定対象の文字列
    Returns:
        bool: SQL文の終了の場合はTrue、それ以外はFalse
    """
    _RE_SQL_END = re.compile(r"(" + "|".join(_SQL_END_OF_STATEMENT) + ")\s*$", re.I)
    return bool(_RE_SQL_END.search(line.strip()))


def is_top_of_sql_codeblock(old_line: str, new_line: str) -> bool:
    """
    sqlコードブロックの新たな開始行かどうかを判定する
    コメント行からコメントではない行のとき、true
    それ以外はfalse
    """
    if is_sql_commentline(old_line) and not is_sql_commentline(new_line):
        return True
    return False


def is_in_sql_codeblock(previous_line: str, new_line: str) -> bool:
    """
    sqlのコードブロックかどうかを判定する
    コードブロック開始行からコードブロック終了行までの行かどうかを判定する
    """
    if not is_sql_commentline(previous_line) and not is_sql_commentline(new_line):
        return True
    return False


def is_out_of_sql_codeblock(old_line: str, new_line: str) -> bool:
    """
    sqlのコードブロックから抜けたかどうかを判定する
    コメントではない行からコメント行のとき、true
    それ以外はfalse
    """
    if not is_sql_commentline(old_line) and is_sql_commentline(new_line):
        return True
    return False


def is_in_sql_commentblock(previous_line: str, new_line: str) -> bool:
    """
    sqlのコードブロックかどうかを判定する
    コードブロック開始行からコードブロック終了行までの行かどうかを判定する
    """
    if is_sql_commentline(previous_line) and is_sql_commentline(new_line):
        return True
    return False


def file2sqlcodeblocks(filepath: str) -> list[str]:
    """
    ファイルからSQLコードブロックを抽出する
    ファイルを読み込み、コメント毎にSQL文を抽出する
    Args:
        filepath (str): ファイルパス
    Returns:
        list[str]: SQLコードブロックのリスト
    """
    blocks = []
    cnt_block = 0

    file = open(filepath, "r", encoding="utf-8-sig")
    lines = file.readlines()

    sqlcodeblock = ""
    old_line = "-- "  # ひとつ前の行（--なのは最初の行がコードブロックの場合にコードブロックtopと認識させるため）

    for line_num, line in enumerate(lines):

        # 空行はスキップ
        if is_blankline(line):
            continue

        # コードブロック開始
        elif is_top_of_sql_codeblock(old_line, line):
            sqlcodeblock = line
            cnt_block += 1
            if is_end_of_sql_statement(line):  # 明示的なコードブロック終了
                blocks.append(sqlcodeblock)
                old_line = f"-- {line_num}"  # コードブロック終了後は初期状態に戻す
                sqlcodeblock = ""
                continue

        # コードブロック中 ※flg_sql_codeblockは前の行がコードブロックかどうかを示すフラグ
        elif is_in_sql_codeblock(old_line, line):
            if is_end_of_sql_statement(line):  # 明示的なコードブロック終了
                blocks.append(sqlcodeblock)
                old_line = f"-- {line_num}"  # コードブロック終了後は初期状態に戻す
                sqlcodeblock = ""
                continue
            else:
                sqlcodeblock = sqlcodeblock + line

        # コードブロック終了(コメント行)
        elif is_out_of_sql_codeblock(old_line, line):
            blocks.append(sqlcodeblock)
            print(f"{line_num}: コメントブロック")
            old_line = f"-- {line_num}"
            sqlcodeblock = ""
            continue

        # コメント行
        elif is_in_sql_commentblock(old_line, line):
            print(f"{line_num}: コメントブロック")

        else:
            raise ValueError(f"不正な行です: {line_num+1}行目")

        #
        old_line = line

    # 最後のコードブロックを追加
    if sqlcodeblock != "":
        blocks.append(sqlcodeblock)

    return blocks
