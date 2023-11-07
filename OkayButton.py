# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:48:31 2022
Simple test of tkinter package and GUIs
@author: Jonas
"""

import tkinter as tk

def on_button_click():
    # Exit the GUI
    root.destroy()

# Create the main window
root = tk.Tk()

# Create a button
button = tk.Button(text="Okay!", command=on_button_click)
button.pack()

# Run the GUI
root.mainloop()
