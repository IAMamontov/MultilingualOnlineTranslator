import requests
from bs4 import BeautifulSoup
import re
from sys import argv, exit


def get_translation(lang_src, lang_trg, word_tr, num_ex):
    prepped.url = f"https://context.reverso.net/translation/{lang_src}-{lang_trg}/{word_tr}"
    prepped.headers['User-Agent'] = 'Mozilla/5.0'
    r = s.send(prepped)
    words = []
    sentences = []
    result = ""
    if r.status_code == requests.codes.ok:
        # print(f"{r.status_code} OK")
        soup = BeautifulSoup(r.content, "html.parser")
        a = soup.find_all('a', class_=re.compile("^translation "))
        for i in a:
            words.append(i.get_text().strip())
        b = soup.find_all('div', class_=re.compile("^(src|trg) (rtl|ltr)(| arabic)$"))
        for i in b:
            sentences.append((i.get_text().strip()))
    else:
        if r.status_code == 404:
            print(f"Sorry, unable to find {word_tr}")
        else:
            print(f"Something wrong with your internet connection")
        exit(1)
    result += f"{lang_trg.capitalize()} Translations:\n"
    for i in range(num_ex):
        if len(words) > i:
            result += f"{words[i]}\n"
        else:
            break
    result += "\n"
    result += f"{lang_trg.capitalize()} Examples:\n"
    for i in range(0, num_ex * 2, 2):
        if len(sentences) >= i:
            result += f"{sentences[i]}\n"
            result += f"{sentences[i + 1]}\n"
            result += "\n"
        else:
            break
    return result


if __name__ == '__main__':
    languages = """1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
"""
    languages_list = [
        "arabic", "german", "english", "spanish", "french", "hebrew", "japanese",
        "dutch", "polish", "portuguese", "romanian", "russian", "turkish", "all"
    ]
    src, trg = 0, 1
    if len(argv) > 0:
        try:
            src = languages_list.index(argv[1])
        except ValueError:
            print(f"Sorry, the program doesn't support {argv[1]}")
            exit(1)
        try:
            trg = languages_list.index(argv[2])
        except ValueError:
            print(f"Sorry, the program doesn't support {argv[2]}")
            exit(1)
        word = argv[3].lower()
    else:
        print("Hello, you're welcome to the translator.")
        print("Translator supports:")
        print(languages)
        print("Type the number of your language:")
        src = int(input()) - 1
        print("Type the number of language you want to translate to:")
        trg = int(input()) - 1
        print("Type the word you want to translate:")
        word = input().lower()
    s = requests.Session()
    link = f"https://context.reverso.net/translation/{languages_list[src]}-{languages_list[trg]}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.Request('GET', url=link, headers=headers)
    prepped = s.prepare_request(req)
    out = ""
    if 0 <= trg < 13:
        out = get_translation(languages_list[src], languages_list[trg], word, 5)
    else:
        for _ in [x for x in range(13) if x != src]:
            out += get_translation(languages_list[src], languages_list[_], word, 1)
    print(out)
    with open(f"{word}.txt", "w") as f:
        f.write(out)
    s.close()
