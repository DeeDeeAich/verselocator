"""
CREATED BY DEEDEEAICH
"""

from tkinter import *
from tkinter import ttk
import os
from dotenv import load_dotenv
import requests
import json

# Loads API Key from an .env file, is more secure than just regular py file
load_dotenv("api_key.env")
api_key = os.getenv("API_KEY")
api_key = json.loads(api_key)

# Creates first window, sets title, sets the size, sets the icon
root = Tk()
root.title("Verse Locator")
root.geometry("680x225")
root.iconbitmap("icon.ico")

# Header/Title - Uses Day Roman font (https://www.dafont.com/day-roman.font)
header = ttk.Label(root, text="Verse Locator", font=("Day Roman", 30)).pack()

# Creates the Entry widget verse_input that takes the user-requested verse
verse_input = ttk.Entry(root, width=30)
verse_input.pack()
ttk.Label(text="", borderwidth=3, font=("Arial", 2)).pack()

# Height variable is for increasing height each time a verse is added to the verse history list.
height = 225


def on_click():
    # Grabs the text put in the entry widget verse_input and stores it in a variable called location
    location = verse_input.get()
    verse_history = [verse_input.get()]

    # Iterates through verse_history list, each time a verse is put in the entry box, a label will be created at the
    # bottom with the verse that you inputted. It also increases the height each time so the history isn't cut off.
    for item in verse_history:
        if item == "":
            continue
        global height
        height += 20
        Label(root, text=item, font=("Day Roman", 10)).pack()
        root.geometry(f"680x{height}")

    # Deletes all the text entered in the entry widget to give visual effect
    verse_input.delete(0, END)

    # Creates a new window
    root2 = Toplevel(root)
    root2.title("Verse Locator")
    root2.iconbitmap("icon.ico")

    # Uses the requests library to grab the inputted verse and search for it in the ESV API
    verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={location}", headers=api_key)
    verse = verse.text
    # Uses the json library to store verse as a dictionary. When making a request to the API, it stores it in an object
    # called requests.models.Response
    verse = json.loads(verse)

    # Creates a label in the window that uses the key "passages" and the 0th index of "passages" as the text
    try:
        verse_text = Label(root2, text=verse["passages"][0], font=("Cardo", 10))
        verse_text.pack(fill="both", expand=1)
    # Error Handling: If the verses inputted do not exist, the console will not only receive the error, but a label
    # is created to show the user that the verse does not exist.
    except KeyError:
        error = Label(root2, text="Error! Verse does not exist!", fg="red")
        error.pack(fill="both", expand=1)
        root2.geometry("420x90")
    except IndexError:
        error = Label(root2, text="Error! Verse does not exist!", fg="red")
        error.pack(fill="both", expand=1)
        root2.geometry("420x90")


# Enter key event, runs on_click()
def enter(event):
    on_click()


# Binds enter key and the enter function to run the on_click() function when enter is pressed
root.bind("<Return>", enter)
locate_button = ttk.Button(root, text="Locate", command=on_click)
locate_button.pack()
# Label is created for spacing between button and the requesting verse notice
ttk.Label(text="", borderwidth=3, font=("Arial", 2)).pack()
# Creates label for requesting verses notice
ttk.Label(root, font=("Arial", 7), text="Unless otherwise indicated, all Scripture quotations are from the ESV® Bible "
                                        "(The Holy Bible, English Standard Version®), \ncopyright © 2001 by Crossway, "
                                        "a publishing ministry of Good News Publishers. Used by permission. All "
                                        "rights reserved. \nYou may not copy or download more than 500 consecutive "
                                        "verses of the ESV Bible or more than one half of any book of the ESV "
                                        "Bible.").pack()
# Label indicating verse history list
ttk.Label(root, text="Verses History: ", font=("Day Roman", 11)).pack()

root.mainloop()
