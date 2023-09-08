#importing tkinter module 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

#creates connection to the sql database
conn=sqlite3.connect("mydtb.db")
#creates cursor to query the database 
cursor=conn.cursor()

#font settings for quicker access
f=("Arial",12)
smallf=("Arial",10)

#creating the app 
class myApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #creating a container to hold the frames
        container=tk.Frame(self)
        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #frames to empty dictionary
        self.frames={}
        #iterating through the different user interfaces
        #the other pages are created when they are called
        for F in (signUp,logIn):
            frame = F(container, self)
            #adding each frame of the user interface
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="")
        #first frame shown is sign up page
        self.showFrame(signUp,container)

    #function to show frames
    def showFrame(self,cont,container):
        #if frame is not initialised, it is created when called
        #this allows the frames to be closed and reopened
        #with updated data
        if cont not in self.frames:
            self.frame=cont(container,self)
            self.frame.grid(row=0,column=0,sticky="")
        else:
            self.frame=self.frames[cont]
        #raise frame to the top
        self.frame.tkraise()

    #function to close frames to allow other frames to be displayed
    def closeFrame(self,frame):
        frame=self.frame
        self.frame.destroy()
        

#sign up class frame
class signUp(tk.Frame):
    def __init__(self, parent, controller):
        #sign up user interface
        tk.Frame.__init__(self, parent)
        self.controller=controller
        #parent acts as instance of container
        #to be passed as a parameter when displaying frames
        #that were not created in class myApp
        self.parent=parent
        #labels
        tk.Label(self,text="Welcome",bg='yellow',width=17,font=f
              ).grid(row=0,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self,text="Create an account:",bg='pink',width=20,font=f
              ).grid(row=1,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self,text="Username: ",bg='light green',width=15,font=f
              ).grid(row=2,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self,text="Password: ",bg='light green',width=15,font=f
              ).grid(row=3,column=0,padx=10,pady=5,sticky='news')
        #username entry field
        self.username=tk.Entry(self,width=15,bg="white",font=f)
        self.username.grid(row=2,column=1,padx=10,pady=5,sticky='news')
        #cursor is set on username entry field
        self.username.focus_set()
        #password entry field
        self.password=tk.Entry(self,width=15,bg="white",show="*",font=f)
        self.password.grid(row=3,column=1,padx=10,pady=5,sticky='news')
        #submit button
        submit=tk.Button(self,text="Submit",width=8,
            command=lambda:self.submit(controller,parent),font=f
            ).grid(row=4,column=0,padx=10,pady=5,sticky='news')
        #clear button
        clear=tk.Button(self,text="Clear",width=8,
            command=lambda:self.clear(),font=f
            ).grid(row=4,column=1,padx=10,pady=5,sticky='news')
        #button to go to log in page
        logInButton=tk.Button(self,text="Log in page",width=20,
            command=lambda:controller.showFrame(logIn,parent),font=f
            ).grid(row=5,column=1,padx=10,pady=5,sticky='news')
        
    #clear button function
    #self allows the other variables in this class to be used
    #without passing in each variable
    def clear(self):
        self.username.delete(0,"end")
        self.password.delete(0,"end")
        self.username.focus_set()

    #submit button function
    def submit(self,controller,parent):
        #retrieve inputs from user
        userCheck=self.username.get()
        passCheck=self.password.get()
        validUser=False
        validPass=False
        valid=False
        #presence and length check
        if userCheck=="" or len(userCheck)>21:
            messagebox.showinfo("My App",
            "Enter a username with 1-20 characters.")#pop up message
            validUser=False
        else:
            validUser=True
        if passCheck=="" or (len(passCheck)<8 or len(passCheck)>21):
            messagebox.showinfo("My App",
            "Enter a password with 8-20 characters.")
            validPass=False
        else:
            validPass=True
        #counts users in dtb with same username
        check=cursor.execute("""
            SELECT COUNT(1) FROM tblUsers WHERE
            username==(?)""",[userCheck])
        result=cursor.fetchone()
        #if 0 there are no existing users with same username
        #otherwise the username is already taken
        #if the username is taken, the value will always be 1
        if result[0]==1:
            messagebox.showinfo(
        "My App",
        "This username is already taken, please enter a different one.")
            valid=False
        else:
            valid=True
        #if user and pass are both valid
        if validUser==True and validPass==True and valid==True:
            #count number of users in dtb
            cursor.execute("""
            SELECT COUNT(*) FROM tblUsers""")
            numUsers=cursor.fetchone()[0]
            #the userID correlates to the number of users 
            self.userID=numUsers+1
            #add new user to dtb
            addUser=cursor.execute("""
            INSERT INTO tblUsers VALUES(?,?,?)""",
            [self.userID,userCheck,passCheck])
            conn.commit()
            #profile frame is created and displayed
            controller.showFrame(profile,parent)
            return self.userID
        
    #to pass userID to other class frames
    def retrieveUserID(self):
        return self.userID

