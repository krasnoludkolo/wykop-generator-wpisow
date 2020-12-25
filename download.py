import datetime
import os
import re
import time

from typing import NoReturn
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
    entry = api.entry(str(entry.id))
    for comment in entry.comments:
        if 'body' in comment:
            texts.append(comment.body)
    return '\n'.join(texts)


def get_messages(tag, pages=100, download_comments=False) -> str:
    messages = []
    for i in range(pages):
        print(f'{datetime.datetime.now()}: Strona: {i + 1}/{pages} tagu #polityka')
        x = api.tag(tag, page=i)
        m = [get_texts_from_entry_and_comments(entry.entry) if download_comments else entry.entry.body for entry in x if
             entry.type == 'entry']
        messages += m
        time.sleep(0.3)
    return '\n'.join(messages)


def save(text, tag) -> NoReturn:
    open(f'{tag}.txt', 'w', encoding="utf-8").write(text)


def load(tag) -> str:
    return open(f'{tag}.txt', 'r', encoding="utf-8").read()


def format_message(text):
    return f"{text}" \
           f"\n\n #politykabot" \
           f"\n\n! O co w tym chodzi?" \
           f" Jestem botem który generuje wiadomości na podstawie wpisów z tagu polityka"


def download(tag):
    messages = get_messages(tag, 500)
    messages = remove_tags(messages)
    messages = remove_nicknames(messages)
    messages = remove_empty_lines_and_format(messages)
    text = filter_to_short(messages, min_words=5)
    save(text, tag)


def main():
    tag = "polityka"
    download(tag)


if __name__ == 'main':
    main()
