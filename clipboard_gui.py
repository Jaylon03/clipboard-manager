import tkinter as tk
import pyperclip
import time
import threading
from collections import OrderedDict
import keyboard

# Use OrderedDict to maintain order + uniqueness
history = OrderedDict()
MAX_HISTORY = 20
_clearing = False
_copying_back = False
current_index = 0
auto_advance_enabled = False
last_clipboard_change_time = 0
_auto_advancing = False  # New flag to prevent monitor interference during auto-advance
_last_auto_advance_text = ""  # Track what was last set by auto-advance
_paste_sequence_started = False  # Track if we're in an active paste sequence

def monitor_clipboard(listbox):
    """Background thread: watches clipboard & updates GUI"""
    global _clearing, _copying_back, current_index, last_clipboard_change_time, _auto_advancing, _last_auto_advance_text, _paste_sequence_started

    while True:
        try:
            text = pyperclip.paste()
            current_time = time.time()
            
            # Don't process clipboard changes during auto-advance or manual copying
            if text and text.strip() and not _clearing and not _copying_back and not _auto_advancing:
                
                # Check if this is the same text we just set via auto-advance
                if text == _last_auto_advance_text and current_time - last_clipboard_change_time < 3.0:
                    print(f"Ignoring auto-advance echo: {text[:30]}...")
                    continue
                
                # Check if this might be a paste of existing history item
                # If auto-advance is enabled and this text is already in history,
                # and it happened recently after our last clipboard change,
                # then it's likely a paste - don't re-add it
                if (auto_advance_enabled and 
                    text in history and 
                    current_time - last_clipboard_change_time < 2.0):
                    continue
                
                # If item already exists and this isn't a recent paste, move it to end
                if text in history:
                    del history[text]
                   
                else:
                    print(f"Added to history: {text[:30]}...")
                
                # Add to end (most recent)
                history[text] = True
                last_clipboard_change_time = current_time
                
                # Keep size limited
                while len(history) > MAX_HISTORY:
                    history.popitem(last=False)
                
                # Reset to start of sequence for next paste session
                current_index = 0  # Start from the oldest item
                _paste_sequence_started = False  # Reset paste sequence
                
                # Clear the auto-advance tracking since this is a new item
                _last_auto_advance_text = ""
                
                # Refresh GUI
                listbox.after(0, lambda: refresh_listbox(listbox))
                
        except Exception as e:
            print(f"Clipboard error: {e}")
        time.sleep(0.5)

def monitor_paste_events():
    """Monitor for Ctrl+V paste events"""
    global auto_advance_enabled
    
    def on_paste():
        if auto_advance_enabled and history:
            # Advance to next item FIRST, then let the normal paste happen
            advance_to_next_item()
            # Small delay to ensure clipboard is updated before paste
            return  # Let the normal Ctrl+V proceed with our updated clipboard
    
    try:
        # Use suppress=False so the normal Ctrl+V still works after we update clipboard
        keyboard.add_hotkey("ctrl+v", on_paste, suppress=False)
        print("Paste monitoring enabled - Ctrl+V will auto-advance!")
        return True
    except Exception as e:
        print(f"Could not monitor paste events: {e}")
        return False

def advance_to_next_item():
    """Automatically advance to the next item in history"""
    global current_index, _copying_back, _auto_advancing, last_clipboard_change_time, _last_auto_advance_text, _paste_sequence_started
    
    if not history or not auto_advance_enabled:
        return
    
    items_list = list(history.keys())
    if len(items_list) == 0:
        return
    
    # Move to next item BEFORE setting clipboard
    if not _paste_sequence_started:
        # First paste: start at index 0 (oldest item)
        current_index = 0
        _paste_sequence_started = True
    else:
        # Subsequent pastes: move to next item
        current_index = (current_index + 1) % len(items_list)
    
    # Set flags to prevent monitor interference
    _auto_advancing = True
    _copying_back = True
    
    current_text = items_list[current_index]
    
    # Update clipboard with current item
    last_clipboard_change_time = time.time()
    _last_auto_advance_text = current_text
    pyperclip.copy(current_text)
    
   
    
    # Re-enable monitoring after delay
    def re_enable():
        global _copying_back, _auto_advancing
        time.sleep(1.2)  # Longer delay to ensure paste completes
        _copying_back = False
        _auto_advancing = False
    
    threading.Thread(target=re_enable, daemon=True).start()

