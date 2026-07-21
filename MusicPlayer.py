import sys 
import pygame
import tkinter as tk
import ctypes
import random
from PIL import Image, ImageTk, ImageEnhance

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
LYRIC_COLOR = "#ffffff"
LYRIC_FONT = ("Helvetica", 20, "bold")
WATERMARK = ("Helvetica", 12, "italic")

verse_1 = [
    ("You walked in the party, your coat was untied", 9.2),
    ("Slammin\' the door \'cause it\'s colder outside", 8.3),
    ("And I won\'t forget that moment like the blink of an eye", 10.0),
    ("You\'re off to the beach now \'til the weather gets nice", 6.5)
]

chorus = [
    ("But what if I call", 5.0),
    ("So, what if I call", 4.6),
    ("And you pick up the phone?", 4.7), 
    ("And I use this holiday to makе my way to your ghost", 9.0),
    ("Oh, what if you're lonely", 4.5),
    ("And you know I am too?", 4.7),
    ("And I get the chance to say", 3.3),
    ("\"Merry Christmas, I miss you\"", 6.0),
    ("I miss you", 5.0)
]

verse_2 = [
    ("So I\'ll hang the lights up, you\'ll see them from space", 9.2),
    ("And all that I want on my list is that look on your face", 8.3),
    ("When I said, \"November's early to be playin' these songs\"", 10.0),
    ("Now whеn I look back, I can see I was wrong", 6.9)
]

bridge = [
    ("You know it\'s true", 4.6, random.randint(200, 1000), random.randint(110, 230)),
    ("Yeah, I miss you", 4.5, random.randint(200, 1000), random.randint(240, 360)),
    ("You know it\'s true", 4.5, random.randint(200, 1000), random.randint(370, 490))
]


FADE_COLORS = ["#0b132b", "#1c2844", "#3d5277", "#6881ad", "#9db2d8", "#cdd8ed", "#ffffff"]

GLITTER_COLORS = ["#ffffff", "#edf2f4", "#d8f3dc", "#caf0f8", "#fefae0"]

MAX_GLITTER = 45

first_verse_Time = 20
chorus_Time = 54
second_verse_Time = 97
second_chorus_Time = 132
bridge_Time = 173
last_chorus_Time = 186


