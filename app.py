from flask import Flask, request, render_template, redirect, url_for
import os
from utils import save_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/admin_upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
        image = request.files['image']
        label = request.form['label']
        if image and label in ['nude', 'not_nude']:
            try:
                filepath = save_image(image, label, app.config['UPLOAD_FOLDER'])
                # Additional processing or model training can go here
                return redirect(url_for('admin_upload'))
            except Exception as e:
                print(f"Error saving image: {e}")
                return "Error processing upload", 500
    return render_template('admin_upload.html')

@app.route('/user_upload', methods=['GET', 'POST'])
def user_upload():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            try:
                filepath = save_image(image, None, app.config['UPLOAD_FOLDER'])
                # Perform prediction or processing here
                return "File uploaded successfully"
            except Exception as e:
                print(f"Error saving image: {e}")
                return "Error processing upload", 500
    return render_template('user_upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
