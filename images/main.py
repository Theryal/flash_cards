import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ------------------------------------- Flashcard word logic ----------------------------------------------------- #
try:
    data = pandas.read_csv("../data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("../data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def draw_flashcard():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(flashy_flashcard, image=flashcard_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(flashy_flashcard, image=flashcard_back)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("../data/words_to_learn.csv", index=False)
    draw_flashcard()

# -------------------------------------------- UI Setup ---------------------------------------------------------- #


window = Tk()
window.configure(background=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flashy")
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
flashcard_front = PhotoImage(file="card_front.png")
flashcard_back = PhotoImage(file="card_back.png")
flashy_flashcard = canvas.create_image(400, 263, image=flashcard_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

x_sign = PhotoImage(file="wrong.png")
dk_button = Button(image=x_sign, command=draw_flashcard, highlightthickness=0)
dk_button.grid(column=0, row=1)

correct_sign = PhotoImage(file="right.png")
correct_button = Button(image=correct_sign, command=is_known, highlightthickness=0)
correct_button.grid(column=1, row=1)

draw_flashcard()

window.mainloop()