def refresh_listbox(listbox):
    """Refresh entire listbox with current history"""
    listbox.delete(0, tk.END)
    items_list = list(history.keys())
    
    if not items_list:
        return
    
    # Show most recent first in display, but track actual order
    for i, item in enumerate(reversed(items_list)):
        display_text = item[:70] + ("..." if len(item) > 70 else "")
        
        # Highlight current active item (convert current_index to display order)
        actual_item_index = len(items_list) - 1 - i  # Convert display index to actual index
        if actual_item_index == current_index:
            display_text = f"-> {display_text}"
        
        listbox.insert(tk.END, display_text)
    
    # Highlight the active item in the listbox
    if items_list:
        # Convert current_index to display index (reversed order)
        active_display_index = len(items_list) - 1 - current_index
        if 0 <= active_display_index < listbox.size():
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(active_display_index)
            listbox.see(active_display_index)

def toggle_auto_advance():
    """Toggle auto-advance mode"""
    global auto_advance_enabled, _paste_sequence_started
    auto_advance_enabled = not auto_advance_enabled
    _paste_sequence_started = False  # Reset paste sequence when toggling
    
    if auto_advance_enabled:
        print("Auto-advance enabled! Each Ctrl+V will move to the next item automatically!")
        print("   Sequence: Copy 1,2,3,4 -> Paste 1 -> Paste 2 -> Paste 3 -> Paste 4 -> Paste 1...")
    else:
        print("Auto-advance disabled - normal clipboard behavior")
    
    return auto_advance_enabled

def reset_to_newest():
    """Reset to the most recent clipboard item"""
    global current_index, _copying_back, _auto_advancing, last_clipboard_change_time, _paste_sequence_started
    if history:
        current_index = len(history) - 1
        _paste_sequence_started = False  # Reset paste sequence
        items_list = list(history.keys())
        newest_item = items_list[current_index]
        
        _copying_back = True
        _auto_advancing = True  # Prevent monitor interference
        last_clipboard_change_time = time.time()
        pyperclip.copy(newest_item)
        
        print(f"Reset to newest: {newest_item[:50]}")
        
        def re_enable():
            global _copying_back, _auto_advancing
            time.sleep(1.0)
            _copying_back = False
            _auto_advancing = False
        
        threading.Thread(target=re_enable, daemon=True).start()

def reset_to_start_sequence():
    """Reset to start of paste sequence (oldest item)"""
    global current_index, _copying_back, _auto_advancing, last_clipboard_change_time, _paste_sequence_started
    if history:
        current_index = 0  # Start from oldest
        _paste_sequence_started = False  # Reset paste sequence
        items_list = list(history.keys())
        oldest_item = items_list[current_index]
        
        _copying_back = True
        _auto_advancing = True  # Prevent monitor interference
        last_clipboard_change_time = time.time()
        pyperclip.copy(oldest_item)
        
        print(f"Reset to start of sequence: {oldest_item[:50]}")
        
        def re_enable():
            global _copying_back, _auto_advancing
            time.sleep(1.0)
            _copying_back = False
            _auto_advancing = False
        
        threading.Thread(target=re_enable, daemon=True).start()

def copy_selected(listbox):
    """Copy selected item back to clipboard"""
    global _copying_back, current_index, last_clipboard_change_time, _auto_advancing, _paste_sequence_started
    
    try:
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            items_list = list(reversed(list(history.keys())))
            selected_text = items_list[index]
            
            # Update current index to match selection (convert from display order to actual order)
            actual_index = len(history) - 1 - index
            current_index = actual_index
            _paste_sequence_started = False  # Reset paste sequence
            
            _copying_back = True
            _auto_advancing = True  # Prevent monitor interference
            last_clipboard_change_time = time.time()
            pyperclip.copy(selected_text)
            
           
            
            def re_enable():
                global _copying_back, _auto_advancing
                time.sleep(1.0)
                _copying_back = False
                _auto_advancing = False
            
            threading.Thread(target=re_enable, daemon=True).start()
            
    except Exception as e:
        print(f"Copy failed: {e}")

