import logging

import markovify

from download import download


def load(tag) -> str:
    return open(f'{tag}.txt', 'r', encoding="utf-8").read()


def format_message(text):
    return f"{text}" \
           f"\n\n #politykabot" \
           f"\n\n! O co w tym chodzi?" \
           f" Jestem botem który generuje wiadomości na podstawie wpisów z tagu polityka"


def generate_message(model):
    message = model.make_sentence(tries=100)
    if message:
        return message
    return generate_message(model)


def main():
    logging.basicConfig(level=logging.INFO)
    tag = "polityka"
    # download(tag)
    state_size = 3


    model = markovify.Text(load(tag), state_size=state_size)
    #
    # op = model.make_sentence(tries=500, max_overlap_ratio=0.5)
    # start = random.randint(0, len(op.split()) - state_size)
    # start_state = " ".join(op.split()[start:start + state_size])
    # print(start_state)
    # comment = model.make_sentence(init_state=start_state, tries=500, max_overlap_ratio=0.5)

    print(model.make_short_sentence(max_chars=1000, min_chars=100))
    a = generate_message(model)
    print(a)
    print(len(a))
    # print(comment)


main()
