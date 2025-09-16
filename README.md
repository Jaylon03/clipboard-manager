#  Clipboard Manager

A lightweight GUI clipboard manager that tracks your copy history and prevents duplicates.

##  Features

# Clipboard History** - Automatically tracks everything you copy
# No Duplicates** - Unique items only (duplicates move to top)
# Quick Copy** - Double-click any item to copy it back
# Always on Top** - Toggle pinning with the pin button
# Clear History** - One-click to clear all history
# Smart Memory** - Limits to 20 most recent items

##  Quick Start

1. **Install requirements:**
   ```bash
   pip install pyperclip tkinter
   ```

2. **Run the app:**
   ```bash
   python clipboard_manager.py
   ```

3. **Start copying!** The app automatically tracks everything you copy.

##  Usage

- **Copy items** normally (Ctrl+C) - they appear in the list automatically
- **Double-click** any item in the list to copy it back to clipboard
- **Click "Copy Selected"** button after selecting an item
- **Pin/Unpin** the window to stay on top of other apps
- **Clear History** to remove all tracked items

## Requirements

- pip install -r requirements.txt
- Python 3.6+
- `pyperclip` library
- `tkinter` (usually included with Python)

##  Tips

- Keep the window small and pinned for easy access
- Double-clicking is faster than using the copy button
- The window is slightly transparent when pinned to be less intrusive
- Most recent items appear at the top of the list

---
*Built with Python & Tkinter*
