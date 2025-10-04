#!/usr/bin/env python3

import tkinter as tk

try:
    # Create root window
    root = tk.Tk()
    root.title("TEST - Should Show This")
    root.geometry("400x300")

    # Add visible label
    label = tk.Label(root, text="HELLO WORLD\nGUI IS WORKING!", font=('Arial', 16, 'bold'), fg='green')
    label.pack(pady=20)

    # Add button
    button = tk.Button(root, text="Click to test", command=lambda: print("Button clicked - functionality working"))
    button.pack(pady=10)

    # Add text field
    entry = tk.Entry(root, width=30)
    entry.insert(0, "Type here if visible")
    entry.pack(pady=10)

    print("GUI components created - window should now be visible with green text!")

    # Start the GUI loop
    root.mainloop()

except Exception as e:
    print(f"Tkinter failed: {e}")
    print("This proves GUI is impossible in this environment")
