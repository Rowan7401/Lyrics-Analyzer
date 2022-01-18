import requests
import time
from bs4 import BeautifulSoup


def bar_searcher(artist_songs):
    res = requests.get(artist_songs)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    page = soup.find_all(attrs={"{s:": ""})

    page_as_words = str(page).split(" ")

    raw_links = []
    for word in page_as_words:
        if word.startswith("href="):
            raw_links.append(word)

    song_links_unfiltered = []
    for word in raw_links:
        if word.endswith("html\""):
            song_links_unfiltered.append(word)

    song_links = []
    for word in song_links_unfiltered:
        opening_quote_spot = word.find("\"")
        if word[opening_quote_spot:] not in song_links:
            song_link = word[opening_quote_spot:]
            song_links.append(song_link)

    for x in range(song_links.__len__()):
        song_links[x] = song_links[x].replace("\"", "")

    query = input("What word would you like to search if the artists uses in their bars? ")
    bar = ""
    mod_query = "[" + query + "]"
    for song in song_links:
        if song.startswith("https"):
            link = str(song)
            master_lyrics = lyric_sorter(link)
            line_spots = []
            start_line = 0
            bar_zone = 0
            if query in master_lyrics:
                query_spot = master_lyrics.index(query)
                for word in master_lyrics:
                    if "\n" in word:
                        end_line = master_lyrics.index(word)
                        line_spots.append(end_line)

                if query_spot <= line_spots[2]:
                    bar_zone = line_spots[4]
                    for x in range(0, bar_zone):
                        bar += master_lyrics[x] + " "
                elif query_spot >= line_spots[-3]:
                    start_line = line_spots[-5]
                    bar_zone = master_lyrics.__len__()
                    for x in range(start_line, bar_zone):
                        bar += master_lyrics[x] + " "
                else:
                    for x in range(line_spots.__len__()):
                        if line_spots[x] < query_spot <= line_spots[x+1]:
                            start_line = line_spots[x-2]
                            bar_zone = line_spots[x+3]
                    for x in range(start_line, bar_zone):
                        bar += master_lyrics[x] + " "
            if query in bar:
                bar = bar.replace(query, "[" + query + "]")
                print(bar)
                print()
            line_spots.clear()
        if song.startswith("/"):
            link = "https://www.azlyrics.com" + str(song)
            master_lyrics = lyric_sorter(link)
            line_spots = []
            start_line = 0
            bar_zone = 0
            if query in master_lyrics:
                query_spot = master_lyrics.index(query)
                for word in master_lyrics:
                    if "\n" in word:
                        end_line = master_lyrics.index(word)
                        line_spots.append(end_line)

                if query_spot <= line_spots[2]:
                    bar_zone = line_spots[4]
                    for x in range(0, bar_zone):
                        bar += master_lyrics[x] + " "
                elif query_spot >= line_spots[-3]:
                    start_line = line_spots[-5]
                    bar_zone = master_lyrics.__len__()
                    for x in range(start_line, bar_zone):
                        bar += master_lyrics[x] + " "
                else:
                    for x in range(line_spots.__len__()):
                        if line_spots[x] < query_spot <= line_spots[x + 1]:
                            start_line = line_spots[x - 2]
                            bar_zone = line_spots[x + 3]
                    for x in range(start_line, bar_zone):
                        bar += master_lyrics[x] + " "

            if query in bar and mod_query not in bar:
                bar = bar.replace(query, mod_query)
                print(bar)
                print()
            line_spots.clear()
    if len(bar) == 0:
        print("This word was never used in the artist's lyrics")


