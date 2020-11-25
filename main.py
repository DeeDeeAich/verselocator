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
root.geometry("600x100")
root.iconbitmap("icon.ico")

# Creates the Entry widget verse_input that takes the user-requested verse
verse_input = ttk.Entry(root, width=30)
verse_input.pack()


def on_click():
    # Grabs the text put in the entry widget verse_input and stores it in a variable called location
    location = verse_input.get()
    # Deletes all the text entered in the entry widget to give visual effect
    verse_input.delete(0, END)

    # Creates a new window
    root2 = Toplevel(root)
    root2.title("Verse")
    root2.iconbitmap("icon.ico")

    # Uses the requests library to grab the inputted verse and search for it in the ESV API
    verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={location}", headers=api_key)
    verse = verse.text
    # Uses the json library to store verse as a dictionary. When making a request to the API, it stores it in an object
    # called requests.models.Response
    verse = json.loads(verse)

    # Creates a label in the window that uses the key "passages" and the 0th index of "passages" as the text
    verse_text = Label(root2, text=verse["passages"][0], font=("Cardo", 10))
    verse_text.pack(fill="both", expand=1)


# Creates label for requesting verses notice
ttk.Label(root, font=("Arial", 7), text="Unless otherwise indicated, all Scripture quotations are from the ESV® Bible "
                                        "(The Holy Bible, English Standard Version®), \ncopyright © 2001 by Crossway, " 
                                        "a publishing ministry of Good News Publishers. Used by permission. All "
                                        "rights reserved. \nYou may not copy or download more than 500 consecutive "
                                        "verses of the ESV Bible or more than one half of any book of the ESV "
                                        "Bible.").pack()
ttk.Button(root, text="Ok", command=on_click).pack()

root.mainloop()
