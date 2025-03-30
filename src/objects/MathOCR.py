import requests
import json
import time 
import os

class MathOCR:
    options = {
        "conversion_formats": {"html": False, "tex.zip": False},
        "math_inline_delimiters": ["$", "$"],
        "math_display_delimiters":["$$", "$$"],
        "rm_spaces": True,
        "rm_fonts": True
    }

    def __init__(self, pdf_file, ROOT_DIR, options=None):
        self.pdf_file = pdf_file

        self.ROOT_DIR = ROOT_DIR
        self.OUTPUT_DIR = os.path.join(ROOT_DIR, "data/markdown")
        self.INPUT_DIR = os.path.join(ROOT_DIR, "data/material")
        self.SETTINGS = os.path.join(ROOT_DIR, "data/settings.json")

        f = open(self.SETTINGS)
        data = json.load(f) 
        self.app_id = data.get("app_id")
        self.app_key = data.get("app_key")
        f.close()

        if options is not None:
            self.options = options

    def process(self):
        path = os.path.join(self.INPUT_DIR, self.pdf_file)
        url = 'https://api.mathpix.com/v3/pdf'
        r = requests.post(url,
            headers = {
                "app_id": self.app_id,
                "app_key": self.app_key
            },
            data={
                "options_json": json.dumps(self.options)
            },
            files={
                "file": open(path, "rb")
            }
        )
        r = r.json()
        self.pdf_id = r.get("pdf_id")
        return r

    def status(self):
        url = "https://api.mathpix.com/v3/pdf/" + self.pdf_id

        r = requests.get(url,
            headers = {
                "app_id": self.app_id,
                "app_key": self.app_key
            }
         )
        return r.json()

    def download(self):
        url = "https://api.mathpix.com/v3/pdf/" + self.pdf_id + ".mmd"
        response = requests.get(url,
            headers = {
                "app_id": self.app_id,
                "app_key": self.app_key
            }
        )

        filename = os.path.splitext(os.path.basename(self.pdf_file))[0] + ".mmd"
        print("filename:", filename)
        output = os.path.join(self.OUTPUT_DIR, filename)
        print("output:", output)

        # filename = self.path + ".mmd" #ToDo name selfpath without .pdf extension
        with open(output, "w") as f:
            f.write(response.text)
            return filename