#log in class frame
class logIn(tk.Frame):
    def __init__(self, parent, controller):
        #log in page interface
        tk.Frame.__init__(self, parent)
        self.parent=parent
        self.controller=controller
        #labels and entry fields
        tk.Label(self,text="Welcome",bg='yellow',width=17,font=f
              ).grid(row=0,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self, text="Log into an account:",bg='pink',width=20,font=f
              ).grid(row=1,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self, text="Username: ",bg='light green',width=15,font=f
              ).grid(row=2,column=0,padx=10,pady=5,sticky='news')
        tk.Label(self,text="Password: ",bg='light green',width=15,font=f
              ).grid(row=3,column=0,padx=10,pady=5,sticky='news') 
        self.username=tk.Entry(self, width=15, bg="white", font=f)
        self.username.grid(row=2,column=1,padx=10,pady=5,sticky='news')
        #cursor is set on username entry field
        self.username.focus_set()
        self.password=tk.Entry(self, width=15, bg="white", show="*", font=f)
        self.password.grid(row=3,column=1,padx=10,pady=5,sticky='news')
        #submit button
        submit=tk.Button(self,text="Submit",width=8,
                command=lambda:self.submit(controller,parent),font=f
                ).grid(row=4,column=0,padx=10,pady=5,sticky='news')
        #clear button
        clear=tk.Button(self,text="Clear",width=8,
                command=lambda:self.clear(), font=f
                ).grid(row=4,column=1,padx=10,pady=5,sticky='news')
        #button to take user to sign in page
        signUpButton=tk.Button(self,text="Sign up page",width=20,
                command=lambda:controller.showFrame(signUp,parent),font=f
                ).grid(row=5,column=1,padx=10,pady=5,sticky='news')
        
    #clear button function
    def clear(self):
        self.username.delete(0,"end")
        self.password.delete(0,"end")
        self.username.focus_set()
        
    #submit button function
    def submit(self,controller,parent):
        #retrieve inputs from user
        userCheck=self.username.get()
        passCheck=self.password.get()
        #check details against database
        valid=False
        #check if user exists in database
        check=cursor.execute("""SELECT COUNT(1) FROM tblUsers
        WHERE username==?""",[userCheck])
        numUsers=cursor.fetchall()[0]
        #result is num of users found in dtb with this username
        #if 1, user exists
        if numUsers[0]==1:
            valid=True
            check2=cursor.execute("""
            SELECT * FROM tblUsers
            WHERE username==?""",[userCheck])
            result=cursor.fetchone()
            self.userID=result[0]
            user=result[1]
            passw=result[2]
            if user==userCheck and passw==passCheck:
                #profile frame is raised
                controller.showFrame(profile,parent)
            else:
                messagebox.showinfo("My App",
                "Username or password is incorrect")
        #if 0, username is incorrect/doesn't exist
        #this also applies if the entry fields are empty
        if numUsers[0]==0:
           messagebox.showinfo("My App",
           "Username or password is incorrect")
           valid=False
           
    #to pass userID to other class frames
    def retrieveUserID(self):
        return self.userID

