"""
Author: Luke Guppy
Usage: Reference README (https://github.com/lukeguppy/TwitchChecker)
Dependencies: twitchAPI, tkinter
"""

import asyncio
import webbrowser
import tkinter as tk
import sys
import threading
from twitchAPI.twitch import Twitch

CLIENT_ID = ''
CLIENT_SECRET = ''
STREAMERS = ['Streamer1', 'Streamer2']
active_streams = {}
twitchLogoPath = r'C:\Users\lukew\Project\FinalReport\Images\twitch_logo.ico'
update_interval = 60 #seconds

notification_window = None

async def authenticate():
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    await twitch.authenticate_app([])
    return twitch

def open_stream(channel_name):
    webbrowser.open(f'https://www.twitch.tv/{channel_name}')
    remove_streamer(channel_name)

def create_notification():
    global notification_window
    if notification_window is None or not notification_window.winfo_exists():
        notification_window = tk.Tk()
        notification_window.title("Live Stream Notifications")
        notification_window.configure(bg='#1e1e1e')
        notification_window.protocol("WM_DELETE_WINDOW", close_program)
    else:
        for widget in notification_window.winfo_children():
            widget.destroy()

    # Check if there are any active streams to display
    if active_streams:
        for streamer, title in active_streams.items():
            frame = tk.Frame(notification_window, bg='#1e1e1e')
            label = tk.Label(
                frame,
                text=f"{streamer} is Live! - {title}",
                bg='#1e1e1e',
                fg='white',
                font=('Arial', 12),
                wraplength=280,
                justify='center'
            )
            label.pack(pady=5)
            
            button_frame = tk.Frame(frame, bg='#1e1e1e')
            open_button = tk.Button(button_frame, text="Open", command=lambda s=streamer: open_stream(s), bg='#007acc', fg='white', width=10)
            open_button.pack(side=tk.LEFT, padx=5)
            
            dismiss_button = tk.Button(button_frame, text="Dismiss", command=lambda s=streamer: remove_streamer(s), bg='#ff3b30', fg='white', width=10)
            dismiss_button.pack(side=tk.LEFT, padx=5)
            
            button_frame.pack(pady=5)
            frame.pack(pady=10)

        notification_window.update_idletasks()
        window_width = 300
        window_height = notification_window.winfo_reqheight() + 20

        screen_width = notification_window.winfo_screenwidth()
        screen_height = notification_window.winfo_screenheight()

        x_position = screen_width - window_width - 10
        y_position = screen_height - window_height - 60

        notification_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        notification_window.update()
        notification_window.deiconify()
    else:
        close_notification_window()

def remove_streamer(streamer):
    if streamer in active_streams:
        del active_streams[streamer]
        
    if streamer in STREAMERS:
        STREAMERS.remove(streamer)  
    
    print("Dismissed " + streamer)
    print(STREAMERS)

    create_notification()

def close_notification_window():
    global notification_window
    if notification_window is not None:
        notification_window.withdraw()  

def close_program():
    global notification_window
    if notification_window is not None:
        notification_window.destroy()
    sys.exit()

async def check_stream(twitch, streamer):
    try:
        user_info_gen = twitch.get_users(logins=[streamer])
        user_info = None

        async for user in user_info_gen:
            user_info = user

        if user_info is None:
            print(f"No user found for {streamer}.")
            return False

        user_id = user_info.id

        streams_gen = twitch.get_streams(user_id=user_id)
        streams = []

        async for stream in streams_gen:
            streams.append(stream)

        if streams:
            stream_title = streams[0].title
            if streamer not in active_streams:
                active_streams[streamer] = stream_title
                create_notification()
        elif streamer in active_streams:
            remove_streamer(streamer)
    except Exception as e:
        print(f"Error checking stream status for {streamer}: {e}")

async def check_all_streams(twitch):
    while True:
        print("Checking streamers:")
        print(STREAMERS)
        if not STREAMERS:  # Exit if there are no streamers left to check
            close_program()
            return

        tasks = [check_stream(twitch, streamer) for streamer in STREAMERS]
        await asyncio.gather(*tasks)
        await asyncio.sleep(update_interval)

def run_asyncio_loop():
    asyncio.run(main())

async def main():
    twitch = await authenticate()
    await check_all_streams(twitch)

if __name__ == "__main__":
    threading.Thread(target=run_asyncio_loop, daemon=True).start()
    
    if notification_window is None:
        notification_window = tk.Tk()
        notification_window.iconbitmap(twitchLogoPath)
        notification_window.title("Stream Checker")
        notification_window.configure(bg='#1e1e1e')
        notification_window.withdraw()  
    notification_window.mainloop()
