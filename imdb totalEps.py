import sqlite3
import csv

#define connection to db file
conn=sqlite3.connect("mydtb.db")
#print(conn.total_changes)
#define cursor
cursor=conn.cursor()

#calculating total number of episodes for each title
with open("title.episode.tsv") as epFile:
    header=next(epFile)
    eps=csv.reader(epFile, delimiter='\t')
    for row in eps:
        parentTitleID=row[1]
        #count occurence of parent title id in dtbTitles
        cursor.execute("""SELECT
        COUNT(*) FROM tblTitles
        WHERE (titleID==?)""",[parentTitleID])
        parentTitle=cursor.fetchall()[0]
        #if a parent title is found then it has multiple eps
        if parentTitle[0]==1:
            #find num eps already saved in dtb
            cursor.execute("""SELECT
            totalEpisodes FROM tblTitles
            WHERE (titleID==?)""",[parentTitleID])
            numEps=cursor.fetchall()[0][0]
            numEps=numEps+1
            #update title to increase ep number by 1
            cursor.execute("""UPDATE tblTitles
            SET totalEpisodes=?
            WHERE (titleID==?)""",[numEps,parentTitleID])
            conn.commit()
            print("added")
         
print("for loop 2 complete")

#extracting titleID and mediaType of all titles in dtb
cursor.execute("""SELECT titleID, mediaType FROM tblTitles""")
output=cursor.fetchall()
for i in range(0,len(output)):
    titleID=output[i][0]
    mediaType=output[i][1]
    #changing mediaType to "show" 
    if mediaType=="tvSeries" or mediaType=="tvMiniSeries":
        cursor.execute("""UPDATE tblTitles SET mediaType="show"
        WHERE (titleID==?)""",[titleID])
        conn.commit()
        print("show updated")
    #changing mediaType to "movie"
    #setting total eps to 1 as they do are not a series
    else:
        cursor.execute("""UPDATE tblTitles SET
        totalEpisodes=1,mediaType="movie"
        WHERE (titleID==?)""",[titleID])
        conn.commit()
        print("movie updated")

cursor.execute("""SELECT titleID,totalEpisodes
                FROM tblTitles""")
output=cursor.fetchall()
for i in range(0,len(output)):
    titleID=output[i][0]
    totalEps=output[i][1]
    #if show has unknown number of eps
    #set to "?"
    if totalEps==0:
        cursor.execute("""UPDATE tblTitles
        SET totalEpisodes="?"
        WHERE(titleID==?)""",[titleID])
        conn.commit()
        print("total eps updated")
        
