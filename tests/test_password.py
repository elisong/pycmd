import string
import subprocess

import pyperclip


class TestPassword:
    def test_password_length(self):
        subprocess.run(["python", "-m", "pycmd.password", "-n", "16"], capture_output=False)
        result = pyperclip.paste()
        assert len(result) == 16

    def test_password_no_upper(self):
        subprocess.run(["python", "-m", "pycmd.password", "-n", "16", "--no-upper"], capture_output=False)
        result = [char for char in pyperclip.paste() if char in string.ascii_uppercase]
        assert len(result) == 0

    def test_password_has_upper(self):
        subprocess.run(["python", "-m", "pycmd.password", "-n", "16"], capture_output=False)
        result = [char for char in pyperclip.paste() if char in string.ascii_uppercase]
        assert len(result) > 0

    def test_password_no_spec(self):
        subprocess.run(["python", "-m", "pycmd.password", "-n", "16", "--no-spec"], capture_output=False)
        result = [char for char in pyperclip.paste() if char in "!@#$%^&*"]
        assert len(result) == 0

    def test_password_has_spec(self):
        subprocess.run(["python", "-m", "pycmd.password", "-n", "16"], capture_output=False)
        result = [char for char in pyperclip.paste() if char in "!@#$%^&*"]
        assert len(result) > 0
