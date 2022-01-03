import requests
from bs4 import BeautifulSoup

#def bar_searcher(songs):
    #searches thru artists songs with user inputting a word and whole lyric prints

def lyric_counter(song):
    res = requests.get(song)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    lyrics = []
    lyrics_counter = {}

    real_words = ['div']
    disallowed_characters = "\n\r?:.-!,/()"

    for t in text:
        if t.parent.name in real_words and t != '\n':
            output += '{} '.format(t)

    for character in disallowed_characters:
        output = output.replace(character, "")

    for word in output:
        info = output.lower().split(' ')
        lyrics = info

    for word in lyrics:
        if word.endswith('\'') and word != 'gon\'':
            fixed = word.replace('\'', 'g')
            lyrics.remove(word)
            lyrics.append(fixed)
        if word == 'gon\'':
            fixed = 'going'
            lyrics.remove(word)
            lyrics.append(fixed)
        if word == '':
            lyrics.remove(word)

    for word in lyrics:
        if word not in lyrics_counter:
            lyrics_counter[word] = 0
        lyrics_counter[word] += 1
    word_freq = []

    for key, value in lyrics_counter.items():
        word_freq.append((value, key))
    word_freq.sort(reverse=True)

    curse_counter = 0
    print()
    for word in lyrics:
        if "fuck" in word or "bitch" in word or "damn" in word or "pussy" in word or "nigg" in word or "piss" in word or "hell" in word or "cunt" in word or "dick" in word or "hoe" in word or "ass" in word or "cock" in word or "fag" in word or "shit" in word:
            curse_counter += 1
    print("The amount of curse words used in the song: " + str(curse_counter))
    print()
    print("These are the top ten most used words in the song")

    for x in range(0, 10):
        number_string = str(x+1)
        print(number_string + ": " + str(word_freq[x]))

    print()
    option = input("Do you want to search for a specific word? (y/n) ")
    while option.lower() == "y":
        word = input("What word would you like to see how frequent it was in this song? ")
        if word in lyrics:
            print(word + " was used " + str(lyrics_counter[word]) + " times")
        else:
            print("This word was never used in the lyrics of this song.")
        option = input("Do you want to search for another specific word? (y/n) ")
    print()
    print("Thanks for analyzing lyrics!")


artist_name = input("Enter the artist name you would like to see analyzed: ")
artist_name = artist_name.replace(" ", "")
artist_name = artist_name.lower()
song_title = input("Enter the song title you would like to see analyzed: ")
song_title = song_title.replace(" ", "")
song_title = song_title.lower()
url = "https://www.azlyrics.com/lyrics/" + artist_name + "/" + song_title + ".html"
lyric_counter(url)