def clear_history(listbox):
    """Clear history + listbox"""
    global history, _clearing, current_index, _paste_sequence_started
    _clearing = True
    history.clear()
    current_index = 0
    _paste_sequence_started = False
    pyperclip.copy("")
    listbox.delete(0, tk.END)
    time.sleep(0.6)
    _clearing = False
    

def on_double_click(event, listbox):
    """Double-click to copy and set as current"""
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
    root.title("Auto-Advance Clipboard Manager")
    root.geometry("650x500")
    
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.95)

    # Title
    title_frame = tk.Frame(root)
    title_frame.pack(pady=10)
    
    title_label = tk.Label(title_frame, text="Auto-Advance Clipboard Manager", 
                          font=("Arial", 14, "bold"))
    title_label.pack()

    # Status frame
    status_frame = tk.Frame(root)
    status_frame.pack(pady=5)
    
    status_label = tk.Label(status_frame, text="Auto-Advance: OFF", 
                           font=("Arial", 11), fg="red", bg="lightyellow")
    status_label.pack()

    def update_status():
        status_text = "Auto-Advance: ON" if auto_advance_enabled else "Auto-Advance: OFF"
        status_color = "green" if auto_advance_enabled else "red"
        status_label.config(text=status_text, fg=status_color)
        root.after(1000, update_status)  # Update every second
    
    update_status()

    # Listbox frame
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, font=("Arial", 11))
    listbox.pack(fill=tk.BOTH, expand=True)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    listbox.bind('<Double-1>', lambda event: on_double_click(event, listbox))

    # Control buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=5)

    def toggle_button():
        enabled = toggle_auto_advance()
        toggle_advance_btn.config(
            text="Disable Auto-Advance" if enabled else "Enable Auto-Advance",
            bg="lightgreen" if enabled else "lightcoral"
        )
        refresh_listbox(listbox)  # Update display

    toggle_advance_btn = tk.Button(control_frame, text="Enable Auto-Advance", 
                                  command=toggle_button, 
                                  bg='lightcoral', font=("Arial", 10, "bold"))
    toggle_advance_btn.pack(side=tk.LEFT, padx=5)

    reset_btn = tk.Button(control_frame, text="Reset to Newest", 
                         command=lambda: [reset_to_newest(), root.after(100, lambda: refresh_listbox(listbox))], 
                         bg='lightyellow')
    reset_btn.pack(side=tk.LEFT, padx=5)

    # New button to reset to start of sequence
    reset_sequence_btn = tk.Button(control_frame, text="Reset to Start", 
                                  command=lambda: [reset_to_start_sequence(), root.after(100, lambda: refresh_listbox(listbox))], 
                                  bg='lightgreen')
    reset_sequence_btn.pack(side=tk.LEFT, padx=5)

    # Standard buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    copy_btn = tk.Button(btn_frame, text="Copy Selected", 
                        command=lambda: [copy_selected(listbox), root.after(100, lambda: refresh_listbox(listbox))], 
                        bg='lightblue')
    copy_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(btn_frame, text="Clear History", 
                         command=lambda: clear_history(listbox), bg='lightcoral')
    clear_btn.pack(side=tk.LEFT, padx=5)

    quit_btn = tk.Button(btn_frame, text="Quit", command=root.destroy, bg='lightgray')
    quit_btn.pack(side=tk.LEFT, padx=5)

    # Instructions
    instructions = [
        "Instructions:",
        "1. Copy multiple items (1, 2, 3, 4)",
        "2. Enable Auto-Advance mode", 
        "3. Go where you want to paste",
        "4. Press Ctrl+V repeatedly: pastes 1, then 2, then 3, then 4, then cycles..."
    ]
    
    for instruction in instructions:
        info_label = tk.Label(root, text=instruction, font=("Arial", 9), fg="gray")
        info_label.pack()

    # Start monitoring threads
    threading.Thread(target=monitor_clipboard, args=(listbox,), daemon=True).start()
    
    # Try to monitor paste events
    paste_monitoring = monitor_paste_events()
    if not paste_monitoring:
        pass  # No action needed if paste monitoring fails
        


    root.mainloop()

if __name__ == "__main__":
    main()