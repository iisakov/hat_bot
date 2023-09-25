import requests

response_word = requests.get('https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt')
response_emoji = requests.get('https://unicode.org/Public/emoji/15.0/emoji-sequences.txt')

text_word = response_word.text
text_emoji = response_emoji.text

with open('word.txt', 'wb') as word:
    word.write(text_word.encode('utf-8'))

with open('emoji.txt', 'wb') as emoji:
    emoji.write(text_emoji.encode('utf-8'))
