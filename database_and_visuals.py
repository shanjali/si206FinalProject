import matplotlib.pyplot as plt
import csv
import sqlite3


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

def process_data(filename):
    '''
        Input: filename (Type: String)
		Output: songs, popularity, engagement score (Type:Tuple)

        Processes the 25 items from the database into a tuple of lists.
    '''
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
    '''
        Input: songs, popularity, engagement score (Type:Tuple)
	    Output: nothing

        Creates two horizontal bar charts for the Spotify popularity and the Youtube engagement.
    '''
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
    '''
        Input: filename (Type: String)
	    Output: views, engagement (Type: Tuple)

        Processes the Youtube csv to return a Tuple of the number of views and the engagement per video.
    '''
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
    '''
        Input: views, engagement (Type: Tuple)
	    Output: nothing

        Creates a scatter plot of the engagement vs. number of views per video.
    '''
    x = data[0]
    y = data[1]

    plt.scatter(y, x, c="red", edgecolors="black")
    plt.xlabel("Engagement")
    plt.ylabel("Number of Views")
    plt.title("Engagement vs. Number of Views for Music Videos")
    plt.savefig("engage_vs_views.png")
    plt.show()

scatter(y_data)