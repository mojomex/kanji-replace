# encoding: utf-8
import os
import unicodedata
from utils.create_hash_kanji2emoji import get_kanji2emoji_dict


def replace_texts(file_name):

    ### open text file
    input_file_name = f"inputs/{file_name}.txt"
    with open(input_file_name, "r", encoding="utf-8") as f:
        text = f.read()

    ### get kanji list in texts
    kanji = set()
    for char in text:
        if 0x9faf >= ord(char) >= 0x4e00:
            kanji.add(char)
    kanji_list = list(kanji)

    ### get list of emojis 
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
    

    ### get dict of kanji2emoji
    kanji2emoji_meaning, kanji_meaning2emoji_meaning = get_kanji2emoji_dict(kanji_list, emoji_list)
    # save
    os.makedirs(f"results/{file_name}", exist_ok=True)
    with open(f"results/{file_name}/kanji2emoji_meaning.txt", "w", encoding="utf-8") as f:
        f.write(str(kanji2emoji_meaning))
    with open(f"results/{file_name}/kanji_meaning2emoji_meaning.txt", "w", encoding="utf-8") as f:
        f.write(str(kanji_meaning2emoji_meaning))

    replacements = {k:meaning2emoji_dict[v] for k, v in kanji2emoji_meaning.items()}

    from utils.utils import save_hash_table
    save_hash_table(replacements, f"results/{file_name}/kanji2emoji")

    ### replace text 
    for (k, v) in replacements.items():
        text = text.replace(k, v)
    # save
    with open(f"results/{file_name}/output.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Successfully replaced at: results/{file_name}/output.txt")
    print(f"Successfully replaced at: output.txt")



if __name__=="__main__":

    ### REPLACE ALL TEXTFILES

    # import glob
    # f_list = glob.glob("inputs/*.txt")
    # f_list = [f.split('/')[1].replace('.txt','') for f in f_list]
    # for FILE_NAME in f_list:
    #     print(f"==== {FILE_NAME} ====")
    #     replace_texts(FILE_NAME)
    
    ### REPLACE SINGLE TEXTFILE
    
    # file should be in inputs folder
    FILE_NAME = "pretender"
    replace_texts(FILE_NAME)