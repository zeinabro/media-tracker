import sqlite3

#define connection to db file
conn=sqlite3.connect("mydtb.db")
print(conn.total_changes)
#define cursor
cursor=conn.cursor()

cursor.execute("PRAGMA foreign_keys")
cursor.fetchone()

#creates tblListNames table
cursor.execute("""CREATE TABLE IF NOT EXISTS tblListNames
                (listID TEXT NOT NULL PRIMARY KEY,
                listName TEXT NOT NULL
                )""")
conn.commit()
print("tblListNames created in mydtb.db")

try:
    listNames=[('C','Currently Watching'),('O','On Hold'),
               ('P','Planning'),('D','Dropped')]
    cursor.execute("""INSERT INTO tblListNames VALUES (?,?)""",
                   [listNames[0][0],listNames[0][1]])
    cursor.execute("""INSERT INTO tblListNames VALUES (?,?)""",
                   [listNames[1][0],listNames[1][1]])
    cursor.execute("""INSERT INTO tblListNames VALUES (?,?)""",
                   [listNames[2][0],listNames[2][1]])
    cursor.execute("""INSERT INTO tblListNames VALUES (?,?)""",
                   [listNames[3][0],listNames[3][1]])
except:
    print("tblListNames already exists")


#creates tblUsers table
sqlCommand="""
    CREATE TABLE IF NOT EXISTS tblUsers
    (userID INTEGER NOT NULL PRIMARY KEY,
    username TEXT NOT NULL, 
    password TEXT NOT NULL
    )"""

cursor.execute(sqlCommand)
print("tblUsers created in mydtb.db")

conn.commit()

#creates tblTitles table
sqlCommand2=("""
    CREATE TABLE IF NOT EXISTS tblTitles
    (titleID TEXT NOT NULL PRIMARY KEY,
    primaryTitle TEXT NOT NULL,
    originalTitle TEXT NOT NULL,
    mediaType TEXT NOT NULL,
    genres TEXT NOT NULL,
    yearReleased DATE NOT NULL,
    totalEpisodes INTEGER NULL
    )""")

cursor.execute(sqlCommand2)
print("tblTitles created in mydtb.db")

conn.commit()

#creates tblLists table
#defines foreign keys to link the tables
#in a one to many relationship

sqlCommand3=("""
    CREATE TABLE IF NOT EXISTS tblLists
    (episodesWatched INTEGER NULL,
    rating INTEGER NULL,
    userID INTEGER NOT NULL,
    titleID TEXT NOT NULL,
    listID TEXT NOT NULL,
    CONSTRAINT fk_dtbUsers
        FOREIGN KEY(userID)
        REFERENCES tblUsers(userID)
        FOREIGN KEY (titleID)
        REFERENCES tblTitles(titleID)
        FOREIGN KEY (listID)
        REFERENCES tblListNames(listID)
    )""")

cursor.execute(sqlCommand3)
print("tblLists created in mydtb.db")

conn.commit()
conn.close()



