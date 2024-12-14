import os
from typing import List, Optional

def load_text(file_path: str, encoding: Optional[str] = "utf-8") -> str:
    """加载文件的完整文本内容"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        raise e
    except Exception as e:
        print(f"Error loading text from {file_path}: {e}")
        raise e

def load_text_lines(file_path: str, encoding: Optional[str] = "utf-8") -> List[str]:
    """按行加载文件内容为列表"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding=encoding) as file:
            return file.readlines()
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        raise e
    except Exception as e:
        print(f"Error loading lines from {file_path}: {e}")
        raise e

def dump_text(file_path: str, content: str, encoding: Optional[str] = "utf-8") -> None:
    """将完整文本写入文件，覆盖原有内容"""
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        raise e

def dump_text_lines(file_path: str, lines: List[str], encoding: Optional[str] = "utf-8") -> None:
    """将多行文本写入文件，覆盖原有内容"""
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.writelines(lines)
    except Exception as e:
        print(f"Error writing lines to {file_path}: {e}")
        raise e

def append_text(file_path: str, content: str, encoding: Optional[str] = "utf-8") -> None:
    """将文本追加到文件末尾"""
    try:
        with open(file_path, "a", encoding=encoding) as file:
            file.write(content)
    except Exception as e:
        print(f"Error appending text to {file_path}: {e}")
        raise e

def append_text_lines(file_path: str, lines: List[str], encoding: Optional[str] = "utf-8") -> None:
    """将多行文本追加到文件末尾"""
    try:
        with open(file_path, "a", encoding=encoding) as file:
            file.writelines(lines)
    except Exception as e:
        print(f"Error appending lines to {file_path}: {e}")
        raise e
