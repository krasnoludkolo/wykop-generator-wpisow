import datetime
import os
import re
import time
import logging

from typing import NoReturn, Tuple
from wykop import WykopAPI

key = os.environ.get('WYKOP_TAKTYK_KEY')
secret = os.environ.get('WYKOP_TAKTYK_SECRET')

api = WykopAPI(key, secret, output='clear')


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


def get_messages(tag, download_comments=False, page=1) -> str:
    messages = []
    logging.info(f'{datetime.datetime.now()}: Strona: {page} tagu #{tag}')
    x = api.search_entries(query=f'#{tag}', page=page, when='month')
    m = [get_texts_from_entry_and_comments(entry) if download_comments else entry.body for entry in x]
    messages += m
    time.sleep(0.3)
    result = '\n'.join(messages)
    if x:
        logging.info(x[0]['date'])
        result += '\n' + get_messages(tag, download_comments, page + 1)
    return result


def save(text, tag) -> NoReturn:
    open(f'{tag}.txt', 'w', encoding="utf-8").write(text)


def download(tag):
    messages = get_messages(tag)
    messages = remove_tags(messages)
    messages = remove_nicknames(messages)
    messages = remove_empty_lines_and_format(messages)
    text = filter_to_short(messages, min_words=5)
    save(text, tag)


def main():
    tag = "grybezpradu"
    download(tag)


if __name__ == '__main__':
    main()
