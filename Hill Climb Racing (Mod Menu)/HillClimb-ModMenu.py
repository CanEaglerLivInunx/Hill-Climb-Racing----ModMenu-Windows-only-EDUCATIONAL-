import customtkinter as ctk
import pymem
import pymem.process
import sys

# config
APP_SIZE = "420x220"
FONT = ("Helvetica", 12)

# Globals for pymem
pm = None
module_base = None

# Try to attach to process (safe handling if it fails)
try:
    pm = pymem.Pymem("HillClimbRacing.exe")
    module = pymem.process.module_from_name(pm.process_handle, "HillClimbRacing.exe")
    module_base = module.lpBaseOfDll
except Exception as e:
    pm = None
    module_base = None
    attach_error = str(e)

# memory addresses (kept from your original)
GEMS_ADDRESS = 0x28CAEC
COINS_ADDRESS = 0x28CAD4


# functions
def set_gems_to_99999():
    """Write 99999 to the gems address."""
    if pm is None or module_base is None:
        status.set("Process not attached")
        status_label.configure(text_color="red")
        return

    try:
        pm.write_int(module_base + GEMS_ADDRESS, 99999)
        status.set("Gems set to 99,999")
        status_label.configure(text_color="lightgreen")
    except Exception as e:
        status.set(f"Failed to set gems: {e}")
        status_label.configure(text_color="red")


def set_coins(new_coins: int):
    """
    Write an integer value into the coin address.
    Returns (message, color).
    """
    if pm is None or module_base is None:
        return ("Process not attached", "red")

    try:
        pm.write_int(module_base + COINS_ADDRESS, int(new_coins))
        return (f"Coins set to {new_coins}", "lightgreen")
    except Exception as e:
        return (f"Error writing coins: {e}", "red")


# UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("GemsHack - HillClimbRacing")
app.geometry(APP_SIZE)

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)


# Status variable
status = ctk.StringVar(value="Ready")
status_label = ctk.CTkLabel(frame, textvariable=status, font=FONT, text_color="lightgreen")
status_label.pack(anchor="w", pady=(0, 10))


# Gems button (sets gems to 99,999)
ctk.CTkButton(frame, text="Set Gems to 99,999", font=FONT, command=set_gems_to_99999).pack(anchor="w", pady=6)


# Coins input
ctk.CTkLabel(frame, text="Set Coins", font=FONT).pack(anchor="w", pady=(10, 0))
input_frame = ctk.CTkFrame(frame, fg_color="transparent")
input_frame.pack(fill="x", pady=8)

entry = ctk.CTkEntry(input_frame, placeholder_text="Coins (integer)")
entry.pack(side="left", fill="x", expand=True, padx=(0, 8))


def confirm_coins():
    raw = entry.get()
    try:
        value = int(raw or 0)
        msg, color = set_coins(value)
        status.set(msg)
        status_label.configure(text_color=color)
    except ValueError:
        status.set("Invalid Number!!!")
        status_label.configure(text_color="yellow")


ctk.CTkButton(input_frame, text="Confirm", font=FONT, command=confirm_coins).pack(side="right")


# If the process failed to attach, show an initial error state and disable controls
if pm is None or module_base is None:
    status.set("Could not attach to HillClimbRacing.exe")
    status_label.configure(text_color="red")
    # disable interactive controls
    for w in frame.winfo_children():
        try:
            w.configure(state="disabled")
        except Exception:
            pass
else:
    status.set("Ready")
    status_label.configure(text_color="lightgreen")

app.mainloop()
