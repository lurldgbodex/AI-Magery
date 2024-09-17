from fastapi import UploadFile, HTTPException
from PIL import Image
import io


def validate_image(file: UploadFile):
    """
    method to check if file is valid
    :params file: file to validate
    """

    try:
        Image.open(io.BytesIO(file.file.read()))
        file.file.seek(0)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid image file: {e}")
