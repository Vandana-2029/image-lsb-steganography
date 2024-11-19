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

# Example usage
if __name__ == "__main__":

    print("What do you want?")
    print("1) Hide message in image")
    print("2) Retrieve message from image")
    choice = int(input())
    img_path = input("Image Path: ")

    if choice == 1:
        msg_path = input("Message File Path: ")

        # Check if the file is a .txt file
        if not msg_path.endswith(".txt"):
            print("Error: The message file must be a .txt file.")
        else:
            # Read the content of the file into a variable
            try:
                with open(msg_path, "r") as file:
                    msg = file.read()  # Read the entire file content into a string

                # Hide a message inside the image
                hide_message(img_path, msg, img_path)
                print("Message hidden successfully!")
            except FileNotFoundError:
                print("Error: The specified file does not exist.")
    elif choice == 2:
        try:
            # Extract the hidden message from the image
            hidden_message = unhide_message(img_path)
            print("The hidden message is:")
            print(hidden_message)
        except FileNotFoundError:
            print("Error: The specified image does not exist.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
