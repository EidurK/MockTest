from ..objects import  MathOCR, Extractor
from tqdm import tqdm
import time 
import os


class DataService:
    def __init__(self, ROOT_DIR, settings_path="data/settings.json"):
        self.ROOT_DIR = ROOT_DIR 
        self.SETTINGS_PATH = os.path.join(self.ROOT_DIR, settings_path)
        self.MARKDOWN_PATH = os.path.join(self.ROOT_DIR, "data/markdown/")


        self.settings_path = settings_path

    async def process_pdf(self, pdf_file):
        self.precent_done = 0
        mmd_file = self._get_mmd(pdf_file)

        if mmd_file:
            self.target = mmd_file
            self.precent_done = 100
            return {"file": mmd_file}

        ocr = MathOCR.MathOCR(pdf_file, self.ROOT_DIR)
        response = ocr.process()
        if not self._ocrStatus(ocr):
            return None
        mmd_file = ocr.download() 
        self.target = mmd_file
        return {"file": mmd_file}


    def _get_mmd(self, pdf_file):
        base_name = os.path.splitext(os.path.basename(pdf_file))[0] + ".mmd"
        mmd_file = os.path.join(self.ROOT_DIR, "data/markdown/", base_name)
        print("_get_mmd ->", mmd_file)
        return mmd_file if os.path.isfile(mmd_file) else None

    def _ocrStatus(self, ocr):
        os.system('clear')
        # progress_bar = tqdm(total=100, desc="Uploading", unit="%", ncols=100)
        while True:
            info = ocr.status()
            self.precent_done = info.get('percent_done', 0)/100
            print(info)
            self.status = info.get('status', '')

            # progress_bar.clear()
            # progress_bar.update(n=self.precent_done)

            if self.status == 'completed':
                return True
            elif self.status == 'error':
                print("An error occurred during upload.")
                return False

    def extract(self, target=None):
        if target:
            self.target = target

        if self.target:
            base_name = os.path.splitext(os.path.basename(self.target))[0] + ".json"
            print("base_name:", base_name)
            info_file = os.path.join(self.ROOT_DIR, "data/facts/", base_name)
            ext = Extractor.Extractor(self.target, self.ROOT_DIR)
            ext.extract()
            ext.write(info_file)
            return info_file
        return None


