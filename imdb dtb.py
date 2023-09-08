import sqlite3
import csv

#define connection to db file
conn=sqlite3.connect("mydtb.db")
#print(conn.total_changes)
#define cursor
cursor=conn.cursor()

#no titles saves in tblTiles at start
numTitles=0

#read titles file with csv library
#latin encoding allows for more characters
with open("title.basics.tsv", encoding='Latin1') as basicsFile:
    #skip over headers
    header=next(basicsFile)
    #lines are separated by \t in tsv file
    basics=csv.reader(basicsFile, delimiter='\t')
    #saves each title to dtb one at a time
    i=0
    for row in basics:
        if i<20000:
            titleID=row[0]
            mediaType=row[1]
            primaryTitle=row[2]
            originalTitle=row[3]
            yearReleased=row[5]
            genres=row[8]
            totalEpisodes=int(0) #temporary value
            #excludes tv episode and video entries 
            if mediaType!="tvEpisode" and mediaType!="video":
                try:
                    if yearReleased=="\\N" or int(yearReleased)>1989:
                        cursor.execute("""INSERT INTO tblTitles
                        VALUES (?,?,?,?,?,?,?)""",
                        [titleID,primaryTitle,originalTitle,mediaType,
                         genres,yearReleased,totalEpisodes])
                        conn.commit()
                        numTitles+=1
                        print(titleID)
                        i=i+1
                except:
                    print("record already exists")
        else:
            print("complete")
            print(numTitles)
            basicsFile.close()

#media types - short, movie, tvSeries, tvEpisode,
#video, tvMovie, tvMiniSeries

#video and tvEpisode removed
#short saved as movie
