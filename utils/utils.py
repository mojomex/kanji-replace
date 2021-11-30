import pickle 

def save_hash_table(replacements, file_name="hash_table"):
    """
    replacements: dict
        {kanji: emoji}
    """
    # sort by kanji unicode
    replacements = dict(sorted(replacements.items(), key=lambda x:x[0]))

    with open(f"{file_name}.pkl", "wb") as f:
        pickle.dump(replacements, f)

    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(str(replacements))
    print(f"Hash dict saved: {file_name}")


def load_pickle(file_name):
    with open(f"{file_name}.pkl", "rb") as f:
        d = pickle.load(f)
    return d

    