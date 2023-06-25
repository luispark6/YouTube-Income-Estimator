import os
#auto starts mysql server so it doesnt need to be started in the terminal
os.system("sudo chown -R _mysql:mysql /usr/local/var/mysql") 
os.system("sudo mysql.server start")
from googleapiclient.discovery import build
import googleapiclient.errors
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def main():
    api_service_name = "youtube"
    api_version = "v3"            
    api_key = "AIzaSyC22GFWR6balVvcOFszYZ9ce0GTGmgff14" #my api key
    youtube = build(api_service_name, api_version, developerKey=api_key)

    #connecting to local host which is my computer
    mydb = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    password = "Leoluis02",
    database = "Youtube_Statistic_Channel"
    )

    #creating object that allows me to execute SQL queries
    cursor = mydb.cursor()
    #will output table named "Information", and we will fetch
    #this output with fetchone
    cursor.execute("SHOW TABLES LIKE 'Information'")

    result = cursor.fetchone()
    
    

    #if result is true(there is data with table name channels),
    #the tabel already exists which means we dont need to create
    #a row of the necessary columns(likes, views, channel name, etc.)
    if result:
        # Table exists, do nothing
        print("")
    else:
        # Create the channels table
        cursor.execute("""
            CREATE TABLE Information (
                id INT NOT NULL AUTO_INCREMENT,
                Channel VARCHAR(255),
                Last_50_Videos_Accumulated_Views VARCHAR(255),
                Time VARCHAR(255),
                Subscribers INT,
                Estimated_Earnings VARCHAR(255),
                PRIMARY KEY (id)
            )
        """)
        print("Table created successfully")


    channelDictionary = {}
    #setting the channel name to their corresponding channel id in a dictionary
    channelDictionary["TSeries"] = []
    channelDictionary["TSeries"].append( "UCq-Fj5jknLsUf-MWSy4_brA")
    channelDictionary["Cocomelon"] = []
    channelDictionary["Cocomelon"].append("UCbCmjCuTUZos6Inko4u57UQ")
    channelDictionary["SetIndia"] = []
    channelDictionary["SetIndia"].append("UCpEhnqL0y41EpW2TvWAHD7Q")
    channelDictionary["MrBeast"] = []
    channelDictionary["MrBeast"].append("UCX6OQ3DkcsbYNE6H8uQQuVA")
    channelDictionary["PewDiePie"] = []
    channelDictionary["PewDiePie"].append("UC-lHJZR3Gqxm24_Vd_AJ5Yw")
    channelDictionary["KidsDianaShow"] = []
    channelDictionary["KidsDianaShow"].append("UCk8GzjMOrta8yxDcKfylJYw")
    channelDictionary["LikeNastya"] = []
    channelDictionary["LikeNastya"].append("UCJplp5SjeGSdVdwsfb9Q7lQ")
    channelDictionary["VladAndNiki"] = []
    channelDictionary["VladAndNiki"].append("UCvlE5gTbOvjiolFlEm-c_Ow")
    channelDictionary["WWE"] = []
    channelDictionary["WWE"].append("UCJ5v_MCY6GNUBTO8-D3XoAg")
    channelDictionary["ZeeMusicCompany"] = []
    channelDictionary["ZeeMusicCompany"].append("UCFFbwnve3yF62-tVXkTyHqg")
    #this will contain all the data we scraped using the youtube api for each youtuber in a list
    channelInfo = []
    for i in channelDictionary:
        #requesting the channel information from each youtube channel from youtube server
        request_channel_info = youtube.channels().list( 
        part="snippet,contentDetails,statistics",
        id=channelDictionary[i]
        )
        #executes the request and feeds the information to response channel
        response_channel = request_channel_info.execute()
        #append the information to channelInfo so we have all the channels information in one list
        channelInfo.append(response_channel)
    #accumulator that will be used to append the playlist id into each youtube channel 
    acc = 0
    for i in channelDictionary:
        #this gets the playlist id which gives us a playlist of the most recent uploads from
        #the channel and gets the statistics of each channel and appends it to the dictionary
        playlistid = channelInfo[acc]['items'][0]["contentDetails"]["relatedPlaylists"]['uploads']
        channelStatistics = channelInfo[acc]["items"][0]['statistics']
        channelDictionary[i].append(playlistid)
        channelDictionary[i].append(channelStatistics)
        acc = acc+1
    

    #this requests the information for the lastest uploads  information from the channel 
    #and we can specify how many recently uploaded videos we want
    for i in channelDictionary:
        request_videos = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=channelDictionary[i][1],
            maxResults=50
        )
        #executes the request
        response_videos = request_videos.execute()
        #this will accumlate all the views of the past 50 videos for each channel
        accumulated_views = 0
        #this will loop through all the video information for the given youtuber and 
        #accumulate the views for each video
        for j in response_videos['items']:
            #requests the video information
            request_video_id = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=j['contentDetails']['videoId'])
            #executes the video information and feeds information into response_video_id
            response_video_id = request_video_id.execute()
            #extract the views of the jth video
            views = response_video_id["items"][0]["statistics"]["viewCount"]
            #add into the accumlator
            accumulated_views = accumulated_views + int(views)
        #creates a dictionary with past 50 video accumulated view count and estimated earnings
        dict = {}
        dict[i+"'s last 50 video data"] = []
        dict[i+"'s last 50 video data"].append(str(accumulated_views))
        #it is estimated that each view earns about 0.018 per view
        #we will convert to an int because cents won't be necessary
        estimatedEarnings = int((accumulated_views * 0.018))
        #seperates the integer with commas for readabiltiy
        estimatedEarnings= f"{estimatedEarnings:,}"
        #append amount into the dictionary
        dict[i+"'s last 50 video data"].append(str(estimatedEarnings) +"$")
        channelDictionary[i].append(dict)

    # Get the current time
    current_time = datetime.now()
    for i in channelDictionary:
        data = [(i, str(channelDictionary[i][3][i+"'s last 50 video data"][0]), current_time, int(channelDictionary[i][2]['subscriberCount']), \
            channelDictionary[i][3][i+"'s last 50 video data"][1])]
        # Insert the data into the table
        sql = "INSERT INTO Information (Channel, Last_50_Videos_Accumulated_Views, Time, Subscribers, Estimated_Earnings) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, data)

    # this will select the table of information we want
    select_query = "SELECT * FROM Information"  
    #this will execute select query
    cursor.execute(select_query)
    # Fetch all rows from the result
    rows = cursor.fetchall()
    #list of channels
    channelList = []
    #list of earnings
    earningsList = []
    #list of subscriber count
    subscriberList = []
    #list of view count
    viewList= []
    #ratio for how much each video they apporixmately make
    ratio = []
    # Print the retrieved data
    for row in rows:
        channelId, channel, view_count, time, subscribers, earnings = row
        print("ID: %d|Channel: %s|Last 50 Videos Views: %s|Time: %s|Subscribers: %d|Earnings \
Past 50 videos: %s" %(channelId, channel, view_count, time, subscribers, earnings) )
        print("")
        channelList.append(channel)
        earningsList.append(int(view_count)*0.018)
        subscriberList.append(int(subscribers))
        viewList.append(int(view_count))
        ratio.append(int(int(view_count)*0.018) //50)
    graphType = input("1: Channel and View Count Graph \n2: Channel and Subsrcriber Count Graph\n3: Channel and Earnings Graph\n4: Channel and Video/Earnings Ratio Graph\n5: Quit\n")
    while graphType != '1' and graphType != '2' and graphType != '3' and graphType != '4' and graphType != '5':
        print("Please enter 1, 2, 3, 4 or 5")
        graphType = input("1: Channel and View Count Graph \n2: Channel and Subsrcriber Count Graph\n3: Channel and Earnings Graph\n4: Channel and Video/Earnings Ratio Graph\n5: Quit\n")
    while True:
        if graphType =="1":
            plt.bar(channelList, viewList)
            plt.xlabel("Channels")
            plt.ylabel("Views")
            plt.ylim(0, 15000000000)
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.show()
        elif graphType =='2':
            plt.bar(channelList, subscriberList)
            plt.xlabel("Channels")
            plt.ylabel("Subscribers")
            plt.ylim(0, 300000000)
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.show()
        elif graphType =='3':
            plt.bar(channelList, earningsList)
            plt.xlabel("Channels")
            plt.ylabel("Earnings")
            plt.ylim(0, 150000000)
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.show()
        elif graphType =='4':
            plt.bar(channelList, ratio)
            plt.xlabel("Channels")
            plt.ylabel("Video/Earnings Ratio")
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.show()
        elif graphType == '5':
            break
        graphType = input("1: Channel and View Count Graph \n2: Channel and Subsrcriber Count Graph\n3: Channel and Earnings Graph\n4: Channel and Video/Earnings Ratio Graph\n5: Quit\n")
        while graphType != '1' and graphType != '2' and graphType != '3' and graphType != '4' and graphType != '5':
            print("Please enter 1, 2, 3, 4 or 5")
            graphType = input("1: Channel and View Count Graph \n2: Channel and Subsrcriber Count Graph\n3: Channel and Earnings Graph\n4: Channel and Video/Earnings Ratio Graph\n5: Quit\n")
        

    #closing and stopping mysql database server
    cursor.close()
    mydb.close()
    os.system("sudo mysql.server stop")


main()