# encoding: utf-8

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

kanji = set()

for char in text:
    if 0x9faf >= ord(char) >= 0x4e00:
        kanji.add(char)


replacements = {}

for (i, kan) in enumerate(kanji):
    replacements[kan] = chr(0x1F400 + i)

for (k, v) in replacements.items():
    text = text.replace(k, v)

from utils.utils import save_hash_table
save_hash_table(replacements, "hash_table")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)