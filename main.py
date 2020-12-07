import os

import markovify
from wykop import WykopAPI
import time

key = os.environ.get('WYKOP_TAG_KEY')
secret = os.environ.get('WYKOP_TAG_SECRET')

api = WykopAPI(key, secret, output='clear')


def remove_tags(text):
    result = []
    for line in text.split('\n'):
        result.append(' '.join([word for word in line.split(' ') if '#' not in word]))
    return '\n'.join([x for x in result if x])


def format(text: str):
    return text.replace('\n\n', '\n')


def filter_to_short(text, min_words=5):
    return '\n'.join([line for line in text.split('\n') if len(line.split(' ')) >= min_words])


def get_messages(tag, pages=100):
    messages = []
    for i in range(pages):
        print(f'{i + 1}/{pages}')
        x = api.tag(tag, page=i)
        m = [entry.entry.body for entry in x if entry.type == 'entry']
        messages += m
        time.sleep(1)
    return '\n'.join(messages)


def save(text, tag):
    open(f'{tag}.txt', 'w', encoding="utf-8").write(text)


def load(tag):
    return open(f'{tag}.txt', 'r', encoding="utf-8").read()


def main():
    tag = "polityka"
    messages = get_messages(tag, 100)
    messages = remove_tags(messages)
    messages = format(messages)
    text = filter_to_short(messages)

    save(text, tag)

    model = markovify.Text(text, state_size=3)

    for _ in range(5):
        print(model.make_sentence(tries=100))
