#This file contains the mainloop of the program
#This file also contains classes to handle the tkinter application
#Classes written for pages and for mainframe of app

import tkinter as tk
import urllib.request
from PIL import ImageTk, Image

#Import necessary functions for Spotify API
import myClient

#Define global vars
token = None
quiz_answer = None

#Class to handle individual pages of application
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    #Show page
    def show(self):
        self.lift()

    #Logic for finding right answer and displaying it to screen
    def handle_answer(self, ans):
        global quiz_answer
        
        if ans == quiz_answer:
            self.answer_label.configure(text="Correct!")
        else:
            self.answer_label.configure(text="Wrong!")

        self.show()

    #Function retrieves info for 2 tracks from Spotify and updates the GUI
    def update(self):
        global token, quiz_answer

        #Track info retrieved
        track_A = myClient.Track()
        track_A.get_rand_track_info(token)

        track_B = myClient.Track()
        track_B.get_rand_track_info(token)

        #Ensures one track will be more popular than the other
        while track_A.song_popularity == track_B.song_popularity:
            track_B.get_rand_track_info(token)

        #Find answer to quiz
        if track_A.song_popularity > track_B.song_popularity:
            quiz_answer = 'a'
        else:
            quiz_answer = 'b'

        #Handle images and text to be displayed
        urllib.request.urlretrieve(track_A.cover_art_url, "Cover_A.png")
        urllib.request.urlretrieve(track_B.cover_art_url, "Cover_B.png")

        textA = f"{track_A.track_name}\n{track_A.album_name}\n{track_A.artist_name}"
        textB = f"{track_B.track_name}\n{track_B.album_name}\n{track_B.artist_name}"

        imageA = ImageTk.PhotoImage(Image.open("Cover_A.png").resize((160, 160), Image.ANTIALIAS))
        imageB = ImageTk.PhotoImage(Image.open("Cover_B.png").resize((160, 160), Image.ANTIALIAS))

        #Update visuals on page 2
        self.labelA.configure(text=textA)
        self.labelB.configure(text=textB)

        self.coverA.configure(image=imageA)
        self.coverA.image = imageA
        self.coverB.configure(image=imageB)
        self.coverB.image = imageB
        
        self.show()

#Starting page of the application
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        #Set background of page
        background_image = tk.PhotoImage(file="Background.png")
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        # label on start screen
        home_label = tk.Label(self,
            text="Popularity Contest",
            font=("Proxima Nova", 15),
            bg="grey",
            fg="white",
            image=background_image,
            compound=tk.CENTER
        )

        home_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER, relwidth=1, relheight=0.35)
       
#Page to display choices
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        #Set background of page
        background_image = tk.PhotoImage(file="Background.png")
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        #Labels with track info
        self.labelA = tk.Label(self,
            text=" ",
            fg="white",
            image=background_image,
            compound=tk.CENTER
        )

        self.labelB = tk.Label(self,
            text=" ",
            fg="white",
            image=background_image,
            compound=tk.CENTER
        )

        self.labelA.place(relx=0.25, rely=0.57, anchor=tk.CENTER, relwidth=0.3, relheight=0.4)
        self.labelB.place(relx=0.75, rely=0.57, anchor=tk.CENTER, relwidth=0.3, relheight=0.4)

        # use labels to display cover art
        self.coverA = tk.Label(self, bg = "grey")
        self.coverB = tk.Label(self, bg = "grey")

        self.coverA.place(relx=0.25, rely=0.25, anchor=tk.CENTER, width=160, height=160)
        self.coverB.place(relx=0.75, rely=0.25, anchor=tk.CENTER, width=160, height=160)
       
#Page to display answer
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        #Set background of page
        background_image = tk.PhotoImage(file="Background.png")
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        # label on start screen
        self.answer_label = tk.Label(self,
            text="Correct!",
            font=("Proxima Nova", 15),
            fg="white",
            image=background_image,
            compound=tk.CENTER
        )

        self.answer_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER, relwidth=1, relheight=0.35)

#Class to handle visual application
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        #Pages instantiated within main frame of app
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #Instantiate buttons and give them required functionality
        b1 = tk.Button(p1,
            text="Play!",
            bg="#75E84A",
            width=20,
            height=5,
            compound=tk.CENTER,
            bd=-10,
            padx=0,
            pady=0,
            command=p2.update
        )

        b2 = tk.Button(p2,
            text="Option A",
            bg="#75E84A",
            width=20,
            height=5,
            compound=tk.CENTER,
            bd=-10,
            padx=0,
            pady=0,
            command=lambda: p3.handle_answer('a')
        )

        b3 = tk.Button(p2,
            text="Option B",
            bg="#75E84A",
            width=20,
            height=5,
            compound=tk.CENTER,
            bd=-10,
            padx=0,
            pady=0,
            command=lambda: p3.handle_answer('b')
        )

        b4 = tk.Button(p3,
            text="Play Again!",
            bg="#75E84A",
            width=20,
            height=5,
            compound=tk.CENTER,
            bd=-10,
            padx=0,
            pady=0,
            command=p2.update
        )

        # placing the buttons on window
        b1.place(in_=p1, relx=0.5, rely=0.5, anchor=tk.CENTER)
        b2.place(in_=p2, relx=0.25, rely=0.8, anchor=tk.CENTER)
        b3.place(in_=p2, relx=0.75, rely=0.8, anchor=tk.CENTER)
        b4.place(in_=p3, relx=0.5, rely=0.5, anchor=tk.CENTER)

        p1.show()


#Main loop of the application
if __name__ == "__main__":
    token = myClient.get_token()
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x400")
    root.resizable(0, 0)
    root.mainloop()