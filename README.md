# si206FinalProject

# How to Use:

Download “charts.csv”
Open “SI206FinalProject.py”
    Run 	early = get_track_ids(read_in_top_songs())
          get_popularity_score(early)
		Run 	create_Spotify_db()
		Run 	create_Youtube_db()
		Run   create_text_file_from_DB()
Open “youtubeapi.py”
		Run	  main()
			    ids = read_in("charts.csv")
    	    vids = get_video_stats(ids)
    		  write_out("youtube.csv", vids)
Open “visuals.py”
		Run	  processed = process_data("Spotify_And_Youtube_DB.csv")
			    double_bar(processed)
		Run 	y_data = process_youtube("youtube.csv")
			    scatter(y_data)
