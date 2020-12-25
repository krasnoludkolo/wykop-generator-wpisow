import datetime
import os
import re
import time

from typing import NoReturn, Tuple
from wykop import WykopAPI

key = os.environ.get('WYKOP_TAKTYK_KEY')
secret = os.environ.get('WYKOP_TAKTYK_SECRET')
account_key = os.environ.get('WYKOP_TAKTYK_ACCOUNTKEY')

api = WykopAPI(key, secret, output='clear', account_key=account_key)
api.authenticate()


def remove_tags(text) -> str:
    return re.sub(r'#(\w*[0-9a-zA-Z]+\w*[0-9a-zA-Z])', '', text)


def remove_nicknames(text) -> str:
    return re.sub(r'@(\w*[0-9a-zA-Z]+\w*[0-9a-zA-Z]:)', '', text)


def remove_empty_lines_and_format(text: str) -> str:
    return '\n'.join([line.strip() for line in text.split("\n") if line.strip()])


def filter_to_short(text, min_words=5) -> str:
    return '\n'.join([line for line in text.split('\n') if len(line.split(' ')) >= min_words])


def get_texts_from_entry_and_comments(entry) -> str:
    texts = [entry.body]
    if entry.comments_count == 0:
        return texts[0]

    time.sleep(0.3)
    entry = api.entry(entry.id)
    for comment in entry.comments:
        if 'body' in comment:
            texts.append(comment.body)
    return '\n'.join(texts)


def get_messages(tag, pages=100, download_comments=False) -> Tuple[str, int]:
    messages = []
    last_id = -1
    for i in range(1, pages+1):
        print(f'{datetime.datetime.now()}: Strona: {i}/{pages} tagu #{tag}')
        x = api.tag_entries(tag, page=i)
        if i == 1:
            last_id = int(x[0]['id'])
        m = [get_texts_from_entry_and_comments(entry.entry) if download_comments else entry.entry.body for entry in x if
             entry.type == 'entry']
        messages += m
        time.sleep(0.3)
    return '\n'.join(messages), last_id


def save(text, tag, last_id) -> NoReturn:
    open(f'{tag}.txt', 'w', encoding="utf-8").write(text)
    open(f'{tag}_last_id.txt', 'w', encoding="utf-8").write(str(last_id))


def download(tag):
    messages, last_id = get_messages(tag, 10)
    messages = remove_tags(messages)
    messages = remove_nicknames(messages)
    messages = remove_empty_lines_and_format(messages)
    text = filter_to_short(messages, min_words=5)
    save(text, tag, last_id)


def main():
    tag = "grybezpradu"
    download(tag)


if __name__ == 'main':
    main()
