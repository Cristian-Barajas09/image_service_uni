import os
import dotenv
dotenv.load_dotenv()

def make_url_path(path):
    """Make url path"""
    return f'/api/{os.getenv("API_VERSION")}/{path}'
