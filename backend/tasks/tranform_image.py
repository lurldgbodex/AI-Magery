import shutil


def transform_image(image_path: str, output_path: str):
    shutil.copy(image_path, output_path)
