from pydantic import BaseModel
from openai import OpenAI
import os
from flask import render_template_string
from typing import List
import json

class Grading(BaseModel):
    feedback: str
    selected_option: int
    correct_option: int

class GradingService:
    system_prompt = """
    You are an helpful teacher.
    You will be provided with a question, 4 different options, and wich option the student has answered.

    1. Give the user feedback on how to solve the question step by step.
    2. Find the correct answer. 
    3. Extract what option the user selected.

    """
    user_prompt = """
    I have provided you with a question and my answer, is my answer correct?
    """

    def __init__(self, ROOT_DIR, settings_path="data/settings.json"):
        self.ROOT_DIR = ROOT_DIR 
        self.SETTINGS_PATH = os.path.join(self.ROOT_DIR, settings_path)

        self.client = OpenAI()

    def grade(self, question, answer):
        q = question.get("question")

        full_up = self.user_prompt
        full_up += f"\n"
        full_up += f"{q}\n"
        for o in question.get("options"):
            full_up += f"{o}\n"
        full_up += f"My answer was:\n"
        full_up += f"{answer}"


        completion = self.client.beta.chat.completions.parse(
            model = "o3-mini",
            reasoning_effort="low",
            messages=[
                { "role": "system", "content": self.system_prompt },
                { "role": "user", "content": full_up}
            ],
            response_format=Grading
        )

        extraction = completion.choices[0].message
        if (extraction.refusal):
            print("Extraction refuesd")
            return None
        else:
            return extraction.parsed

    def empty_grade(self, question):
        return Grading(feedback="No answer", selected_option="-1", correct_option="-1")

    def get_json(self, question):
        question_dict = {
            "answer": question.answer,
            "feedback": question.feedback
        }
        return question_dict

    def html(self, questions, grading):
        output = ""
        for i in range(len(questions)):
            output += self._html_helper(questions[i], grading[i], i+1)
        return output

    def _html_helper(self, question, answer, number):
        with open(os.path.join(self.ROOT_DIR, "templates/answer_block.html"), "r") as f:
            template_string = f.read()
            return render_template_string(template_string, 
                                          number = number, 
                                          question=question.get('question'), 
                                          options= question.get('options'), 
                                          correct=answer.correct_option, 
                                          selected=answer.selected_option, 
                                          feedback=answer.feedback)

