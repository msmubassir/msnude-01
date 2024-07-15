from flask import Flask, request, render_template, redirect, url_for
import os
from utils import save_image, train_model, predict_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Admin upload page
@app.route('/admin_upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
        image = request.files['image']
        label = request.form['label']
        if image and label in ['nude', 'not_nude']:
            filepath = save_image(image, label, app.config['UPLOAD_FOLDER'])
            train_model(app.config['UPLOAD_FOLDER'])
        return redirect(url_for('admin_upload'))
    return render_template('admin_upload.html')

# User upload page
@app.route('/user_upload', methods=['GET', 'POST'])
def user_upload():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            filepath = save_image(image, None, app.config['UPLOAD_FOLDER'])
            prediction = predict_image(filepath)
            return render_template('result.html', prediction=prediction)
    return render_template('user_upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
