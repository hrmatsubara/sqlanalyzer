"""
strproc.py
文字列処理関連の関数を定義するモジュール
"""

import re


def whitespace2space(s: str) -> str:
    """
    文字列中の空白文字をスペースに変換する
    正規表現パターンをコンパイル(\sが)し、sub()メソッドで置換
    Args:
        s (str): 置換対象の文字列
    Returns:
        str: 置換後の文字列
    """
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    return _RE_COMBINE_WHITESPACE.sub(" ", s)


def is_empty(s: str) -> bool:
    """
    文字列が空文字列かどうかを判定する
    strip()により改行\nや全角スペース\u3000やタブ\tなどが空白文字として除去される
    Args:
        s (str): 判定対象の文字列
    Returns:
        bool: 空文字列の場合はTrue、それ以外はFalse
    """
    return not s.strip()
