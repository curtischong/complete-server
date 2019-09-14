import subprocess


def fetchData(search_words):

    cmd = "https://searchcode.com/api/codesearch_I/?q="
    for search_word in search_words
    cmd += search_word + "+"
    cmd = cmd[:-1]
    cmd += "&p=1&per_page=100"
