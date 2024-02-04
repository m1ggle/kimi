from pathlib import Path

from openai.types import FileObject

from kimi_client import get_client


def get_kimi_file() -> FileObject:
    """
    获取已经上传的文件
    :return:
    """
    client = get_client()
    return client.files.list()


def upload_kimi_file(file_path: str):
    """
    上传文件
    :return:
    """
    client = get_client()
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    if file_object.status == "processed":
        return True
    else:
        return False