def lyric_sorter(song):
    res = requests.get(song)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    lyrics = []

    real_words = ['div']
    disallowed_characters = "\r?:.-!,/()\\\""

    for t in text:
        if t.parent.name in real_words and t != '\n':
            output += '{} '.format(t)

    for character in disallowed_characters:
        output = output.replace(character, "")

    for word in output:
        info = output.lower().split(' ')
        lyrics = info

    for x in range(37):
        lyrics.pop(0)

    while '' in lyrics:
        lyrics.remove('')

    song_end = lyrics.index("mxm")
    removables = lyrics.__len__() - song_end
    for x in range(removables):
        lyrics.pop(lyrics.__len__() - 1)
    lyrics[0] = lyrics[0].replace("\n", "")

    time.sleep(3)
    return lyrics


def lyric_sorter_wordcount(song):
    res = requests.get(song)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    lyrics = []
    lyrics_counter = {}

    real_words = ['div']
    disallowed_characters = "\n\r?:.-!,/()\\\""

    for t in text:
        if t.parent.name in real_words and t != '\n':
            output += '{} '.format(t)

    for character in disallowed_characters:
        output = output.replace(character, "")

    for word in output:
        info = output.lower().split(' ')
        lyrics = info

    for x in range(37):
        lyrics.pop(0)

    while '' in lyrics:
        lyrics.remove('')

    song_end = lyrics.index("mxm")
    removables = lyrics.__len__() - song_end
    for x in range(removables):
        lyrics.pop(lyrics.__len__() - 1)

    for word in lyrics:
        if word.endswith('\'') and word != 'gon\'':
            fixed = word.replace('\'', 'g')
            lyrics.remove(word)
            lyrics.append(fixed)
        if word == 'gon\'':
            fixed = 'going'
            lyrics.remove(word)
            lyrics.append(fixed)

    for word in lyrics:
        if word not in lyrics_counter:
            lyrics_counter[word] = 0
        lyrics_counter[word] += 1
    word_freq = []

    for key, value in lyrics_counter.items():
        word_freq.append((value, key))
    word_freq.sort(reverse=True)
    time.sleep(3)
    return lyrics, word_freq, lyrics_counter


def lyric_analyzer(lyrics, word_freq, lyrics_counter):
    curse_counter = 0
    print()
    for word in lyrics:
        if "fuck" in word or "bitch" in word or "damn" in word or "pussy" in word or "nigg" in word or "piss" in word or "hell" in word or "cunt" in word or "dick" in word or "hoe" in word or "ass" in word or "cock" in word or "fag" in word or "shit" in word:
            curse_counter += 1
    print("The amount of curse words used in the song: " + str(curse_counter))
    print()
    print("These are the top ten most used words in the song")

    for x in range(0, 10):
        number_string = str(x + 1)
        print(number_string + ": " + str(word_freq[x]))

    print()
    option = input("Do you want to search for a specific word? (y/n) ")
    while option.lower() == "y":
        word = input("What word would you like to see its frequency? ")
        if word in lyrics:
            print(word + " was used " + str(lyrics_counter[word]) + " times")
        else:
            print("This word was never used in the lyrics of this song.")
        option = input("Do you want to search for another specific word? (y/n) ")
    print()
    print("Thanks for analyzing lyrics!")


artist_name = input("Enter the artist name you would like to see analyzed: ")
first_letter = artist_name[0:1]
artist_name = artist_name.replace(" ", "")
artist_name = artist_name.lower()
decision = input("Do you want a specific song's lyrics to be analyzed? (y/n) ")
print()
if decision == "y":
    song_title = input("Enter the song title you would like to see analyzed: ")
    song_title = song_title.replace(" ", "")
    song_title = song_title.replace("\'", "")
    song_title = song_title.lower()
    url = "https://www.azlyrics.com/lyrics/" + artist_name + "/" + song_title + ".html"
    song_items = lyric_sorter_wordcount(url)
    lyric_analyzer(*song_items)

else:
    answer = input("Would you like to search for bars? (y/n) ")
    if answer == "y":
        if artist_name == "24kgoldn":
            url = "https://www.azlyrics.com/19/" + artist_name + ".html"
        else:
            url = "https://www.azlyrics.com/" + first_letter + "/" + artist_name + ".html"
        bar_searcher(url)
    else:
        print("alrighty then we will do nothing")
