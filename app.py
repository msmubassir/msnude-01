from flask import Flask, request, render_template, redirect, url_for
from utils import save_image, is_image_safe

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin_upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
        image = request.files['image']
        label = request.form.get('label')  # Assuming a form input for label (e.g., 'nude', 'not_nude')
        if image:
            try:
                save_image(image, label, app.config['UPLOAD_FOLDER'])
                return "File uploaded successfully."
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
                
                # Check if the uploaded image is safe (not 'nude')
                safe = is_image_safe(filepath)
                
                if safe:
                    result_message = "It's not nude."
                else:
                    result_message = "It's nude."
                
                return render_template('user_upload.html', message=result_message)
            except Exception as e:
                print(f"Error saving image: {e}")
                return "Error processing upload", 500
    return render_template('user_upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
