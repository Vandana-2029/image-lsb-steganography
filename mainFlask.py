from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'secret_key'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Function to hide the message in the image
def hide_message(image_path, text_message, output_image_path):
    binary_message = ''.join(format(ord(c), '08b') for c in text_message)
    binary_message += '1111111111111110'  # Add a delimiter to mark the end of the message
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = image.load()
    
    width, height = image.size
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if data_index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break
    
    image.save(output_image_path)


# Function to retrieve the hidden message
def unhide_message(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = image.load()
    
    width, height = image.size
    binary_message = ''
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
                break
            binary_message += str(g & 1)
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
                break
            binary_message += str(b & 1)
            if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
                break
        if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
            binary_message = binary_message[:-16]
            break
    
    text_message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        text_message += chr(int(byte, 2))
    
    return text_message


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hide', methods=['POST'])
def hide():
    if 'image' not in request.files or not request.form['message']:
        return redirect(url_for('index'))
    
    image = request.files['image']
    message = request.form['message']
    filename = secure_filename(image.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    
    output_filename = f"hidden_{filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    hide_message(input_path, message, output_path)
    
    return send_file(output_path, as_attachment=True)


@app.route('/retrieve', methods=['POST'])
def retrieve():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    image = request.files['image']
    filename = secure_filename(image.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    
    try:
        hidden_message = unhide_message(input_path)
        return render_template('index.html', hidden_message=hidden_message)
    except Exception as e:
        return render_template('index.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
