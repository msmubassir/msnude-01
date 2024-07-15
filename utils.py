import os
from PIL import Image

def save_image(image, label, upload_folder):
    """
    Save the uploaded image to the specified upload folder.

    Parameters:
    - image: FileStorage object representing the uploaded image.
    - label: Optional label indicating the category of the image (e.g., 'nude', 'not_nude').
    - upload_folder: Path to the folder where images will be saved.

    Returns:
    - filepath: Path where the image file is saved.
    """
    label_folder = 'unlabeled' if label is None else label
    folder_path = os.path.join(upload_folder, label_folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, image.filename)
    image.save(filepath)
    return filepath

def is_image_safe(filepath):
    """
    Placeholder function to check if an image is safe (e.g., not 'nude').

    Parameters:
    - filepath: Path to the image file.

    Returns:
    - safe: Boolean indicating if the image is safe.
    """
    # Implement your logic here to check if the image is safe
    # Example: Use your trained model to predict if the image is 'nude'
    # For demonstration, let's assume all images are safe in this example
    return True

def delete_image(filepath):
    """
    Delete an image file.

    Parameters:
    - filepath: Path to the image file.
    """
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(f"File not found: {filepath}")
