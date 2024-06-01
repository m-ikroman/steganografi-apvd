from flask import Flask, render_template, request, redirect, url_for
import os
from apvd import embed_message, extract_message

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['GET', 'POST'])
def embed():
    if request.method == 'POST':
        message = request.form['message']
        image = request.files['image']
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'embedded_' + image.filename)
        embed_message(image_path, message, output_path)
        
        return render_template('embed.html', output_image=output_path)
    
    return render_template('embed.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        image = request.files['image']
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        
        message_length = int(request.form['message_length'])
        extracted_message = extract_message(image_path, message_length)
        
        return render_template('extract.html', extracted_message=extracted_message)
    
    return render_template('extract.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
