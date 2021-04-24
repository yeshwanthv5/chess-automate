# chess.com API -> https://www.chess.com/news/view/published-data-api
# The API has been used to download monthly archives for a user using a Python3 program.
# This program works as of 24/09/2018

import urllib
import urllib.request

user_list = ["magnuscarlsen"]
for username in user_list:
    print("Downloading games of " + username)
    baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
    archivesUrl = baseUrl + "archives"

    #read the archives url and store in a list
    f = urllib.request.urlopen(archivesUrl)
    archives = f.read().decode("utf-8")
    archives = archives.replace("{\"archives\":[\"", "\",\"")
    archivesList = archives.split("\",\"" + baseUrl)
    archivesList[len(archivesList)-1] = archivesList[len(archivesList)-1].rstrip("\"]}")

    #download all the archives
    for i in range(len(archivesList)-1):
        url = baseUrl + archivesList[i+1] + "/pgn"
        filename = archivesList[i+1].replace("/", "-")
        urllib.request.urlretrieve(url, "/path/to/datasets/" + username + "/" + filename + ".pgn") #change
        print(filename + ".pgn has been downloaded.")
    print ("All files have been downloaded for " + username)