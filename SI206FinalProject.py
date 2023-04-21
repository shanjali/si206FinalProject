import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import base64
import json
from secrets import *
import csv
import sqlite3
import os
from googleapiclient.discovery import build


def CreateToken():
        
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    

    data ={}

    clientId = "19010435a701468aaaac1fc85ab56058"
    clientSecret = "86d0ad27dfb14dfbbea6698626bff9d8"

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    
    return token


def read_in_top_songs():
    top_song_names = []
    with open("desktop/charts.csv", "r") as f:
        
        next(f)
        for line in f:
            
            top_song_names.append(line.split(",")[2])

    return top_song_names




def get_track_ids(song_names):
    track_ids = []
    base_url = 'https://api.spotify.com/v1/search'
    token = CreateToken()
    headers = {'Authorization': 'Bearer ' + token}
               
    for song in song_names:
        # search for the song on Spotify
        params = {'q': song, 'type': 'track'}
        response = requests.get(base_url, headers=headers, params=params).json()
        track_id = response['tracks']['items'][0]['id']
        track_ids.append(track_id)

    return track_ids

listofsong = ["Unwritten", "You Belong With Me", "Death by a Thousand Cuts", "All too well", "Dress", "Midnight Rain"]
#print(get_track_ids(read_in_top_songs()))

def get_popularity_score(idlist):
    base_url = "https://api.spotify.com/v1/tracks/{id}"
    token = CreateToken()
    headers = {'Authorization': 'Bearer ' + token}
    with open("Spotify.csv", "w", newline ='') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Artist Name", "Song Name", "Popularity Score"])
        count = 1
        for id in idlist:
            params = {'id': id}
            response = requests.get(base_url.format(id = id), headers=headers, params=params).json()
            writer.writerow([count, response['artists'][0]['name'], response['name'], response['popularity']])
            ##f.writerow(str(count) + "," + response['artists'][0]['name'] + "," +  response['name'] +  "," +str(response['popularity']) + "\n")
            count += 1


#early = get_track_ids(read_in_top_songs())
#get_popularity_score(early)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
youtube = build('youtube', 'v3', developerKey="AIzaSyDBAQwtfnUb2XEs-vfXnOTcALWe5j60Fk8")

def read_in(filename):

    '''
        Input: filename (Type: String)
		Output: video ids (Type: List)
        Reads in data from csv file and returns a list of video ids.
    '''
    
    ids = []

    inFile = open(filename)
    csv_file = csv.reader(inFile)

    headers = next(inFile)

    for row in csv_file:
        ids.append(row[-1])

    inFile.close()

    return ids

def write_out(filename, tup_in):

    '''
        Input: filename (Type: String), tup_in (Type: Tuple)
		Output: nothing
        Writes data to a csv file.
    '''

    outFile = open(filename, "w")
    csv_file = csv.writer(outFile)

    header = ("id", "music video title", "view count", "like count", "dislike count", "comment count")
    csv_file.writerow(header)

    for tup in tup_in:
        csv_file.writerow(tup)



def get_video_stats(ids):
    '''
        Input: Youtube ids (Type: List)
		Output: Statistics of Youtube ids (Type: List)
        Extracts video data from Youtube API given a list of video ids.
    '''

    stats_list = []

    id_num = 1

    for i in range(0, len(ids), 25):
        request = youtube.videos().list(
            part = "snippet, statistics",
            id = ids[i:i+25]
        )

        data = request.execute()
        for video in data['items']:
            title =  video["snippet"]["title"]
            view_count = video['statistics'].get('viewCount',0)
            like_count = video['statistics'].get('likeCount',0)
            dislike_count = video['statistics'].get('dislikeCount',0)
            comment_count = video['statistics'].get('commentCount',0)
            tup = (id_num, title, view_count, like_count, dislike_count, comment_count)
            id_num += 1
            stats_list.append(tup)

    return stats_list



ids = read_in("charts.csv")
vids = get_video_stats(ids)
write_out("youtube.csv", vids)


def create_Spotify_db():

  
        conn = sqlite3.connect('Spotify_And_Youtube_Table.db')
        cursor = conn.cursor()
  
        conn.execute('''CREATE TABLE IF NOT EXISTS Spotify_Table
                        (
                        Value INT,
                        Artist_Name TEXT,
                        Song_Name TEXT,
                        Popularity INT);''')

   
        with open('Spotify.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

           
            next(csv_reader)

            # Insert each row of the CSV data into the table
            for i, row in enumerate(csv_reader):
                if i >= 25:
                    break
                conn.execute("INSERT INTO Spotify_Table (Value, Artist_Name, Song_Name, Popularity) VALUES (?, ?, ?, ?)", row)
                
        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

#create_Spotify_db()

def create_Youtube_db():

    # Connect to a new database (creates a new file if it doesn't exist)
        conn = sqlite3.connect('Spotify_And_Youtube_Table.db')

        # Create a new table to hold the CSV data
        conn.execute('''CREATE TABLE IF NOT EXISTS Youtube_Table
                        (
                        Value INT,
                        Music_Video TEXT,
                        View_Count INT,
                        Like_Count INT,
                        Dislike_Count INT,
                        Comment_Count INT);''')

        # Open the CSV file and read its contents
        with open('youtube.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            
            next(csv_reader)
            for i, row in enumerate(csv_reader):
                if i >= 25:
                    break
                conn.execute("INSERT INTO Youtube_Table (Value, Music_Video, View_Count, Like_Count, Dislike_Count, Comment_Count) VALUES (?, ?, ?, ?, ?, ?)", row)

    
        conn.commit()

        # Close the database connection
        conn.close()
 
#create_Youtube_db()



