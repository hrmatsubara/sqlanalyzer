import os
from sqlanalyzer.sqlblockchkr import file2sqlcodeblocks
from sqlanalyzer.output import strlist2file

"""
特定のフォルダ内のテキストファイルからSQLコードブロックをすべて
"""

filepath = "sqlsample/testfile.txt"

codeblocks = file2sqlcodeblocks(filepath)


strlist2file(codeblocks, "output.txt")
