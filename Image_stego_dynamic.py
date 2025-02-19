import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
from stegano import lsb
import base64


# Function to switch between frames
def show_frame(frame):
    frame.tkraise()  # Bring the selected frame to the top

def generate_key( password ):
    """Generate an encryption key from a password."""
    return base64.urlsafe_b64encode(password.ljust(32).encode()[:32])

def encrypt_message(message, password):
    """Encrypts the message using AES encryption."""
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(hidden_message, password):
    #decrypt message using encryption
    try:
        key = generate_key(password)
        cipher = Fernet(key)
        return cipher.decrypt(hidden_message.encode()).decode()
    except Exception:
        return None

# Function to Hide Message
def hide_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if not file_path:
        return

    message = message_entry.get("1.0", tk.END).strip()
    password = password_entry.get()

    if not message or not password:
        messagebox.showerror("❌ Error", "Message and Password cannot be empty!")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not output_path:
        return

    try:
        encrypted_text: str = encrypt_message(message, password)  # Simple password protection
        secret = lsb.hide(file_path, encrypted_text)
        secret.save(output_path)
        messagebox.showinfo("✅ Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to hide message: {str(e)}")

# Function to Reveal Message
def extract_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if not file_path:
        return

    password = reveal_password_entry.get()
    if not password:
        messagebox.showerror("❌ Error", "Password cannot be empty!")
        return

    try:
        hidden_message = lsb.reveal(file_path)
        if hidden_message:
            decrypted_message = decrypt_message(hidden_message, password)

            if decrypted_message:
                messagebox.showinfo("✅ Success", f"Decrypted message is  {decrypted_message}")
            else:
                messagebox.showerror("❌ Error", "Incorrect Password!")
        else:
            messagebox.showerror("❌ Error", "No hidden message found!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to reveal message: {str(e)}")


# Create Main Tkinter Window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x400")

# Create a container frame
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Configure grid layout for easy switching
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create Frames for Different Pages
home_frame = tk.Frame(container)
hide_frame = tk.Frame(container)
reveal_frame = tk.Frame(container)

# Stack the frames (place them on top of each other)
for frame in (home_frame, hide_frame, reveal_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# ---- Home Page ----
ttk.Label(home_frame, text="Image Steganography", font=("Arial", 20, "bold")).pack(pady=40)
ttk.Button(home_frame, text="Hide Message", command=lambda: show_frame(hide_frame)).pack(pady=20)
ttk.Button(home_frame, text="Reveal Message", command=lambda: show_frame(reveal_frame)).pack(pady=20)


# ---- Hide Message Page ----
hide_title = ttk.Label(hide_frame, text="Hide a Secret Message in Image", font=("Arial", 18))
hide_title.pack(pady=20)

ttk.Label(hide_frame, text="Enter Message:").pack(pady=5)
message_entry = tk.Text(hide_frame, height=4, width=50)
message_entry.pack(pady=5)

ttk.Label(hide_frame, text="Enter Password:").pack(pady=5)
password_entry = ttk.Entry(hide_frame, show="*", width=30)
password_entry.pack(pady=10)

ttk.Label(hide_frame, text="Select Image to hide message:").pack(pady=5)
ttk.Button(hide_frame, text="Choose the Image", command=hide_message, ).pack(pady=10)
ttk.Button(hide_frame, text="Back", command=lambda: show_frame(home_frame)).pack(pady=5)

# ---- Reveal Message Page ----
reveal_title = ttk.Label(reveal_frame, text="Reveal Hidden Message", font=("Arial", 18))
reveal_title.pack(pady=20)

ttk.Label(reveal_frame, text="Enter Password:").pack(pady=5)
reveal_password_entry = ttk.Entry(reveal_frame, show="*", width=30)
reveal_password_entry.pack(pady=10)

ttk.Button(reveal_frame, text="Reveal Message from Image", command=extract_message).pack(pady=10)
ttk.Button(reveal_frame, text="Back", command=lambda: show_frame(home_frame)).pack(pady=5)

# Show Home Page Initially
show_frame(home_frame)

# Run Tkinter Loop
root.mainloop()