class MusicApp:
            
    def __init__(self, root):

        self.root = root
        self.root.title("Merry Christmas, I miss you")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.snow = []
        
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

        self.musicplayer()

        self.falling_snow()


    def musicplayer(self):
    
        try: 
            pygame.mixer.init()
            pygame.mixer.music.load("Assets/Merry_Christmas,_i_miss_you.mp3")
            pygame.mixer.music.play(0)

            self.time_elapsed = 0

            self.count_validation()
        
        except pygame.error as e:
            print(f"\n[CRITICAL ERROR] Pygame failed because: {e}")
            print("Type of error:", type(e).__name__)
            sys.exit()

    
    def count_validation(self):

        if self.time_elapsed >= 0:

            print(f"[VALIDATION] Time: {self.time_elapsed}s")

            self.time_elapsed += 1

            self.root.after(1000, self.count_validation)

        if self.time_elapsed == first_verse_Time:

            self.current_lyric_index = 0
            self.index_validation = len(verse_1)
            self.lyrics_pop()
        
        if self.time_elapsed == chorus_Time:

            self.current_lyric_index = 0
            self.index_validation = len(chorus)
            self.lyrics_pop()

        if self.time_elapsed == second_verse_Time:

            self.current_lyric_index = 0
            self.index_validation = len(verse_2)
            self.root.after(600, self.lyrics_pop)

        if self.time_elapsed == second_chorus_Time:

            self.current_lyric_index = 1
            self.index_validation = len(chorus)
            self.lyrics_pop()

        if self.time_elapsed == bridge_Time:

            self.current_lyric_index = 0
            self.index_validation = len(bridge)
            self.bridge_pop()

        if self.time_elapsed == last_chorus_Time:

            self.current_lyric_index = 1
            self.index_validation = len(chorus)
            self.root.after(700, self.lyrics_pop)

    
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


    def bridge_fade(self, text, width, height, frame=0, fading_in=True):

        if fading_in:
            current_color = FADE_COLORS[frame]

        else:
            current_color = list(reversed(FADE_COLORS))[frame]

        self.canvas.create_text(
        width, height,
        text=text,
        fill=current_color,
        font=LYRIC_FONT,
        tags="lyric_text",
        justify="center"
        )

        if frame < len(FADE_COLORS) - 1:
            self.root.after(40, lambda: self.bridge_fade(text, width, height, frame + 1, fading_in))


    def lyrics_pop(self):

        self.canvas.delete("lyric_text")

        if self.current_lyric_index < self.index_validation:

            if first_verse_Time <= self.time_elapsed < chorus_Time:

                text, duration = verse_1[self.current_lyric_index]

            if chorus_Time <= self.time_elapsed < second_verse_Time:

                text, duration = chorus[self.current_lyric_index]

                if self.current_lyric_index == 0:
                    self.current_lyric_index += 1

            if second_verse_Time <= self.time_elapsed < second_chorus_Time:

                text, duration = verse_2[self.current_lyric_index]

            if second_chorus_Time <= self.time_elapsed < bridge_Time:

                text, duration = chorus[self.current_lyric_index]

                if self.current_lyric_index == 8:
                    duration -= 0.8

            if last_chorus_Time <= self.time_elapsed :

                text, duration = chorus[self.current_lyric_index]

                if self.current_lyric_index == 0:
                    self.current_lyric_index += 1

            delay = int(duration * 1000)

            self.lyrics_fade(text, frame=0, fading_in=True)

            fade_out_delay = max(100, delay - 280)
            self.root.after(fade_out_delay, lambda: self.lyrics_fade(text, frame=0, fading_in=False))

            self.current_lyric_index += 1

            self.root.after(delay, self.lyrics_pop)

            
    def bridge_pop(self):

        self.canvas.delete("lyric_text")

        if self.current_lyric_index < self.index_validation:

            if bridge_Time <= self.time_elapsed < last_chorus_Time:

                text, duration, width, height = bridge[self.current_lyric_index]

                delay = int(duration * 1000)

                self.bridge_fade(text, width, height, frame=0, fading_in=True)

                fade_out_delay = max(100, delay - 280)
                self.root.after(fade_out_delay, lambda: self.bridge_fade(text, width, height, frame=0, fading_in=False))

                self.current_lyric_index += 1

                self.root.after(delay, self.bridge_pop)

    
    def falling_snow(self):
        
        self.canvas.delete("snow")

        if len(self.snow) < MAX_GLITTER and random.random() < 0.4:

            self.snow.append({
                "x": random.randint(0, WINDOW_WIDTH),
                "y": 0,
                "radius": random.uniform(1.5, 3.0),
                "speed": random.uniform(1.5, 4.0),
                "sway": random.uniform(-1.2, 1.2),
                "color": random.choice(GLITTER_COLORS)
            })

        for glitter in self.snow[:]:

            glitter["x"] += glitter ["sway"]
            glitter["y"] += glitter ["speed"]

            current_x = glitter["x"]
            current_y = glitter["y"]
            r = glitter["radius"]

            if glitter["y"] > WINDOW_HEIGHT:
                self.snow.remove(glitter)
                continue

            self.canvas.create_oval(
            current_x - r, current_y - r,
            current_x + r, current_y + r,
            fill=glitter["color"],
            outline="",
            tags="snow"
            )

        self.root.after(20, self.falling_snow)


    def outro_title(self, frame=0, fading_in=True):

        current_color = FADE_COLORS[frame]

        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 300,
            text="Merry Christmas, I miss you - Alex Crichton",
            fill=current_color, 
            font=LYRIC_FONT,
            justify="center"
        )

        if frame < len(FADE_COLORS) - 1:
            self.root.after(40, lambda: self.outro_title(frame + 1, fading_in))


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