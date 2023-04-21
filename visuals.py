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
  
    ax[1] = plt.subplot(122, sharey=ax[0])
    ax[1].barh(X, Y_eng, align='center', color='red', edgecolor='black')
        
    plt.savefig("double_bar.png")
    plt.show()  
    plt.close()

double_bar(processed)

#plt.bar(x_axis - 0.2, Y_pop, 0.4, label = 'Spotify Popularity')
 #   plt.bar(x_axis + 0.2, Y_eng, 0.4, label = 'Youtube Engagement')
  
  #  plt.xticks(x_axis + 0.25/2, X)
   # plt.xlabel("Songs")
    #plt.ylabel("Metric")
    #plt.title("Spotify Popularity vs. Youtube Engagement")
    #plt.legend()
    #plt.show()