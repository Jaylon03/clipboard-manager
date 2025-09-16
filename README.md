# Clipboard Manager

A lightweight GUI clipboard manager that tracks your copy history and prevents duplicates.

## Features

- **Clipboard History** - Automatically tracks everything you copy  
- **No Duplicates** - Unique items only (duplicates move to top)  
- **Quick Copy** - Double-click any item to copy it back  
- **Always on Top** - Toggle pinning with the pin button  
- **Clear History** - One-click to clear all history  
- **Smart Memory** - Limits to 20 most recent items  

## Quick Start (Python Users)

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/clipboard-manager.git
   cd clipboard-manager
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python clipboard_manager.py
   ```

4. **Start copying!** The app automatically tracks everything you copy.

## Quick Start (Windows .exe Users)

1. Download the latest `.exe` from the [Releases](https://github.com/jaylon03/clipboard-manager/releases) section
2. Double-click to launch — no Python installation required
3. Start copying! The GUI will track your clipboard automatically

## Usage

- Copy items normally (`Ctrl+C`) — they appear in the list automatically
- Double-click any item in the list to copy it back to clipboard
- Click "Copy Selected" button after selecting an item
- Pin/Unpin the window to stay on top of other apps
- Clear History to remove all tracked items

## Requirements

- Python 3.6+
- pyperclip library
- tkinter (usually included with Python)
- keyboard library

Install dependencies with:
```bash
pip install -r requirements.txt
```

**Optional:** If you don't have `requirements.txt`, you can manually install dependencies:
```bash
pip install pyperclip keyboard
```

## Tips

- Keep the window small and pinned for easy access
- Double-clicking is faster than using the copy button
- The window is slightly transparent when pinned to be less intrusive
- Most recent items appear at the top of the list

## Creating requirements.txt

To make it easier for others to install dependencies, create a `requirements.txt` in your repo with the following contents:

```
pyperclip
keyboard
```

Then users can just run:
```bash
pip install -r requirements.txt
```