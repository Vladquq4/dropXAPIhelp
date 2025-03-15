import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import requests

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/awb"  # Update with your actual server address

def fetch_qr_data():
    """Fetch QR data from FastAPI and return as a list."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise error if request failed
        data = response.json().get("uris", [])  # Extract array from JSON
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return ["Error fetching data"]  # Default fallback

# Initialize Tkinter
root = tk.Tk()
root.title("QR Code Carousel")
root.geometry("400x500")
root.minsize(300, 400)

# Fetch data from API
data = fetch_qr_data()

# Generate QR Code images
def generate_qr_images():
    return [ImageTk.PhotoImage(qrcode.make(text).resize((200, 200), Image.Resampling.LANCZOS)) for text in data]

qr_images = generate_qr_images()

# Ensure there's at least one image
if not qr_images:
    default_qr = qrcode.make("No Data Available").resize((200, 200), Image.Resampling.LANCZOS)
    qr_images.append(ImageTk.PhotoImage(default_qr))

total_qr = len(qr_images)
current_index = 0

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Center QR Code
qr_label = tk.Label(main_frame, image=qr_images[current_index])
qr_label.pack(expand=True)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=10)

# Function to switch QR codes
def show_qr(index):
    global current_index
    if qr_images:
        current_index = index % len(qr_images)
        qr_label.config(image=qr_images[current_index])

def remove_current_qr():
    global current_index, qr_images, data
    if qr_images:
        del qr_images[current_index]
        del data[current_index]
        if not qr_images:
            default_qr = qrcode.make("No Data Available").resize((200, 200), Image.Resampling.LANCZOS)
            qr_images.append(ImageTk.PhotoImage(default_qr))
        current_index = current_index % len(qr_images)
        qr_label.config(image=qr_images[current_index])

# Navigation Buttons
btn_prev = ttk.Button(button_frame, text="⬅ Prev", command=lambda: show_qr(current_index - 1), width=12)
btn_prev.pack(side="left", expand=True, padx=10, pady=5)

btn_remove = ttk.Button(button_frame, text="Remove", command=remove_current_qr, width=12)
btn_remove.pack(side="left", expand=True, padx=10, pady=5)

btn_next = ttk.Button(button_frame, text="Next ➡", command=lambda: show_qr(current_index + 1), width=12)
btn_next.pack(side="right", expand=True, padx=10, pady=5)

# Keyboard navigation
def key_pressed(event):
    if event.keysym == "Left":
        show_qr(current_index - 1)
    elif event.keysym == "Right":
        show_qr(current_index + 1)
    elif event.keysym == "Delete":
        remove_current_qr()

root.bind("<Left>", key_pressed)
root.bind("<Right>", key_pressed)
root.bind("<Delete>", key_pressed)

# Run GUI
root.mainloop()
