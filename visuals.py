import matplotlib.pyplot as plt
import numpy as np
import csv
import math

def process_data(filename):
    songs = []
    popularity = []
    engagement = []

    inFile = open(filename, "r")
    csv_file = csv.reader(inFile)

    headers = next(csv_file)

    for row in csv_file:
        songs.append(row[0])
        popularity.append(float(row[1]))
        engagement.append(float(row[2]))

    return (songs, popularity, engagement)

processed = process_data("Spotify_And_Youtube_DB.csv")

def double_bar(data):
    X = data[0]
    Y_pop = data[1]
    Y_eng = data[2]

    fig, ax = plt.subplots(1, 2,
                       constrained_layout = True)
    fig.set_figwidth(15)
    fig.set_figheight(5)

    ax[0,] = plt.subplot(121)
    ax[0].barh(X, Y_pop, align='center', color='green', edgecolor='black')
    ax[0].title.set_text("Spotify Popularity")
  
    ax[1] = plt.subplot(122, sharey=ax[0])
    ax[1].barh(X, Y_eng, align='center', color='red', edgecolor='black')
    ax[1].title.set_text("Youtube Engagement")
        
    plt.savefig("double_bar.png")
    plt.show()  
    plt.close()

double_bar(processed)

def process_youtube(filename):
    engagement = []
    views = []

    inFile = open(filename, "r")
    csv_file = csv.reader(inFile)

    headers = next(csv_file)

    for row in csv_file:
        view = float(row[2])
        likes = float(row[3])
        comments = float(row[5])
        engage = ((likes + comments) / view) * 100
        views.append(view)
        engagement.append(engage)

    return (views, engagement)

y_data = process_youtube("youtube.csv")

def scatter(data):
    x = data[0]
    y = data[1]

    plt.scatter(y, x, c="red", edgecolors="black")
    plt.xlabel("Engagement")
    plt.ylabel("Number of Views")
    plt.title("Engagement vs. Number of Views for Music Videos")
    plt.savefig("engage_vs_views.png")
    plt.show()

scatter(y_data)