from openai import OpenAI
from pydantic import BaseModel
import json
import os

# Facts, Examples, etc

class Information(BaseModel):
    reasoning: str
    info: str

class Highlights(BaseModel):
    info: list[Information]

class Extractor:

    system_prompt = """
    You are a helpful AI that helps students extract key reading material to prepare for incomming test.
    Help the user find key reading material by extracting important information and reason why it is likely to come on the test
    """
    user_prompt = """
    Instructions:
        - Given the Lecture notes below, extract ALL important information that might come on the test.
        - Return the information in a clear and concise way.
        - Include markdown formatting where applicaple.
    """

    def __init__(self, target, ROOT_DIR, model="o3-mini"):

        self.ROOT_DIR = ROOT_DIR
        target +=".mmd"
        input_file = os.path.join(self.ROOT_DIR, "data/markdown/", target)

        self.client = OpenAI()
        self.model = model
        with open(input_file, "r") as file:
            file_content = file.read()
            self.user_prompt = self.user_prompt + file_content

    def extract(self):
        completion = self.client.beta.chat.completions.parse(
            model = self.model,
            reasoning_effort="low",
            messages=[
                { "role": "system", "content": self.system_prompt },
                { "role": "user", "content": self.user_prompt }
            ],
            response_format=Highlights
        )

        extraction = completion.choices[0].message
        if (extraction.refusal):
            print("Extraction refuesd")
            return None
        else:
            self.highlights = extraction.parsed
            return self.highlights

    def write(self, output_file):
        info = self.highlights

        if self.highlights:
            f = open(output_file, "w")
            f.write(info.model_dump_json())
            return output_file
        else:
            print("Extract first!!")
            return None
