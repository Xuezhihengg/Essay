import json


def load_json(file_path: str):
    """从文件加载 JSON 数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file '{file_path}': {e}")

def dump_json(data, file_path, indent=4):
    """将 Python 数据保存为 JSON 文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
    except Exception as e:
        print(f"Error saving JSON file '{file_path}': {e}")
        

