from pathlib import Path
from config.config import read_config

from openai import OpenAI


def get_client():
    """
    创建Kimi client
    :return: client
    """
    config = read_config()
    return OpenAI(
        api_key=config.get("api_key"),
        base_url="https://api.moonshot.cn/v1",
    )


def list_modules(client: OpenAI):
    """
    支持的所有类型
    :param client:
    :return:
    """
    module_list = client.models.list()
    return module_list.data


def client_chat_batch(content: str):
    """
    批量调用-默认角色
    :param content: 提出的问题
    :return: 返回的答案
    """
    client = get_client()
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI "
                        "提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI "
                        "为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": content}
        ],
        temperature=0.3,
    )
    return completion.choices[0].message.content


def client_chat_batch_set(content_set: str, content_user: str):
    """
    批量调用-可以设定角色
    :param content_set: 设定角色
    :param content_user: 提问内容
    :return:
    """
    client = get_client()
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": content_set},
            {"role": "user", "content": content_user}
        ],
        temperature=0.3,
    )
    return completion.choices[0].message.content


def client_chat_stream(content_user: str):
    """
    流式调用-默认角色
    :param content_user:
    :return:
    """
    client = get_client()

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI "
                           "提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI "
                           "为专有名词，不可翻译成其他语言。",
            },
            {"role": "user", "content": content_user},
        ],
        temperature=0.3,
        stream=True,
    )
    collected_messages = []
    for idx, chunk in enumerate(response):
        chunk_message = chunk.choices[0].delta
        if not chunk_message.content:
            continue
        collected_messages.append(chunk_message)  # save the message
        print(f"#{idx}: {''.join([m.content for m in collected_messages])}")
    return ''.join([m.content for m in collected_messages])


def client_chat_stream_set(content_set: str, content_user: str):
    """
    流式调用-可以设定角色
    :param content_set:
    :param content_user:
    :return:
    """
    client = get_client()

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {
                "role": "system",
                "content": content_set,
            },
            {"role": "user", "content": content_user},
        ],
        temperature=0.3,
        stream=True,
    )
    collected_messages = []
    for idx, chunk in enumerate(response):
        chunk_message = chunk.choices[0].delta
        if not chunk_message.content:
            continue
        collected_messages.append(chunk_message)  # save the message
        print(f"#{idx}: {''.join([m.content for m in collected_messages])}")
    return ''.join([m.content for m in collected_messages])


def client_chat_files(file_path: str, content_user: str):
    client = get_client()

    file_object = client.files.create(file=Path(file_path), purpose="file-extract")

    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，之前 retrieve_content api 在最新版本标记了 warning, 可以用下面这行代替
    # 如果是旧版本，可以用 retrieve_content
    file_content = client.files.content(file_id=file_object.id).text

    # 把它放进请求中
    messages = [
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI "
                       "提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI "
                       "为专有名词，不可翻译成其他语言。",
        },
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "user", "content": content_user},
    ]

    # 然后调用 chat-completion, 获取 kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )

    return completion.choices[0].message.content
