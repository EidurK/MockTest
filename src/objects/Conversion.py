import json

class Conversion:
    def __init__(self, path):
        self.path = path
        f = open(path)
        self.data = json.load(f) 
        f.close()

    def __del__(self):
        print("Writing into", self.path)
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data))

    def get(self, file):
        return self.data.get(file)

    def add(self, file_pdf, file_mmd):
        print("conversion added", file_pdf, "->",file_mmd)
        self.data.update({file_pdf: file_mmd})

    def clear(self):
        self.data = {}




