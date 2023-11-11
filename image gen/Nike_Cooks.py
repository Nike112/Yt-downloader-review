import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon') #provides sentiment scores based on the words used.
sia = SentimentIntensityAnalyzer() #this helps analyse the customers reviews and decides if positve or negative review
import customtkinter as ctk
from tkinter import ttk
import tkinter
from pytube import YouTube
import os
import mysql.connector as m
from PIL import Image, ImageTk
import threading

def download_video():
    url = url_entry2.get()
    resolution = res_var.get()

    progress_label2.pack(pady = 10)
    progress_bar2.pack(pady = 10)
    status_label2.pack(pady = 10)
    

    try:
        yt = YouTube(url , on_progress_callback= on_progress2)
        stream = yt.streams.filter(res = resolution ).first() # ensures given url is legit , else it will not return anything
        #downloads video
        stream.download(output_path= "videos")
        status_label2.configure(text = "  Downloaded  " , text_color = "white" , fg_color = "green")
    except Exception as e:
        status_label2.configure(text = f"Error {str(e)}", text_color = "white" , fg_color = "red" )
        



def download_song():
    url = url_entry1.get()

    progress_label1.pack(pady = 10)
    progress_bar1.pack(pady = 10)
    status_label1.pack(pady = 10)


    try:
        yt = YouTube(url , on_progress_callback= on_progress1)
        video = yt.streams.filter(only_audio=True).first()# ensures given url is legit , else it will not return anything
        #downloads video
        out_file = video.download(output_path='songs')
        base , ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        status_label1.configure(text = "  Downloaded  " , text_color = "white" , fg_color = "green")

    except Exception as e:
        status_label1.configure(text = f"Error {str(e)}", text_color = "white" , fg_color = "red" )



mcon = m.connect(host = "localhost" , user = "Niketh" , password = "Root@123" , database = "Reviews")
mycur = mcon.cursor()
if mcon.is_connected():
    print("works")
else:
    print("Nope")
mycur.execute("drop table customers")
mycur.execute("create table if not exists customers(OrderID int(5) primary key , First_Name varchar(10) , Last_Name varchar(10) , Gender varchar(15) , Sentiment varchar(20))")


