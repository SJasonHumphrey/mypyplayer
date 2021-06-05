from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# importing tkinter, pygame, time and mutagen

#   setting up the players look and size

root = Tk()
root.title('MyPyPlayer')
root.geometry('300x600')
img = PhotoImage(file='images/MyPyPlayer.png') 
root.configure(bg='#99D98C')
logoimage = Label(image = img) 
logoimage.place(width = 300, height = 600)      

# mixer

pygame.mixer.init()

# to get the tracks time of play and length of track
# using time for time elapsed and mutagen to get track length

def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))
    current_song = playlist.curselection()
    song = playlist.get(ACTIVE)
    song = f'/Users/jasonhumphrey/Desktop/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_time = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_time} of {converted_song_time} ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # slider hasn't been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        # slider has been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_time} of {converted_song_time} ')
        
        move_time = int(my_slider.get()) + 1
        my_slider.config(value=move_time)
    
    # my_slider.config(value=current_time)
    status_bar.after(1000, play_time)

# add song function

def add_song():
    song = filedialog.askopenfilename(initialdir='user/music', title='Choose Track', filetypes=(('Audio Files', '* .mp3'),))
    song = song.replace('/Users/jasonhumphrey/Desktop/', '')
    song = song.replace('.mp3', '')
    playlist.insert(END, song)

# adding many songs to the playlist function

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='user/music', title='Choose Track', filetypes=(('Audio Files', '* .mp3'),))
    for song in songs:
        song = song.replace('/Users/jasonhumphrey/Desktop/', '')
        song = song.replace('.mp3', '')
        playlist.insert(END, song)

# song window with background and foreground color
master_frame = Frame(root)
master_frame.pack(pady=20)

playlist = Listbox(master_frame, bg ='#91a6ff',fg ='#faff7f',width = 30, selectbackground= '#faff7f', selectforeground='#91a6ff')
playlist.pack()

volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.pack()

# the song play function using pygame
def play():
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    song = f'/Users/jasonhumphrey/Desktop/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
# the play_time function is initialized inside play function
    play_time()
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)

# the stop function and clearing the track when stopped

def stop():
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    status_bar.config(text='')
    global stopped 
    stopped = True

# the next song function to play the next available track

def next_song():
    my_slider.config(value=0)
    status_bar.config(text='')
    next = playlist.curselection()
    next = next[0]+1
    song = playlist.get(next)
    song = f'/Users/jasonhumphrey/Desktop/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(next)
    playlist.selection_set(next, last=None)

# the previous track function to play the previous track if available

def previous_song():
    my_slider.config(value=0)
    status_bar.config(text='')
    next = playlist.curselection()
    next = next[0]-1
    song = playlist.get(next)
    song = f'/Users/jasonhumphrey/Desktop/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(next)
    playlist.selection_set(next, last=None)

# deletes individual song and will stop playback

def delete_song():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()
    
# deletes entire song list and stops playback

def delete_songs():
    stop()
    playlist.delete(0, END)
    pygame.mixer.music.stop()

global paused
paused = False

# checks current song to see if paused and what it should do
# if track is or isn't paused

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def slide(x):
    song = playlist.get(ACTIVE)
    song = f'/Users/jasonhumphrey/Desktop/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# bring in control images for playback buttons

back_button_img = PhotoImage(file ='images/back button.png')
pause_button_img = PhotoImage(file ='images/pause button.png')
play_button_img = PhotoImage(file ='images/play button.png')
stop_button_img = PhotoImage(file ='images/stop button.png')
forward_button_img = PhotoImage(file ='images/forward button.png')
controls_frame = Frame(master_frame)
controls_frame.pack()

# put buttons in control frame and inits the functions for those controls

back_btn = Button(controls_frame, image=back_button_img, borderwidth=0, command=previous_song)
pause_btn = Button(controls_frame, image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
play_btn = Button(controls_frame, image=play_button_img, borderwidth=0, command=play)
stop_btn = Button(controls_frame, image=stop_button_img,borderwidth=0, command=stop)
forward_btn = Button(controls_frame, image=forward_button_img, borderwidth=0, command=next_song)

# grid buttons and postion buttons layout

back_btn.grid(row=0 ,column=0)
pause_btn.grid(row=0 ,column=1)
play_btn.grid(row=0 ,column=2)
stop_btn.grid(row=0 ,column=3)
forward_btn.grid(row=0 ,column=4)

# create menu

my_menu = Menu(root)
root.config(menu=my_menu)

# add song from menu

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add Song', command=add_song)

# add many songs from menu

add_song_menu.add_command(label='Add Songs', command=add_many_songs)

# delete an individual song or songs from the menu

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Delete Song', command=delete_song)
remove_song_menu.add_command(label='Delete Songs', command=delete_songs)

# playback status bar with time of track and time elapsed

status_bar = Label(master_frame, text='', bd=1, relief=RIDGE, anchor=E, bg='#99D98C')
status_bar.pack(fill=X, side=TOP, ipady=2)

# music position slider

my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=250)
my_slider.pack()
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=250)
volume_slider.pack()
# slide label





root.mainloop()
