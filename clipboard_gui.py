import tkinter as tk
import pyperclip
import time
import threading
from collections import OrderedDict

# Use OrderedDict to maintain order + uniqueness
history = OrderedDict()
MAX_HISTORY = 20
_clearing = False
_copying_back = False

def monitor_clipboard(listbox):
    """Background thread: watches clipboard & updates GUI"""
    global _clearing, _copying_back

    while True:
        try:
            text = pyperclip.paste()
            if text and text.strip() and not _clearing and not _copying_back:
                
                # If item already exists, remove it first (so it goes to end)
                if text in history:
                    del history[text]
                    print(f" Moving to top: {text[:30]}...")
                else:
                    print(f" Added to history: {text[:30]}...")
                
                # Add to end (most recent)
                history[text] = True
                
                # Keep size limited
                while len(history) > MAX_HISTORY:
                    history.popitem(last=False)  # Remove oldest
                
                # Refresh GUI
                listbox.after(0, lambda: refresh_listbox(listbox))
                
        except Exception as e:
            print(f"Clipboard error: {e}")
        time.sleep(0.5)

def refresh_listbox(listbox):
    """Refresh entire listbox with current history"""
    listbox.delete(0, tk.END)
    # Show most recent first (reverse the OrderedDict)
    for item in reversed(list(history.keys())):
        display_text = item[:70] + ("..." if len(item) > 70 else "")
        listbox.insert(tk.END, display_text)

def copy_selected(listbox):
    """Copy selected item back to clipboard"""
    global _copying_back
    
    try:
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            # Get items in reverse order (most recent first in display)
            items_list = list(reversed(list(history.keys())))
            selected_text = items_list[index]
            
            # Temporarily disable monitoring
            _copying_back = True
            pyperclip.copy(selected_text)
            
            print(f" Copied back: {selected_text[:50]}")
            
            # Re-enable after delay
            def re_enable():
                global _copying_back
                time.sleep(1.0)
                _copying_back = False
            
            threading.Thread(target=re_enable, daemon=True).start()
            
    except Exception as e:
        print(f"Copy failed: {e}")

def clear_history(listbox):
    """Clear history + listbox"""
    global history, _clearing
    _clearing = True
    history.clear()  # Clear the OrderedDict
    pyperclip.copy("")
    listbox.delete(0, tk.END)
    time.sleep(0.6)
    _clearing = False
    print(" History cleared!")

def on_double_click(event, listbox):
    """Double-click to copy"""
    try:
        index = listbox.nearest(event.y)
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
        listbox.activate(index)
        listbox.after(10, lambda: copy_selected(listbox))
    except Exception as e:
        print(f"Double-click failed: {e}")

def main():
    root = tk.Tk()
    root.title(" Unique Clipboard Manager")
    root.geometry("500x400")
    
    # Keep window always on top
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.95)

    label = tk.Label(root, text=" Unique Clipboard History", font=("Arial", 14))
    label.pack(pady=10)

    # Scrollable listbox
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, font=("Arial", 11))
    listbox.pack(fill=tk.BOTH, expand=True)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    # Double-click functionality
    listbox.bind('<Double-1>', lambda event: on_double_click(event, listbox))

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    # Toggle always-on-top
    def toggle_topmost():
        current = root.attributes('-topmost')
        root.attributes('-topmost', not current)
        topmost_btn.config(text=" Pin" if not current else " Unpin", 
                          bg="lightgreen" if not current else "lightyellow")
    
    topmost_btn = tk.Button(btn_frame, text=" Unpin", command=toggle_topmost, bg="lightyellow")
    topmost_btn.pack(side=tk.LEFT, padx=5)

    copy_btn = tk.Button(btn_frame, text=" Copy Selected", command=lambda: copy_selected(listbox), bg='lightblue')
    copy_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(btn_frame, text=" Clear History", command=lambda: clear_history(listbox), bg='lightcoral')
    clear_btn.pack(side=tk.LEFT, padx=5)

    quit_btn = tk.Button(btn_frame, text=" Quit", command=root.destroy, bg='lightgray')
    quit_btn.pack(side=tk.LEFT, padx=5)

    # Instructions
    info_label = tk.Label(root, text=" Only unique items stored! Double-click to copy quickly!", 
                         font=("Arial", 10), fg="green")
    info_label.pack(pady=(0, 5))

    print(" Unique Clipboard Manager Started!")
    print(" Only unique values will be stored!")
    print(" Duplicates will move to the top instead of creating copies!")

    # Start monitoring
    threading.Thread(target=monitor_clipboard, args=(listbox,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()