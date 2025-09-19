Clipboard Manager

A lightweight desktop utility that enhances productivity by tracking your clipboard history, removing duplicates, and enabling fast pasting.

Features

Clipboard History – Automatically logs everything you copy.
Duplicate Prevention – Keeps items unique; duplicates are moved to the top.
Instant Paste – Double-click or select an item to copy it back to the clipboard.
Always on Top – Pin the window above other applications.
Clear History – Remove all tracked items with one click.

Memory Optimization – Stores only the 20 most recent items for high performance.
Quick Start

Install dependencies:
pip install pyperclip tkinter


Run the application:
python clipboard_manager.py


Start copying! All copied items are automatically tracked.

Usage

Copy text normally (Ctrl+C); it appears in the app automatically.
Double-click an item to copy it back immediately, or use Copy Selected.
Toggle Always on Top to keep the window visible.
Click Clear History to remove all items.

Requirements
Python 3.6+
pyperclip
tkinter (included with most Python installations)

Tips

Keep the window small and pinned for quick access.
Double-clicking is faster than using the copy button.
The window is slightly transparent when pinned for minimal disruption.
Most recent items always appear at the top.
