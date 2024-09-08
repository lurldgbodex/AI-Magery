from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    The default home page url of the api. displays a welcome message when a get request is received.
    """
    return {
        "message": "Welcome to the Image Transformation API!"
    }
