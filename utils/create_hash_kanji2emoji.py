import numpy as np
from scipy.spatial import distance
from scipy.optimize import linear_sum_assignment

try:
    from utils.get_kanji_info import get_kanji_info
    from utils.get_sentence_embedding import embed
except:
    from get_kanji_info import get_kanji_info
    from get_sentence_embedding import embed


def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    l2[l2==0] = 1
    return v/l2


def get_kanji2emoji_dict(kanji_list, emoji_names_list):

    # embed kanji
    print("embedding kanji...: ", len(kanji_list))
    kanji_meaning_list = [get_kanji_info(kanji)[1] for kanji in kanji_list]
    kanji_embeddings_arr = embed(kanji_meaning_list)
    kanji_embeddings_arr = normalize(kanji_embeddings_arr)

    # embed emoji
    print("embedding kanji...: ", len(emoji_names_list))
    emoji_embeddings_arr = embed(emoji_names_list)
    emoji_embeddings_arr = normalize(emoji_embeddings_arr)

    # calc dist matrix
    print("Calculating distance matrix... (i, j):", len(kanji_embeddings_arr), len(emoji_embeddings_arr))
    cost = distance.cdist(kanji_embeddings_arr, emoji_embeddings_arr, 'euclidean')

    # matching
    print("Matching...")
    row_ind, col_ind = linear_sum_assignment(cost)

    # dict
    kanji2emoji_meaning = {}
    for i, j in zip(row_ind, col_ind):
        kan = kanji_list[i]
        emo = emoji_names_list[j]
        kanji2emoji_meaning[kan] = emo
    # print(d)


    kanji_meaning2emoji_meaning = {}
    for i, j in zip(row_ind, col_ind):
        kan_mean = kanji_meaning_list[i]
        emo = emoji_names_list[j]
        kanji_meaning2emoji_meaning[kan_mean] = emo


    return kanji2emoji_meaning, kanji_meaning2emoji_meaning

if __name__=='__main__':

    kanji_list = ["笑", "愛", "島"] # not in unicode
    kanji_meaning_list = [get_kanji_info(kanji)[1] for kanji in kanji_list]

    kanji_embeddings_arr = embed(kanji_meaning_list)
    kanji_embeddings_arr = normalize(kanji_embeddings_arr)

    emoji_names_list = ["Smile", "love", "island"]
    emoji_embeddings_arr = embed(emoji_names_list)
    emoji_embeddings_arr = normalize(emoji_embeddings_arr)

    # calc dist matrix
    print(len(kanji_embeddings_arr), len(emoji_embeddings_arr))
    cost = distance.cdist(kanji_embeddings_arr, emoji_embeddings_arr, 'euclidean')

    # matching
    row_ind, col_ind = linear_sum_assignment(cost)

    # dict
    d = {}
    for i, j in zip(row_ind, col_ind):
        kan = kanji_list[i]
        emo = emoji_names_list[j]
        d[kan] = emo
    print(d)