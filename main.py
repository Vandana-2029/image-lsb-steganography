from PIL import Image
import argparse

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


# Define the functions hide_message and unhide_message here or import them
# Example functions:
# from steganography_tool import hide_message, unhide_message
def main():
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    parser.add_argument(
        "action",
        choices=["hide", "retrieve"],
        help="Choose 'hide' to hide a message or 'retrieve' to extract a hidden message.",
    )
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument(
        "--message",
        help="The message to hide in the image (required for 'hide' action).",
    )

    args = parser.parse_args()

    if args.action == "hide":
        if not args.message:
            print("Error: --message is required for the 'hide' action.")
            return

        # Hide the message in the image
        try:
            hide_message(args.image_path, args.message, args.image_path)
        except FileNotFoundError:
            print("Error: The specified image file does not exist.")
    elif args.action == "retrieve":
        # Extract the hidden message from the image
        try:
            hidden_message = unhide_message(args.image_path)
            print(hidden_message)
        except FileNotFoundError:
            print("Error: The specified image file does not exist.")
    else:
        print("Invalid action. Use 'hide' or 'retrieve'.")

if __name__ == "__main__":
    main()