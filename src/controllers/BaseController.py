from helpers.config import get_settings, Settings
from fastapi import Depends
import os
import random
import string

class BaseController:
    def __init__(self, Settings: Settings = Depends(get_settings)):
        self.Settings = Settings

        self.base_path = os.path.join(os.path.dirname(__file__), "..")
        self.files_path = os.path.join(self.base_path, "assets/files")

    def generate_random_string(self, length: int = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))