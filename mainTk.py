import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
# Part 1: Hide text message inside the image
def hide_message(image_path, text_message, output_image_path):
    # Convert the text message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in text_message)
    binary_message += '1111111111111110'  # Add a delimiter to mark the end of the message
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Ensure the image is in RGB mode
    pixels = image.load()
    
    # Get image dimensions
    width, height = image.size
    data_index = 0
    
    # Loop through each pixel
    for y in range(height):
        for x in range(width):
            # Get the current pixel (R, G, B)
            r, g, b = pixels[x, y]
            
            # Modify the last bit of each color component with the binary message
            if data_index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[data_index])  # Replace the last bit of R
                data_index += 1
            if data_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[data_index])  # Replace the last bit of G
                data_index += 1
            if data_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[data_index])  # Replace the last bit of B
                data_index += 1
            
            # Update the pixel with the new RGB values
            pixels[x, y] = (r, g, b)
            
            # Stop if all bits have been encoded
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break
    
    # Save the modified image
    image.save(output_image_path)
    print(f"Message hidden successfully in {output_image_path}")

# Part 2: Extract the hidden message from the image
def unhide_message(image_path):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Ensure the image is in RGB mode
    pixels = image.load()
    
    # Get image dimensions
    width, height = image.size
    binary_message = ''
    
    # Loop through each pixel to extract the LSBs
    for y in range(height):
        for x in range(width):
            # Get the current pixel (R, G, B)
            r, g, b = pixels[x, y]
            
            # Extract the last bit of each color component
            binary_message += str(r & 1)  # Last bit of R
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':  # End delimiter
                break
            binary_message += str(g & 1)  # Last bit of G
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':  # End delimiter
                break
            binary_message += str(b & 1)  # Last bit of B
            
            # Check if we've reached the delimiter (end of message)
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':  # End delimiter
                break
        if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':  # Check after the inner loop
            binary_message = binary_message[:-16]  # Remove the delimiter
            break
    
    # Convert binary message to text
    text_message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        text_message += chr(int(byte, 2))  # Convert binary to text
    
    return text_message

# Function to hide the message in the image
def hide_message_gui():
    # Open file dialog to select an image
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return

    # Ask for the message to hide
    message = message_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Message cannot be empty!")
        return

    # Save the output image
    output_path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if not output_path:
        return

    try:
        hide_message(image_path, message, output_path)
        messagebox.showinfo("Success", f"Message hidden successfully in {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to extract the hidden message from the image
def unhide_message_gui():
    # Open file dialog to select an image
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return

    try:
        hidden_message = unhide_message(image_path)
        messagebox.showinfo("Hidden Message", f"The hidden message is:\n\n{hidden_message}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Tkinter GUI setup
root = tk.Tk()
root.title("Image Steganography Tool")
root.geometry("500x300")
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="Image Steganography Tool", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Instruction Label
instruction_label = tk.Label(root, text="Enter a message to hide or retrieve a hidden message from an image.", font=("Arial", 10))
instruction_label.pack(pady=5)

# Text Entry for Message
message_label = tk.Label(root, text="Message to Hide (only for Hide Message):", font=("Arial", 10))
message_label.pack(pady=5)
message_entry = tk.Text(root, height=5, width=40)
message_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

hide_button = tk.Button(button_frame, text="Hide Message", font=("Arial", 12), bg="lightblue", command=hide_message_gui)
hide_button.grid(row=0, column=0, padx=10)

retrieve_button = tk.Button(button_frame, text="Retrieve Message", font=("Arial", 12), bg="lightgreen", command=unhide_message_gui)
retrieve_button.grid(row=0, column=1, padx=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="lightcoral", command=root.quit)
exit_button.pack(pady=10)

# Mainloop
root.mainloop()
