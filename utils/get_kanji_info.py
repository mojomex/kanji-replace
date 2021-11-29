# pip install --upgrade jamdict jamdict-data
# to use (https://opensourcelibs.com/lib/jamdict)

from jamdict import Jamdict
jam = Jamdict()

def get_kanji_info(char):
    """
    not in unicode
    """
    result = jam.lookup(char)
    kanji_info = repr(result.chars[0])
    stoke_num = int(kanji_info.split(":")[1])
    meanings = kanji_info.split(":")[2]
    return stoke_num, meanings

if __name__=="__main__":
    result = jam.lookup("愛")
    print(result.chars[0])
    print(repr(result.chars[0]))
    print(get_kanji_info("愛"))

    # with open("input.txt", "r", encoding="utf-8") as f:
    #     text = f.read()

    # kanji = set()
    # for char in text:
    #     if 0x9faf >= ord(char) >= 0x4e00:
    #         kanji.add(char)

    # print(get_kanji_info(list(kanji)[0]))