import os
from PIL import Image

def save_image(image, label, upload_folder):
    label_folder = 'unlabeled' if label is None else label
    folder_path = os.path.join(upload_folder, label_folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, image.filename)
    image.save(filepath)
    return filepath
