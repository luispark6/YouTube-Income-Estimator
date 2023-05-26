import os
#auto starts mysql server so it doesnt need to be started in the terminal
os.system("sudo chown -R _mysql:mysql /usr/local/var/mysql") 
os.system("sudo mysql.server start")
from googleapiclient.discovery import build
import googleapiclient.errors
import mysql.connector

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
    database = "Youtube_Income_Estimator"
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
        print("Table already exists")
    else:
        # Create the channels table
        cursor.execute("""
            CREATE TABLE Information (
                id INT NOT NULL AUTO_INCREMENT,
                Channel VARCHAR(255),
                Last_50_Videos_Accumlated_Views INT,
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
        #this gets the upload id which gives us a playlist id of the most recent uploads from
        #the channel and gets the statistics of each channel and appends it to the dictionary
        playlistid = channelInfo[acc]['items'][0]["contentDetails"]["relatedPlaylists"]['uploads']
        channelStatistics = channelInfo[acc]["items"][0]['statistics']

        channelDictionary[i].append(playlistid)
        channelDictionary[i].append(channelStatistics)

        acc = acc+1
    print(channelDictionary)
    



    
    

    cursor.close()
    mydb.close()
    os.system("sudo mysql.server stop")


main()