from pydantic import BaseModel
from openai import OpenAI
import os
from flask import render_template_string
from typing import List
import json

class Question(BaseModel):
    question: str
    options: list[str]




class QuestionService:
    system_prompt = """
    You are an AI designed to create educational content.
    Your task is to generate a multiple-choice question from the provided text.
    The text may include facts, definitions, rules, code blocks, examples, or questions. 

    Provide four answer choices, ensuring one is correct and the others are plausible distractors. 

    Ensure the question and options are relevant and informative.

    If you have been provided with a question make sure that your output question is not identical to the original question.
    Ensure your output is in markdown format.
    """
    user_prompt = """
    Create a Test question from the following text, do not only test my understanding of the concepts but also their application:
    """

    def __init__(self, ROOT_DIR, settings_path="data/settings.json"):
        self.ROOT_DIR = ROOT_DIR 
        self.SETTINGS_PATH = os.path.join(self.ROOT_DIR, settings_path)

        self.client = OpenAI()
        self.questions = []

    def generate(self, fact):
        completion = self.client.beta.chat.completions.parse(
            model = "o3-mini",
            reasoning_effort="medium",
            messages=[
                { "role": "system", "content": self.system_prompt },
                { "role": "user", "content": self.user_prompt + fact}
            ],
            response_format=Question
        )

        extraction = completion.choices[0].message
        if (extraction.refusal):
            print("Extraction refuesd")
            return None
        else:
            self.questions.append(extraction.parsed) 
            return 

    def get_questions(self):
        return self.questions
    def clear_questions(self):
        self.questions = []

    def get_json(self):
        questions_json = []
        for question in self.questions:
            question_dict = {
                "question": question.question,
                "options": question.options
            }
            questions_json.append(question_dict)
        return questions_json


    def markdown(self):
        output = f"***\n"
        for q in self.questions:
            output += f"{q.question}\n\n"
            for o in q.options:
                output += f"- [ ] {o}\n"
            output += f"***\n"
        return output

    def html(self, q):
        output = ""
        for i in range(len(q)):
            output += self._html_helper(q[i], i+1)
        return output

    def _html_helper(self, question, number):
        with open(os.path.join(self.ROOT_DIR, "templates/question_block.html"), "r") as f:
            template_string = f.read()
            return render_template_string(template_string,
                                   number = number,
                                   question=question.get('question'),
                                   options= question.get('options'))