#profile class frame
class profile(tk.Frame):
    def __init__(self, parent, controller):
        #profile page interface
        tk.Frame.__init__(self, parent)
        self.parent=parent
        self.controller=controller
        #                       menu of options
        #frame created for menu of options
        menuFrame=tk.Frame(self,bd=2,padx=10,pady=5)
        menuFrame.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
        #button to search by genre
        genres=tk.Button(menuFrame,text="Genres",width=15,
            #command=searchByGenre,
            bg="light blue",font=f
            ).grid(row=0,column=0,padx=5,pady=5)
        #button to search by year of release
        yearReleased=tk.Button(menuFrame,text="Years released",width=15,
            #command=searchByYear,
            bg="light blue",font=f
            ).grid(row=0,column=1,padx=5,pady=5)
        #button to log a title using search bar
        logTitle=tk.Button(menuFrame,text="Log a title",width=15,
            command=lambda:self.openSearch(controller,parent),
            bg="light yellow",font=f
            ).grid(row=0,column=2,padx=5,pady=5)
        #tells user this is their profile
        profileButton=tk.Button(menuFrame,text="Profile",bg="light pink",
            command=lambda:controller.showFrame(profile,parent),
            width=15,font=f
            ).grid(row=0,column=3,padx=5,pady=5)
        
        #extract list names and list IDs from mydtb.db
        cursor.execute("""SELECT * FROM tblListNames""")
        lists=cursor.fetchall()
        
        #pass in userID from either signUp or logIn
        #signUp is the first frame shown so it is first
        try:
            self.userID=controller.frames[signUp].retrieveUserID()
        #if signUp does not return userID, use logIn
        except:
            self.userID=controller.frames[logIn].retrieveUserID()
        #close the frames after retrieving userID
        controller.closeFrame(signUp)
        controller.closeFrame(logIn)
        
        #                       shows section
        #canvas frame of shows lists
        showCanvasFrame=tk.Frame(self,bd=2)
        showCanvasFrame.grid(row=1,column=0,pady=10,padx=10)
        showCanvasFrame.grid_rowconfigure(0, weight=1)
        showCanvasFrame.grid_columnconfigure(0, weight=1)
        #canvas embedded in canvas frame
        showCanvas=tk.Canvas(showCanvasFrame,bg="light blue",
                      bd=0,highlightthickness=0, relief='ridge')
        #vertical scrollbar for shows
        showsScrollbar=tk.Scrollbar(showCanvasFrame,orient="vertical")
        showsScrollbar.grid(column=1,sticky="ns")
        showsScrollbar.config(command=showCanvas.yview)
        #add scrollbar to canvas
        showCanvas.config(yscrollcommand=showsScrollbar.set)
        showCanvas.grid(row=0,column=0)
        #frame displaying the shows section
        showsFrame=tk.Frame(showCanvas,bd=1,padx=10,pady=5,bg="light blue")
        showCanvas.create_window((0,0),window=showsFrame)
        #label of shows section
        tk.Label(showsFrame,text="Shows",width=20,bg="light pink",font=f
            ).grid(row=0,column=0,padx=5,pady=5)
        #starts at first row of the frame
        self.listRow=1
        #to display the shows list
        self.frame=showsFrame
        self.mediaType="show"
        for i in range (0,5):
            self.listName=lists[i][1]
            self.listID=lists[i][0]
            #calls function to display list labels
            #last row used is returned
            self.listRow=self.listLabels(
                self.listName,self.listRow,self.frame)
            #calls function to display the list items
            #new row after function displays all titles
            self.listRow=self.listItems(
                self.userID,self.listID,self.listRow,
                self.frame,self.mediaType,parent,controller)
            
        #update measurements after widgets have been places
        #and set scrollregion to ensure all of canvas is accessible
        showsFrame.update_idletasks()
        showCanvas.config(width=650,height=250)
        showCanvas.config(scrollregion=showCanvas.bbox("all"))
        
        #                        movies section
        moviesCanvasFrame=tk.Frame(self,bd=2)
        moviesCanvasFrame.grid(row=2,column=0,pady=10,padx=10)
        moviesCanvasFrame.grid_rowconfigure(0, weight=1)
        moviesCanvasFrame.grid_columnconfigure(0, weight=1)
        #canvas embedded in canvas frame
        moviesCanvas=tk.Canvas(moviesCanvasFrame,bg="light blue",
                      bd=0,highlightthickness=0, relief='ridge')
        #vertical scrollbar for movies
        moviesScrollbar=tk.Scrollbar(moviesCanvasFrame,orient="vertical")
        moviesScrollbar.grid(column=1,sticky="ns")
        moviesScrollbar.config(command=moviesCanvas.yview)
        #add scrollbar to canvas
        moviesCanvas.config(yscrollcommand=moviesScrollbar.set)
        moviesCanvas.grid(row=0,column=0)
        #frame displaying the movies section
        moviesFrame=tk.Frame(moviesCanvas,bd=2,padx=10,pady=5,bg="light blue")
        #moviesFrame.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
        moviesCanvas.create_window((0,0),window=moviesFrame,anchor="nw")
        #label of movies section
        tk.Label(moviesFrame,text="Movies",width=20,bg="light pink",font=f
            ).grid(row=0,column=0,padx=5,pady=5)
        #starts at first row of the frame
        self.listRow=1
        #to display the movies list
        self.frame=moviesFrame
        self.mediaType="movie"
        #find number of show entries
        cursor.execute("""SELECT COUNT(*) FROM tblLists
        WHERE (userID==?)""",[self.userID])
        self.numEntries=cursor.fetchone()[0]
        #to display the shows list
        self.frame=moviesFrame
        self.mediaType="movie"
        for i in range (0,5):
            self.listName=lists[i][1]
            self.listID=lists[i][0]
            #calls function to display list labels
            #last row used is returned
            self.listRow=self.listLabels(
                self.listName,self.listRow,self.frame)
            #calls function to display the list items
            #new row after function displays all titles
            self.listRow=self.listItems(
                self.userID,self.listID,self.listRow,
                self.frame,self.mediaType,parent,controller)

        moviesFrame.update_idletasks()
        moviesCanvas.config(width=650,height=250)
        moviesCanvas.config(scrollregion=moviesCanvas.bbox("all"))

    #prints out appropriate labels for each list
    #name of list, current row and frame is passed in as parameters
    def listLabels(self,listName,listRow,frame):
        listRow=listRow+1
        #label of list, according to value passed in
        tk.Label(frame,text=str(listName),width=20,font=f
            ).grid(row=listRow,column=0,padx=5,pady=5)
        #directs user on how to edit the list items
        tk.Label(frame,text="Click the title to edit",width=20,font=f
            ).grid(row=listRow,column=2,padx=5,pady=5,sticky='news')
        #title label
        tk.Label(frame,text="Title",width=20,font=smallf,bg="light blue"
            ).grid(row=listRow+1,column=0,padx=5,pady=5,sticky='news')
        #eps watched label
        tk.Label(frame,text="Episodes Watched",width=20,font=smallf,
                 bg="light blue"
        ).grid(row=listRow+1,column=1,padx=5,pady=5,sticky='news')
        #rating label
        tk.Label(frame,text="Rating",width=20,font=smallf,
                 bg="light blue"
        ).grid(row=listRow+1,column=2,padx=5,pady=5,sticky='news')
        return int(listRow)

    #function to display list items of each list
    #passes current row and name of frame as parameters
    #add database info once connected
    def listItems(self,userID,listID,listRow,frame,mediaType
                  ,parent,controller):
        listRow=listRow+2
        column=0
        #counts the num of titles the user has
        cursor.execute("""
            SELECT COUNT(*) FROM tblLists WHERE
            (userID==? AND listID==?)""",[self.userID,listID])
        numTitles=cursor.fetchone()[0]
        for i in range(0,numTitles):
            sql=cursor.execute("""
            SELECT * FROM tblLists WHERE (userID==?
            AND listID==?)""",[self.userID,listID])
            userLists=cursor.fetchall()
            episodesWatched=userLists[i][0]
            rating=userLists[i][1]
            titleID=userLists[i][3]
            sql=cursor.execute("""
            SELECT * FROM tblTitles
            WHERE (titleID==? AND mediaType==?)""",
            [titleID,mediaType])
            titles=cursor.fetchall()
            #array may be empty if there are no entries in this list
            for x in range (0,len(titles)):
                titleID=titles[x][0]
                titleName=titles[x][1]
                mediaType=titles[x][3]
                genres=titles[x][4]
                yearReleased=titles[x][5]
                totalEpisodes=titles[x][6]
                #button of title name
                titleName=tk.Button(frame,text=str(titleName),
                    width=20,bg="light yellow",font=f,
                    #can edit list item by clicking title
                    #calls function in listEditor class to pass titleID
                    command=lambda t=str(titleID):
                            listEditor.openListEditor
                                    (self,t,controller,parent)
                    ).grid(row=listRow,column=0,padx=5,
                           pady=5,sticky='news')
                #number of episodes label
                tk.Label(frame,width=20,font=f,
                    text=str(episodesWatched)+"/"+str(totalEpisodes)
                    ).grid(row=listRow,column=1,padx=5,
                           pady=5,sticky='news')
                #rating label
                tk.Label(frame,text=str(rating)+"/5",width=20,font=f
                    ).grid(row=listRow,column=2,padx=5,
                           pady=5,sticky='news')
                #next title, to the row underneath
                listRow=listRow+1
        return int(listRow)

    def retrieveUserID(self):
        return self.userID

    #close profile and open search page
    def openSearch(self,controller,parent):
        controller.closeFrame(profile)
        controller.showFrame(searchTitles,parent)
    
