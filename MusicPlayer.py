import sys 
import pygame
import tkinter as tk
import ctypes
import math
import random
from PIL import Image, ImageTk, ImageEnhance

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
LYRIC_COLOR = "#ffffff"
LYRIC_FONT = ("Helvetica", 20, "bold")
WATERMARK = ("Helvetica", 12, "italic")

lyrics = [
    ("So, what if I call", 5.2),
    ("And you pick up the phone?", 4.7), 
    ("And I use this holiday to makе my way to your ghost", 9),
    ("Oh, what if you're lonely", 4.5),
    ("And you know I am too?", 4.7),
    ("And I get the chance to say", 3.4),
    ("\"Merry Christmas, I miss you\"", 6),
    ("I miss you", 23)
]


FADE_COLORS = ["#0b132b", "#1c2844", "#3d5277", "#6881ad", "#9db2d8", "#cdd8ed", "#ffffff"]

GLITTER_COLORS = ["#ffffff", "#edf2f4", "#d8f3dc", "#caf0f8", "#fefae0"]

MAX_GLITTER = 40


class MusicApp:
            
    def __init__(self, root):

        self.root = root
        self.root.title("Merry Christmas, I miss you")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.current_lyric_index = 0
        self.snowflake = []
        
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        icon_image = Image.open("Assets/snowflakelogo.png")

        self.window_logo = ImageTk.PhotoImage(icon_image)

        self.root.iconphoto(False, self.window_logo)

        bg_image = Image.open("Assets/christmas_snoopy.jpg")
        bg_image = bg_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)

        dimmer = ImageEnhance.Brightness(bg_image)
        dark_bg_image = dimmer.enhance(0.4)

        self.tk_dark_bg = ImageTk.PhotoImage(dark_bg_image)

        self.canvas.create_image(0, 0, image=self.tk_dark_bg, anchor="nw")

        self.canvas.create_text(WINDOW_WIDTH - 80, WINDOW_HEIGHT - 40, text= "Made by Levi", fill=LYRIC_COLOR, font=WATERMARK)

        self.dark_title_bar()

        #self.musicplayer()
        #self.lyricspop()

        self.falling_snow()

        self.root.after(500, self.musicplayer(), self.lyricspop())


    def musicplayer(self):
    
        try: 
            pygame.mixer.init()
            pygame.mixer.music.load("Assets/Merry_Christmas,_i_miss_you.mp3")
            pygame.mixer.music.play(0, 185.2)
        
        except pygame.error as e:
            print(f"\n[CRITICAL ERROR] Pygame failed because: {e}")
            print("Type of error:", type(e).__name__)
            sys.exit()

    
    def lyrics_fade(self, text, frame=0, fading_in=True):

        if fading_in:
            current_color = FADE_COLORS[frame]

        else:
            current_color = list(reversed(FADE_COLORS))[frame]

        self.canvas.create_text(
        WINDOW_WIDTH // 2, WINDOW_HEIGHT - 300,
        text=text,
        fill=current_color,
        font=LYRIC_FONT,
        tags="lyric_text",
        justify="center"
        )

        if frame < len(FADE_COLORS) - 1:
            self.root.after(40, lambda: self.lyrics_fade(text, frame + 1, fading_in))


    def lyricspop(self):

        if self.current_lyric_index < len(lyrics):
            self.canvas.delete("lyric_text")

            text, duration = lyrics[self.current_lyric_index]

            delay = int(duration * 1000)

            self.lyrics_fade(text, frame=0, fading_in=True)

            fade_out_delay = max(100, delay - 280)
            self.root.after(fade_out_delay, lambda: self.lyrics_fade(text, frame=0, fading_in=False))

            self.current_lyric_index += 1

            self.root.after(delay, self.lyricspop)

        else: 
            self.canvas.delete("lyric_text")
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 300, text="Merry Christmas, I miss you - Alex Crichton", fill=LYRIC_COLOR, font=LYRIC_FONT)
            pygame.mixer.music.stop()

    
    def falling_snow(self):
        
        self.canvas.delete("snow")

        if len(self.snowflake) < MAX_GLITTER and random.random() < 0.4:

            self.snowflake.append({
                "x": random.randint(0, WINDOW_WIDTH),
                "y": 0,
                "radius": random.uniform(1.5, 3.0),
                "speed": random.uniform(1.5, 4.0),
                "color": random.choice(GLITTER_COLORS)
            })

        for flake in self.snowflake[:]:

            flake["y"] += flake ["speed"]

            current_x = flake["x"]
            r = flake["radius"]

            if flake["y"] > WINDOW_HEIGHT:
                self.snowflake.remove(flake)
                continue

            self.canvas.create_oval(
            current_x - r, flake["y"] - r,
            current_x + r, flake["y"] + r,
            fill=flake["color"],
            outline="",
            tags="snow"
            )

        self.root.after(20, self.falling_snow)


    def dark_title_bar(self):

        window.update()

        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ctypes.windll.user32.GetParent

        hwnd = get_parent(window.winfo_id())
        rendering_policy = ctypes.c_int(2)
        
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(rendering_policy), ctypes.sizeof(rendering_policy))


if __name__ == "__main__":
    window = tk.Tk()
    app = MusicApp(window)
    window.mainloop()