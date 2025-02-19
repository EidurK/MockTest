from pydantic import BaseModel
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
import random

from Question import Question
from Feedback import Feedback

#------------------------------
system_prompt = ""
client = OpenAI()

#------------------------------

def get_question_content_fancy(q):
    question_content = f"{q.question}\n\n"
    for option in q.options:
        question_content += f"- [ ] {option}\n" 
    return question_content

def get_question_content(q):
    question_content = f"{q.question}\n"
    for option in q.options:
        question_content += f"{option}\n" 
    return question_content

def get_feedback_content(f):
    feedback_content = ""
    for feedback in f.feedback:
        feedback_content += f"{feedback}\n" 
    return feedback_content

def combine(question, options):
    return Question(question, options)

def generate_question_answers(fact):
    completion = client.beta.chat.completions.parse(
        model = "gpt-4o-2024-08-06",
        messages=[
            {"role": "system",
             "content": 
             """
            You take in either a fact or a question: 
            in case you recieved a fact:
            1. Generate a question based on the provided fact.  
            2. Create four answer options for the question, ensuring only one is correct.  
            3. Ensure the incorrect options are plausible but incorrect.  
            4. Ensure the output is in correct markdown format

            In case you recieved a question:
            1. Identify the Core Concept: What is the main topic or concept that this question addresses?
            2. Generate a new unique question based on the core concept of the provided question.
            3. Ensure the generated question is NOT IDENTICAL or similar to the provided question.
            4. Ensure the generated question is as difficult as the original question. 
            5. Create four answer options for the question, ensuring only one is correct.  
            6. Ensure the incorrect options are plausible but incorrect.  
            7. Ensure the output is in correct markdown format
             """
             },
            {"role": "assistant", 
             "content":[
                 {"type": "text",
                  "question": 
                  """ 
                  Calculate the result of the following expression 
                  $$3 + 4 \cdot 10 - \frac{4^2}{2}$$ 
                  """, 
                  "options": ["$35$", "$62$", "$39$", "$11$"]
                  },
                 {"type": "text",
                  "question": "Who was the 13. president of the USA" ,
                  "options": ["John Diefenbaker", "Zachary Taylor","Millard Fillmore", "Barack Obama"]
                  },
                 {"type": "text",
                  "question": 
                  """ 
                  Consider the following incomplete binary search function in Python. 
                  Which of the following options do you need to add in line 4 for this binary search function to work correctly?
                  ```python
                  def binary_search(arr, target):
                      lo, hi = 0, len(arr) - 1
                      while lo <= hi:
                          mid = #insert code here
                          if arr[mid] == target:
                              return mid
                          elif arr[mid] < target:
                              lo = mid + 1
                          else:
                              hi = mid - 1
                      return -1
                  ```
                  """,
                  "options": [
                      "`lo + (hi - lo) // 2`",
                      "`lo + (hi - 2) // lo`",
                      "`lo + (lo - hi) / 2`",
                      "`math.mid(lo,hi)`"
                      ]
                  },
                 ]
             },
            {"role": "user", "content": fact},
        ],
        response_format=Question,
    )
    return completion.choices[0].message.parsed

def generate_question(fact):
    completion = client.beta.chat.completions.parse(
        model = "gpt-4o-2024-08-06",
        messages=[
            {"role": "system",
             "content": 
             """ 
             You generate questions from some data.
             You take in either a fact or a question: 
             in case you recieved a fact: 
             - Identify the Core Concept: What is the main topic or concept that this fact addresses? 
             - Generate a question based on the provided topic.  

             In case you recieved a question:
             - Identify the Core Concept: What is the main topic or concept that this question addresses?
             - Generate a new unique question based on the core concept of the provided question.
             - Ensure the generated question is NOT IDENTICAL or similar to the provided question.

             Make sure the question generated is
             - dificult
             - unambiguous
             - detailed
             - easily understandable
             """
             },
            {"role": "assistant", 
             "content":[
                 {"type": "text",
                  "question": 
                  """ 
                  Calculate the result of the following expression 
                  $$3 + 4 \cdot 10 - \frac{4^2}{2}$$ 
                  """, 
                  },
                 {"type": "text",
                  "question": "Who was the 13. president of the USA" ,
                  },
                 {"type": "text",
                  "question": 
                  """ 
                  Consider the following incomplete binary search function in Python. 
                  Which of the following options do you need to add in line 4 for this binary search function to work correctly?
                  ```python
                  def binary_search(arr, target):
                      lo, hi = 0, len(arr) - 1
                      while lo <= hi:
                          mid = #insert code here
                          if arr[mid] == target:
                              return mid
                          elif arr[mid] < target:
                              lo = mid + 1
                          else:
                              hi = mid - 1
                      return -1
                  ```
                  """,
                  },
                 ]
             },
            {"role": "user", "content": fact},
        ],
    )
    return completion.choices[0].message.parsed


def review_question(q):
    question_content = get_question_content(q)

    completion = client.beta.chat.completions.parse(
            model = "gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": 
                 """ 
                 You have been provided with a multiple choice question. 
                 You give feedback on the quality of the question.
                 In order to give good feedback you should:
                 - Do not compliment anything.
                 - Keep your feedback concise and detailed.
                 - Only point out what should be done better.
                 - Make sure the question is either unambiguous or only 1 option is correct.
                 - Make sure each option is similarly long. 
                 - Make sure the question is detailed, concise and easily understandable. 
                 - Make sure the options do not include any list markers or enumerators.
                 - Make sure the question is difficult. 
                 - Ensure the options are specific and detailed.

                 Please respond with 'No feedback' if the question can't be improved.
                 """ 
                 }, 
                {"role": "user",
                 "content": question_content
                 },
                ],
            response_format=Feedback,
            )
    return completion.choices[0].message.parsed

