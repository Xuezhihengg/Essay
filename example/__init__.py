import os

def load_example(filename: str) -> str:
    """
    加载 example 文件夹中的 txt 文件内容为字符串。

    Args:
        filename (str): 文本文件的名称，例如 "example.txt"。

    Returns:
        str: 文件内容的字符串。

    Raises:
        FileNotFoundError: 如果文件不存在。
        ValueError: 如果文件扩展名不是 .txt。
    """
    if not filename.endswith('.txt'):
        raise ValueError("只支持加载 .txt 文件")
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件 {filename} 不存在于 {current_dir}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content
