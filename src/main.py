from DataController import DataController
from QuestionController import QuestionController 
import json

#------------------------------
pdf_file = 'pyc9.pdf'
settings_path = '../settings.json'
data_path = '../data/'
#------------------------------

dataController = DataController(data_path, settings_path)
questionController = QuestionController ()
mmd_file = dataController.process_pdf(pdf_file)
fact_file = dataController.extract()
with open(fact_file, 'r') as file:
    data = json.load(file)
    output_string =""
    for fact in data.get("info"):
        questionController.generate(fact.get("info"))
    output_string = questionController.markdown()

    with open("output.md", "w") as f:
        f.write(output_string)