def modify_question(q, f):
    question_content = get_question_content(q)
    feedback_content = get_feedback_content(f)
    completion = client.beta.chat.completions.parse(
            model = "gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": 
                 """
                You have been provided with a multiple choice question in markdown format and feedback on how to improve the question. 
                For each feedback try to improve the question.
                To improve the question you should
                - Identify the Core Concept: What is the main topic or concept that this question addresses?
                - Identify the main issues of the question pointed out by the feedback.
                - Create a new Unique question that follows the same topic and fixes the issues.
                 """
                 },
                {"role": "assistant", 
                 "content":[
                     {"type": "text",
                      "question": 
                      """ 
                          Calculate the result of the following expression 
                          $$3 + 4 \cdot 10 - \frac{4^2}{2}$$ 
                          """, 
                      "options": ["$35$", "$62$", "$39$", "$11$"]
                      },
                     {"type": "text",
                      "question": "Who was the 13. president of the USA" ,
                      "options": ["John Diefenbaker", "Zachary Taylor","Millard Fillmore", "Barack Obama"]
                      },
                     {"type": "text",
                      "question": 
                      """ 
                          Consider the following incomplete binary search function in Python. 
                          Which of the following options do you need to add in line 4 for this binary search function to work correctly?
                          ```python
                          def binary_search(arr, target):
                              lo, hi = 0, len(arr) - 1
                              while lo <= hi:
                                  mid = #insert code here
                                  if arr[mid] == target:
                                      return mid
                                  elif arr[mid] < target:
                                      lo = mid + 1
                                  else:
                                      hi = mid - 1
                              return -1
                          ```
                          """,
                      "options": [
                          "`lo + (hi - lo) // 2`",
                          "`lo + (hi - 2) // lo`",
                          "`lo + (lo - hi) / 2`",
                          "`math.mid(lo,hi)`"
                          ]
                      },
                     ]
                 },
                {"role": "user",
                 "content": question_content },
                {"role": "user", 
                 "content": feedback_content 
                 },
                ],
            response_format=Question,
            )
    return completion.choices[0].message.parsed

def pick_question(q1, q2):

    question_content1 = get_question_content(q1)
    question_content2 = get_question_content(q2)
    completion = client.beta.chat.completions.parse(
            model = "gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": 
                 """
                 You are a model that picks the better question out of two options.

                 """
                 },
                {"role": "user",
                 "content": [
                     {"type":"text", "text": question_content1},
                     {"type":"text", "text": question_content2},
                     ]
                 },
                ],
            response_format=Question,
            )
    return completion.choices[0].message.parsed






def markdownify(q):
    question_content = get_question_content(q)
    completion = client.beta.chat.completions.parse(
            model = "gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": 
                 """
                 You have been provided with a multiple choice question and 4 options for that question, your job is to put the question into markdown format.
                 To do this you must:
                 - Ensure short math expressions are wrapped in inline mathblock, e.g. $<short math expression>$
                 - Ensure that long math expression are wrapped in mathblock, e.g. $$<long math expression>$$. This is only applicable for the question and not the options.
                 - Ensure code in the question is wrapped in code block.
                 - For each code block in the question, identify insert the correct programming language
                 - Ensure short code snippets in the options are wrapped in inline codeblock e.g. `<short code>`. You will not need to specify the programming language for these blocks.
                 - Ensure mathblocks are declared using dollar-signs
                 - Ensure that there is not a whitespace between the dollar-signs and the math expression in a mathblock. e.g. $<expression>$ and not $ <expression> $.

                 You should not modify the content of the question or the options, only change the format displayed.
                 """
                 },
                {"role": "user",
                 "content": question_content},
                {"role": "assistant", 
                 "content":[
                     {"type": "text",
                      "question": 
                      """ 
                      Calculate the result of the following expression 
                      $$3 + 4 \cdot 10 - \frac{4^2}{2}$$ 
                      """, 
                      "options": ["$35$", "$62$", "$39$", "$11$"]
                      },
                     {"type": "text",
                      "question": "Who was the 13. president of the USA" ,
                      "options": ["John Diefenbaker", "Zachary Taylor","Millard Fillmore", "Barack Obama"]
                      },
                     {"type": "text",
                      "question": 
                      """ 
                      Consider the following incomplete binary search function in Python. 
                      Which of the following options do you need to add in line 4 for this binary search function to work correctly?
                      ```python
                      def binary_search(arr, target):
                          lo, hi = 0, len(arr) - 1
                          while lo <= hi:
                              mid = #insert code here
                              if arr[mid] == target:
                                  return mid
                              elif arr[mid] < target:
                                  lo = mid + 1
                              else:
                                  hi = mid - 1
                          return -1
                      ```
                      """,
                      "options": [
                          "`lo + (hi - lo) // 2`",
                          "`lo + (hi - 2) // lo`",
                          "`lo + (lo - hi) / 2`",
                          "`math.mid(lo,hi)`"
                          ]
                      },
                     ]
                 },
                ],
            response_format=Question,
            )
    return completion.choices[0].message.parsed







