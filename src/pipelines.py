from pydantic import BaseModel
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
import random

# Import the necessary components from the original file
from generate_question import generate_question_answers, generate_question, review_question, modify_question,get_question_content_fancy, get_question_content, get_feedback_content, markdownify, pick_question
from reader import read_facts
from Feedback import Feedback

# Initialize console for output
console = Console()

# Select a random fact from the list
F = read_facts('../data/Facts.json')

random_fact = random.choice(F)

def get_pipeline_string(fact, pipeline):
    return  get_question_content_fancy(pipeline(fact))

# Generate a question using the selected fact
def pipeline_basic(fact):
    question = generate_question_answers(fact)
    feedback = review_question(question)
    modified_question = modify_question(question, feedback)
    final_question = markdownify(modified_question)
    return final_question

def pipeline_difficult(fact):
    question = generate_question_answers(fact)
    feedback = review_question(question)
    feedback.add_feedback("Make the question harder.")
    feedback.add_feedback("The question is not detailed enough.")
    modified_question = modify_question(question, feedback)
    final_question = markdownify(modified_question)
    return final_question

def pipeline_difficult_2(fact):
    question = generate_question_answers(fact)
    feedback = review_question(question)
    feedback.add_feedback("Make the question harder.")
    feedback.add_feedback("The question is not detailed enough.")
    question = modify_question(question, feedback)
    feedback = review_question(question)
    feedback.add_feedback("Make the question harder.")
    feedback.add_feedback("The question is not detailed enough.")
    question = modify_question(question, feedback)
    final_question = markdownify(question)
    return final_question

def pipeline_longer(fact):
    question = generate_question_answers(fact)
    feedback = review_question(question)
    feedback.add_feedback("Make the question longer.")
    feedback.add_feedback("The question is not detailed enough.")
    question = modify_question(question, feedback)
    final_question = markdownify(question)
    return final_question

def pipeline_generate_x3(fact):
    question = generate_question_answers(fact)
    question = generate_question_answers(get_question_content(question))
    question = generate_question_answers(get_question_content(question))

    feedback = review_question(question)
    feedback.add_feedback("Make the question harder.")
    feedback.add_feedback("The question is not detailed enough.")
    question = modify_question(question, feedback)

    final_question = markdownify(question)
    return final_question

def pipeline_two_questions(fact):
    question1 = generate_question_answers(fact)
    question2 = generate_question_answers(fact)
    question = pick_question(question1, question2)
    feedback = review_question(question)
    feedback.add_feedback("Make the question harder.")
    feedback.add_feedback("The question is not detailed enough.")
    question = modify_question(question, feedback)
    final_question = markdownify(question)
    return final_question




def pipeline_question_only(fact):
    question = generate_question_answers(fact)
    for i in range(2):
        feedback = review_question(question)
        feedback.add_feedback("The question is not detailed enough.")
        question = modify_question(question, feedback)
        question = generate_question_answers(question.question)
    final_question = markdownify(question)
    return final_question


def write_to_file(string1, string2, filepath):
    with open(filepath, 'w') as file:
        file.write('# Fact\n' + string1 + '\n')

    with open(filepath, 'a') as file:
        file.write('# Question\n'+string2)

files = ['../Obsidian vault/Model1.md', '../Obsidian vault/Model2.md']
pipelines = [  pipeline_difficult, pipeline_two_questions]
random.shuffle(pipelines)

print(pipelines[0].__name__, " -> ", files[0])
write_to_file(random_fact, get_pipeline_string(random_fact, pipelines[0]), files[0])
print(pipelines[1].__name__, " -> ", files[1])
write_to_file(random_fact, get_pipeline_string(random_fact, pipelines[1]), files[1])


