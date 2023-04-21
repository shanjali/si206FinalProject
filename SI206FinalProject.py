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



def CreateToken():

    '''
        Input: Nothing
	    Output: Spotify access Token (Type: String)

        Creates Spotify access token.
    '''
        
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
    '''
        Input: Nothing
	    Output: 100 top song name from Charts.csv (Type: List)

        Extracts the top 100 songs from the inputted csv.
    '''
    top_song_names = []
    with open("charts.csv", "r") as f:
        
        next(f)
        for line in f:
            
            top_song_names.append(line.split(",")[2])

    return top_song_names




def get_track_ids(song_names):
    '''
        Input: List of song names
	    Output: Spotify Track IDs (Type: List)

        Takes in a list of song names and returns their Spotify track ids.
    '''
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

#listofsong = ["Unwritten", "You Belong With Me", "Death by a Thousand Cuts", "All too well", "Dress", "Midnight Rain"]
#print(get_track_ids(read_in_top_songs()))

def get_popularity_score(idlist):
    '''
        Input: List of Spotify Track IDs
	    Output: Nothing

        Writes out the popularity scores of the given songs based on the inputted track ids.
    '''

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

def create_Spotify_db():
    '''
        Input: Nothing
	    Output: Nothing

        Creates the database.
    '''
  
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

create_Spotify_db()

def create_Youtube_db():

    '''
        Input: Nothing
	    Output: Nothing

        Creates the database.
    '''

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
 
create_Youtube_db()



def create_text_file_from_DB():

    '''
        Input: Nothing
	    Output: Nothing

        Creates a text file of 25 items from the database.
    '''

    conn = sqlite3.connect('Spotify_And_Youtube_Table.db')
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT Spotify_Table.Song_Name, Spotify_Table.Popularity as Spotify_Popularity,round(Cast(Youtube_Table.Comment_Count+Youtube_Table.Like_Count as REAL)/Cast(Youtube_Table.View_Count as REAL)*1000,4) as Youtube_Enagement_Score From Spotify_Table join Youtube_Table on Youtube_Table.Value= Spotify_Table.value")
    rows = cur.fetchall()


    with open('Spotify_And_YouTube_DB.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])  
        writer.writerows(rows)

    conn.close()


create_text_file_from_DB()

"""SELECT DISTINCT Spotify_Table.Song_Name, Spotify_Table.Popularity as Spotify_Popularity,round(Cast(Youtube_Table.Comment_Count+Youtube_Table.Like_Count as REAL)/Cast(Youtube_Table.View_Count as REAL)*1000,4) as Youtube_Enagement_Score
From Spotify_Table
join Youtube_Table on Youtube_Table.Value= Spotify_Table.value
"""