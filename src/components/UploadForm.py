class UploadForm:
    def __init__(self):
        self.files = []

    def add_file(self, file):
        self.files.append(file)
        return json.dumps(self.files)

    def get_files(self):
        return json.dumps(self.files)
