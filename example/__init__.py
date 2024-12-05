import os
import json
from typing import TypedDict

class Example(TypedDict):
    Grade: str
    Title: str
    ModelContent: str
    Content: str
    


def load_json_example(filename: str) -> Example:
    """
    加载 example 文件夹中的 JSON 文件并解析为 Python 字典。

    Args:
        filename (str): JSON 文件的名称，例如 "example.json"。

    Returns:
        dict: 解析后的 JSON 数据。

    Raises:
        FileNotFoundError: 如果文件不存在。
        ValueError: 如果文件扩展名不是 .json。
        json.JSONDecodeError: 如果 JSON 格式不合法。
    """
    if not filename.endswith('.json'):
        raise ValueError("只支持加载 .json 文件")
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件 {filename} 不存在于 {current_dir}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 文件格式错误: {e}")
    
    return content