def on_progress1(stream , chunk , bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    per_completed = (bytes_downloaded / total_size ) * 100

    progress_label1.configure(text = str(int(per_completed)) + "%")
    progress_label1.update()
    progress_bar1.set(float(per_completed / 100))



def on_progress2(stream , chunk , bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    per_completed = (bytes_downloaded / total_size ) * 100

    progress_label2.configure(text = str(int(per_completed)) + "%")
    progress_label2.update()
    progress_bar2.set(float(per_completed / 100))




def db(i):
    firstname = first_name_entry.get()
    lastname = last_name_entry.get()
    title = title_combobox.get()
    rev = review.get("1.0" , "end")
    mycur.execute("insert ignore into customers values({},'{}','{}','{}','{}')".format( i, firstname , lastname , title , Sentiment(rev) ))
    mcon.commit()
    

def Sentiment(res):
    revDic = sia.polarity_scores(res)
    revComp = revDic['compound']
    if revComp > 0.49 :
        return "Happy"
            
    elif revComp < 0 :
        return "Unhappy"
            
    else:
        return "Neutral"
        


#creating the root window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root.title("Futzy")



i = 0
def enter_data():
    accepted = accept_var.get()
    global i
    i += 1
    if accepted=="Accepted":
        # User info
        print(i)
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        rev = review.get("1.0" , "end")

        db(i) # storing data

        #clearing user info for the next person
        first_name_entry.delete(0, 'end')
        last_name_entry.delete(0, 'end')
        title_combobox.delete(0, 'end')
        review.delete("1.0",'end')

        if firstname and lastname:
            title = title_combobox.get()
            print("First name: ", firstname, "Last name: ", lastname)
            print("Gender: ", title)
            Sentiment(rev)
            print("------------------------------------------")
                
        else:
            tkinter.messagebox.showwarning(title="Error", message="First name and last name are required.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="You have not accepted the terms")







#geometry
root.geometry("470x420")
#min and max size of window
root.minsize(470, 400)
root.maxsize(470 , 500)

tabview = ctk.CTkTabview(master=root)
tabview.pack(fill = ctk.BOTH , expand = True , padx = 10 , pady =10)
tabview.add("MP3")
tabview.add("MP4")
tabview.add("Review")
tabview.add("gojo")

#label and entry widgets for video URL
url_label = ctk.CTkLabel(master = tabview.tab("MP3"), text = "Enter Youtube URL below : ")
url_entry1 = ctk.CTkEntry(master = tabview.tab("MP3"), width=400 , height=40)
url_label.pack()
url_entry1.pack()

url_label = ctk.CTkLabel(master = tabview.tab("MP4"), text = "Enter Youtube URL below : ")
url_entry2 = ctk.CTkEntry(master = tabview.tab("MP4"), width=400 , height=40)
url_label.pack()
url_entry2.pack()


mp4dnload_button = ctk.CTkButton(master = tabview.tab("MP4"), text = "Download MP4" , command= download_video )
mp3dnload_button = ctk.CTkButton(master = tabview.tab("MP3"), text = "Download MP3" , command= download_song )
mp3dnload_button.pack(pady = 10)
mp4dnload_button.pack(pady = 10)


#creating resolution box
resolutions = ["720p" , "360p" , "240p" , "144p"]
res_var = ctk.StringVar()
res_combobox = ttk.Combobox(master = tabview.tab("MP4"), values=resolutions, textvariable=res_var)
res_combobox.pack(pady = 10)
res_combobox.set("720p")


#progress bar label to display download time

progress_label1 = ctk.CTkLabel(master = tabview.tab("MP3"), text = "0%")

progress_bar1 = ctk.CTkProgressBar(master = tabview.tab("MP3"), width=400)
progress_bar1.set(0)




progress_label2 = ctk.CTkLabel(master = tabview.tab("MP4"), text = "0%")

progress_bar2 = ctk.CTkProgressBar(master = tabview.tab("MP4"), width=400)
progress_bar2.set(0)


#status
status_label1 = ctk.CTkLabel(master = tabview.tab("MP3"), text="")
status_label2 = ctk.CTkLabel(master = tabview.tab("MP4"), text="")


user_info_frame =tkinter.LabelFrame(master = tabview.tab("Review"), text="User Information")
user_info_frame.grid(row= 0, column=0, padx=20, pady=5)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)

last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)

first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

title_label = tkinter.Label(user_info_frame, text="Gender")
title_combobox = ttk.Combobox(user_info_frame, values=["Male" , "Female" , "Rather not say"])

title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

user_Rev =tkinter.LabelFrame(master = tabview.tab("Review"), text="User Review")
user_Rev.grid(row= 2, column=0, padx=20, pady=5)

review = tkinter.Text(user_Rev , width= 45 , height=5)
review.grid(row = 0 , column= 0 , padx=10 , pady = 5)

terms_frame = tkinter.LabelFrame(master = tabview.tab("Review"), text="Terms & Conditions")
terms_frame.grid(row=3, column=0, sticky="news", padx=20, pady=5)

accept_var = tkinter.StringVar(value="Not Accepted")

terms_check = tkinter.Checkbutton(terms_frame, text= "I accept the terms and conditions.",variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

button = tkinter.Button(master = tabview.tab("Review"), text = "Enter Data", padx=20, pady=5, command = enter_data)
button.grid(row=4, column=0, sticky="news", padx=20, pady=5)

gif_frames = []
frame_delay = 0

def read_gif():
    global frame_delay

    gif_file = Image.open('images\gojovssukuna.gif')

    for r in range(0, gif_file.n_frames):
        gif_file.seek(r)
        gif_frames.append(gif_file.copy())
    frame_delay = gif_file.info['duration']
    play_gif()

frame_count = -1

def play_gif():
    global frame_count , current_frame
    if frame_count >= len(gif_frames) - 1:
        frame_count = -1
        play_gif()
    else:
        frame_count +=1
        current_frame = ImageTk.PhotoImage(gif_frames[frame_count])
        gif_lb.config(image=current_frame)
        tabview.tab("gojo").after(frame_delay, play_gif)


gif_lb = tkinter.Label(master= tabview.tab("gojo"))
gif_lb.pack(fill= tkinter.BOTH)
threading.Thread(target=read_gif).start()
read_gif()
#to start application
root.mainloop()