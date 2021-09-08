from tkinter import Tk, Button, Canvas, PhotoImage
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_SMALL = ('Ariel', 40, 'italic')
FONT_LARGE = ('Ariel', 60, 'bold')

current_card = {}
word_dictionary = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    word_dictionary = original_data.to_dict(orient='records')
else:
    word_dictionary = data.to_dict(orient='records')
    # word_dictionary = data.to_dict()['French']


def is_known():
    word_dictionary.remove(current_card)
    data = pandas.DataFrame(word_dictionary)
    data.to_csv('data/words_to_learn.csv', index=False)
    change_card()

# ----Show English Card----
def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_background, image=card_back_img)

# ----Create new flash cards----

def change_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    # random_word = word_dictionary[random.randint(0, 100)]
    current_card = random.choice(word_dictionary)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_background, image=card_img)
    flip_timer = window.after(3000, func=flip_card)
    

# ----UI----
# Window
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# window.setup(height=1000, width=1000)

flip_timer = window.after(3000, func=flip_card)

# Flash card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_img = PhotoImage(file='images/card_front.gif')
card_back_img = PhotoImage(file='images/card_back.gif')
card_background = canvas.create_image(400, 263, image=card_img)
card_title = canvas.create_text(400, 150, text='title', font=FONT_SMALL)
card_word = canvas.create_text(400, 263, text='word', font=FONT_LARGE)

canvas.grid(row=0, column=0, columnspan=2)

# × Buttons
wrong_img = PhotoImage(file='images/wrong.gif')
wrong_button = Button(image=wrong_img, highlightthickness=0, command=change_card)
wrong_button.grid(row=1, column=0)

# ○ Buttons
right_img = PhotoImage(file='images/right.gif')
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

change_card()

window.mainloop()