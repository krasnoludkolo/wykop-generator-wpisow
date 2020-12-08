import os
import time
import re

import markovify
from wykop import WykopAPI

key = os.environ.get('WYKOP_TAG_KEY')
secret = os.environ.get('WYKOP_TAG_SECRET')

api = WykopAPI(key, secret, output='clear')


def remove_tags(text):
    return re.sub(r'#(\w*[0-9a-zA-Z]+\w*[0-9a-zA-Z])', '', text)


def remove_empty_lines(text: str):
    return '\n'.join([line for line in text.split("\n") if line.strip()])


def filter_to_short(text, min_words=5):
    return '\n'.join([line for line in text.split('\n') if len(line.split(' ')) >= min_words])


def get_messages(tag, pages=100):
    messages = []
    for i in range(pages):
        print(f'{i + 1}/{pages}')
        x = api.tag(tag, page=i)
        m = [entry.entry.body for entry in x if entry.type == 'entry']
        messages += m
        time.sleep(0.3)
    return '\n'.join(messages)


def save(text, tag):
    open(f'{tag}.txt', 'w', encoding="utf-8").write(text)


def load(tag):
    return open(f'{tag}.txt', 'r', encoding="utf-8").read()


def main():
    tag = "polityka"
    messages = get_messages(tag, 500)
    messages = remove_tags(messages)
    messages = remove_empty_lines(messages)
    text = filter_to_short(messages)

    save(text, tag)

    model = markovify.Text(load(tag), state_size=3)

    for _ in range(5):
        print(model.make_sentence(tries=100))


main()
