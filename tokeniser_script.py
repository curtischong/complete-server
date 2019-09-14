def tokenize(text):
    """Given a string, returns the searchable keywords as a list of strings"""

    words_list = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "not"
    ]

    chars_list = [
        ":",
        ")",
        "(",
        "]",
        "[",
        "{",
        "}",
        "/",

    ]
    text = text.split()
    keywords = []
    for word in text:
        if word not in words_list and len(word) > 1:
            for char in word:
                if char in chars_list:
                    word = word.replace(char, "")
            keywords.append(word)
    return keywords
