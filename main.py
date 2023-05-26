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
                Estimated_Earnings VARCHAR(255)
            )
        """)
        print("Table created successfully")



    #setting the channel name to their corresponding channel id
    TSeries = "UCq-Fj5jknLsUf-MWSy4_brA"
    Cocomelon = "UCbCmjCuTUZos6Inko4u57UQ"
    SetIndia = "UCpEhnqL0y41EpW2TvWAHD7Q"
    MrBeast = "UCX6OQ3DkcsbYNE6H8uQQuVA"
    PewDiePie= "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
    KidsDianaShow="UCk8GzjMOrta8yxDcKfylJYw"
    LikeNastya ="UCJplp5SjeGSdVdwsfb9Q7lQ"
    VladAndNiki = "UCvlE5gTbOvjiolFlEm-c_Ow"
    WWE = "UCJ5v_MCY6GNUBTO8-D3XoAg"
    ZeeMusicCompany = "UCFFbwnve3yF62-tVXkTyHqg"

    cursor.close()
    mydb.close()
    os.system("sudo mysql.server stop")


main()