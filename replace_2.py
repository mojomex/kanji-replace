# encoding: utf-8
import unicodedata
from utils.create_hash_kanji2emoji import get_kanji2emoji_dict

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

kanji = set()
for char in text:
    if 0x9faf >= ord(char) >= 0x4e00:
        kanji.add(char)
kanji_list = list(kanji)


# https://github.com/kyokomi/emoji/blob/master/cmd/generateEmojiCodeMap/emoji_data.go
# https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json
import json 
with open("emoji.json", "rb") as f:
    emoji_info = json.load(f)
emoji_unicodes = [int("0x"+info["unified"], 16) for info in emoji_info if "-" not in info["unified"]] # not include like "1F1E7-1F1FF"
print("All emojis:", len(emoji_unicodes))
# print(emoji_unicodes[:10])
emoji2meaning_dict= {} 
for i in range(len(emoji_unicodes)):
    try:
        emoji = chr(emoji_unicodes[i])
        emoji_name = unicodedata.name(emoji)
        emoji2meaning_dict[emoji] = emoji_name
    except:
        pass
print("Valid emojis:", len(emoji2meaning_dict))

meaning2emoji_dict = {v:k for k,v in emoji2meaning_dict.items()}
emoji_list = [k for k,v in meaning2emoji_dict.items()]
# print(emoji2meaning_dict)


kanji2emoji_meaning, kanji_meaning2emoji_meaning = get_kanji2emoji_dict(kanji_list, emoji_list)
with open(f"kanji2emoji_meaning.txt", "w", encoding="utf-8") as f:
    f.write(str(kanji2emoji_meaning))
with open(f"kanji_meaning2emoji_meaning.txt", "w", encoding="utf-8") as f:
    f.write(str(kanji_meaning2emoji_meaning))

replacements = {k:meaning2emoji_dict[v] for k, v in kanji2emoji_meaning.items()}

for (k, v) in replacements.items():
    text = text.replace(k, v)

from utils.utils import save_hash_table
save_hash_table(replacements, "hash_table")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)