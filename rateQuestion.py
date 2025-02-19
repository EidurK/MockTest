from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_api(input_string, system):
    completion = client.chat.completions.create(
            model="4o",
            messages=[
                {
                    "role": "system",
                    "content": system
                    },
                {
                    "role": "user",
                    "content": input_string
                    }
                ],
            max_tokens=1000
            )
    return completion.choices[0].message.content.strip()

def get_input_string(question):
    question = question['question']

    description = question['description']
    options = question['options']
    a = options['a']
    b = options['b']
    c = options['c']
    d = options['d']
    answer = question['answer']
    return f"""
{description}
    a {a}
    b {b}
    c {c}
    d {d}
the answer is {answer}
"""

def rate_question(question_array, system):
    question_array = question_array['questions']
    # question_array = question_array[:5]
    response = []
    for question in question_array:
        res = query_api(get_input_string(question), system)
        response.append(res)
    return response



system = ""
with open('./tests/prompt.txt', 'r') as file:
    system = file.read()

with open('./tests/test.json', 'r') as file:
    questions = file.read()
    question_array = json.loads(questions)
    response = rate_question(question_array, system)
    for res in response:
        print(res)