#frame to search for and log titles
class searchTitles(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="light yellow")
        self.parent=parent
        self.controller=controller
        #search bar and button in separate frame
        searchFrame=tk.Frame(self,bd=2,padx=10,pady=5,bg="light yellow")
        searchFrame.grid(row=0,column=0,padx=10,pady=10,
                         columnspan=2)
        self.searchEntry=tk.Entry(searchFrame,width=30,bg="white",font=f)
        self.searchEntry.grid(row=0,column=0,padx=10,pady=10)
        self.searchEntry.focus_set()
        
        #frame for the results section canvas
        canvasFrame=tk.Frame(self,bd=2)
        canvasFrame.grid(row=1,column=0,padx=10,pady=10)
        canvasFrame.grid_rowconfigure(0, weight=1)
        canvasFrame.grid_columnconfigure(0, weight=1)
        #search results canvas
        resultsCanvas=tk.Canvas(canvasFrame,bg="light blue",
                        bd=0,highlightthickness=0, relief='ridge')
        #vertical scrollbar for search results
        scrollbar=tk.Scrollbar(canvasFrame,orient="vertical")
        scrollbar.grid(column=1,sticky="ns")
        scrollbar.config(command=resultsCanvas.yview)
        #add scrollbar to canvas
        resultsCanvas.config(yscrollcommand=scrollbar.set)
        resultsCanvas.grid(row=0,column=0)
        #frame displaying the shows section
        resultsFrame=tk.Frame(resultsCanvas,bd=2,padx=10,pady=5,
                              bg="light blue")
        resultsCanvas.create_window((0,0),window=resultsFrame,anchor="nw")
        
        self.frame=resultsFrame
        self.resultsRow=1
        
        #search button calls function to display results in frame
        searchButton=tk.Button(searchFrame,text="Search",bg="lavender"
                ,command=lambda:self.search(self.frame,self.resultsRow,
                        parent,controller),font=f
                ).grid(row=0,column=1,padx=5,pady=5,sticky='news')

        buttonFrame=tk.Frame(self,bg="light yellow")
        buttonFrame.grid(row=2,column=0,padx=5,pady=5)
        #back to profile button
        profileButton=tk.Button(buttonFrame,text="Back to profile",
                bg="light green",font=f,width=15,
                command=lambda:self.backToProfile
                        (controller,parent))
        profileButton.grid(row=0,column=1,pady=10,padx=10,sticky='news')
        #button to clear search results
        clearButton=tk.Button(buttonFrame,text="Clear results",
                bg="light green",font=f,width=15,
                command=lambda:self.clearResults(self.frame))
        clearButton.grid(row=0,column=0,pady=10,padx=10,sticky='news')

        resultsFrame.update_idletasks()
        resultsCanvas.config(width=650,height=250)
        resultsCanvas.config(scrollregion=resultsCanvas.bbox("all"))

    #clears search results by destroying widgets
    #in resultsFrame
    def clearResults(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
        #clear search entry field and set cursor
        self.searchEntry.delete(0,"end")
        self.searchEntry.focus_set()
        
    def search(self,frame,resultsRow,parent,controller):
        #for each search, results start at top
        resultsRow+=2
        column=0
        searchInput=self.searchEntry.get()
        #compare search input to database titles
        cursor.execute("""SELECT * FROM tblTitles WHERE
            ((primaryTitle LIKE ?)OR (originalTitle LIKE ?))""",
                       [searchInput,searchInput])
        results=cursor.fetchall()
        #if matching titles have been found
        if results!=[]:
            #each result is displayed on its own row
            for i in range (0,len(results)):
                titleID=results[i][0]
                titleName=results[i][1]
                mediaType=results[i][3]
                genres=results[i][4]
                yearReleased=results[i][5]
                totalEpisodes=results[i][6]
                #log button takes user to list editor function
                logButton=tk.Button(frame,font=f,text="Log into profile",
                    bg="light pink",command=lambda t=str(titleID):
                    listEditor.openListEditor(self,t,controller,parent))
                logButton.grid(row=resultsRow,column=0,
                        padx=5,pady=5)
                #title info in label
                text=("Title: "+str(titleName)+"\nYear Released: "
                    +str(yearReleased)+"\nGenres: "+str(genres)
                      +"\nTotal Episodes: "+str(totalEpisodes))
                titleInfo=tk.Label(frame,text=text,font=f,width=40,
                    bg="light blue"
                    ).grid(row=resultsRow,column=1,padx=5,pady=5)
                #next row
                resultsRow+=1
        else:
            messagebox.showinfo("My App",
            "No matching titles were found.")
            
            
    #close search, open profile
    def backToProfile(self,controller,parent):
        controller.closeFrame(searchTitles)
        controller.showFrame(profile,parent)
        

#list editor frame class
class listEditor(tk.Frame):
    
    #to retrieve titleID from button in profile lists
    def openListEditor(self,t,controller,parent):
        global titleID
        titleID=t
        controller.showFrame(listEditor,parent)
        return titleID
            
    #list editor interface
    def __init__(self, parent, controller):
        #close profile page
        controller.closeFrame(profile)
        tk.Frame.__init__(self, parent)
        logFrame=tk.Frame(self,bd=2,padx=10,pady=10,bg="light yellow")
        logFrame.grid(row=1,column=0,columnspan=3,padx=0,pady=0)
        self.parent=parent
        self.controller=controller
        
        #global titleID from openListEditor function
        self.titleID=titleID
        #userID retrieved from profile
        self.userID=profile(parent,controller).retrieveUserID()

        #extract info about the title
        cursor.execute("""SELECT * FROM tblTitles
        WHERE (titleID==?)""",[self.titleID])
        titleInfo=cursor.fetchall()
        self.primaryTitle=titleInfo[0][1]
        self.originalTitle=titleInfo[0][2]
        self.mediaType=titleInfo[0][3]
        self.genres=titleInfo[0][4]
        self.yearReleased=titleInfo[0][5]
        self.totalEpisodes=titleInfo[0][6]
        #extract user's info about the list entry of this title
        cursor.execute("""SELECT * FROM tblLists
        WHERE (userID==? AND titleID==?)""",[self.userID,self.titleID])
        entryInfo=cursor.fetchall()
        #if user has logged the title before,
        #the info needed is extracted
        if entryInfo!=[]:
            self.epsWatched=entryInfo[0][0]
            self.rating=entryInfo[0][1]
            self.listID=entryInfo[0][4]
            cursor.execute("""SELECT listName FROM tblListNames
                            WHERE (listID==?)""",[self.listID])
            self.listName=cursor.fetchall()[0][0]
        #if the user has not already logged the title,
        #the output will be empty
        #generic info for the user to change
        else:
            self.epsWatched="-"
            self.rating="-"
            self.listName="Choose a list"
        #labels, buttons and dropdown menus
        #title of show/movie
        tk.Label(logFrame,text=str(self.primaryTitle)+" ("+
                 str(self.yearReleased)+")",
              width=30,bg="light blue",font=f,
              ).grid(row=0,column=1,padx=1,pady=5)
        tk.Label(logFrame,text="List:",width=15,bg="light pink",
              font=smallf).grid(row=1,column=0,padx=1,pady=5)
        tk.Label(logFrame,text="Episodes watched:",width=15,bg="light pink",
              font=smallf).grid(row=1,column=1,padx=1,pady=5)
        tk.Label(logFrame,text="Rating:",width=15,bg="light pink",
              font=smallf).grid(row=1,column=2,padx=1,pady=5)
        #options for lists to save to
        listNames=['Currently Watching','On Hold'
                   ,'Planning','Dropped','Completed']
        self.listNameVar=tk.StringVar()
        self.listNameVar.set(str(self.listName))
        #list names dropdown menu
        listNameDropdown=tk.OptionMenu(logFrame,self.listNameVar,
            *listNames,command=lambda x:self.displayListName())
        listNameDropdown.config(font=f)
        listNameDropdown.grid(row=2,column=0,padx=10,pady=5)
        
        #options for num of eps watched from 0 to total eps
        maxEps=['-']
        for i in range (0,self.totalEpisodes+1):
            maxEps.append(i)
        self.epsVar=tk.StringVar()
        self.epsVar.set(self.epsWatched)
        #eps watched dropdown menu
        epsDropdown=tk.OptionMenu(logFrame,self.epsVar,
            *maxEps,command=lambda x:self.displayEpsWatched())
        epsDropdown.config(font=f)
        epsDropdown.grid(row=2,column=1,padx=5,pady=5)
        
        #rating options from 0-5
        ratingOptions=['-',0,1,2,3,4,5]
        self.ratingVar=tk.StringVar()
        self.ratingVar.set(self.rating)
        #rating dropdown menu
        ratingDropdown=tk.OptionMenu(logFrame,self.ratingVar,
            *ratingOptions,command=lambda x:self.displayRating())
        ratingDropdown.config(font=f)
        ratingDropdown.grid(row=2,column=2,padx=5,pady=5)
        
        #save button
        saveButton=tk.Button(logFrame,text="Save",width=15,
            bg="light blue",font=f,
            command=lambda :self.save()
            ).grid(row=3,column=1,padx=5,pady=5)
        #delete button
        deleteButton=tk.Button(logFrame,text="Delete",width=15,
            bg="light blue",font=f,
            command=lambda:self.delete()
            ).grid(row=3,column=2,padx=5,pady=5)
        #back to profile button
        profileButton=tk.Button(logFrame,text="Back to profile",width=15,
            bg="light green",font=f,
            command=lambda:self.backToProfile(controller,parent)
            ).grid(row=4,column=2,padx=5,pady=5)

    def save(self):
        #check that user has not already logged this title
        #to prevent the same title being logged again

        #retrieve data chosen from option menus
        self.rating=self.displayRating()
        self.chosenListName=self.displayListName()
        self.epsWatched=self.displayEpsWatched()
        
        #set to completed if all eps watched
        if int(self.epsWatched)==int(self.totalEpisodes):
            self.chosenListName="Completed"
            
        #find listID of list name chosen
        cursor.execute("""SELECT listID FROM tblListNames
            WHERE (listName LIKE ?)""",[self.chosenListName])
        try:
            #if list has been selected and listID is found
            self.listID=cursor.fetchone()[0]
            #look for entries of the title in user's profile
            cursor.execute("""SELECT COUNT(*) FROM tblLists
                WHERE (userID==? AND titleID==?)""",
                           [self.userID,self.titleID])
            count=cursor.fetchall()[0][0]
            #if the user has not logged this title before
            if count==0:
                #log title to user's lists
                cursor.execute("""INSERT INTO tblLists
                VALUES(?,?,?,?,?)""",
                [self.epsWatched,self.rating,
                 self.userID,self.titleID,self.listID])
                conn.commit()
            #if user has already logged this title
            else:
                #update user's list entry
                cursor.execute("""UPDATE tblLists
                SET episodesWatched=?,rating=?,listID=?
                WHERE (titleID==? AND userID==?)"""
                ,[self.epsWatched,self.rating,
                  self.listID,self.titleID,self.userID])
                conn.commit()
        #if list has not been selected - error pop up message
        except:
            messagebox.showinfo("My App",
            "Choose a list to save the title to.")

    #delete button function
    def delete(self):
        #delete list entry
        cursor.execute("""DELETE FROM tblLists WHERE
        (userID==? AND titleID==?)""",
                       [self.userID,self.titleID])
        conn.commit()

    #closes list editor frame and opens profile frames
    #with updates lists
    def backToProfile(self,controller,parent):
        controller.closeFrame(listEditor)
        controller.showFrame(profile,parent)
        
    #drop down functions, retrieves chosen option
    def displayListName(self):
        chosenListName=self.listNameVar.get()
        return chosenListName

    def displayEpsWatched(self):
        epsWatched=self.epsVar.get()
        return epsWatched

    def displayRating(self):
        chosenRating=self.ratingVar.get()
        return chosenRating
        
app=myApp()
app.mainloop()


        
