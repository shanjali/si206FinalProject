import os
from googleapiclient.discovery import build
import requests
import json
from secrets import *
import csv

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
youtube = build('youtube', 'v3', developerKey="AIzaSyDBAQwtfnUb2XEs-vfXnOTcALWe5j60Fk8")

def read_in(filename):
    ids = []

    inFile = open(filename)
    csv_file = csv.reader(inFile)

    headers = next(inFile)

    for row in csv_file:
        ids.append(row[-1])

    inFile.close()

    return ids

def write_out(filename, tup_in):

    outFile = open(filename, "w")
    csv_file = csv.writer(outFile)

    header = ("id", "music video title", "view count", "like count", "dislike count", "comment count")
    csv_file.writerow(header)

    for tup in tup_in:
        csv_file.writerow(tup)



def get_video_stats(ids):
   
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

def main():

    ids = read_in("charts.csv")
    vids = get_video_stats(ids)
    write_out("youtube.csv", vids)

if __name__ == "__main__":
    main()