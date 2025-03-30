from flask import Flask, render_template, request, redirect, render_template_string
import os
import asyncio
import json

from src.services import DataService, QuestionService, SettingsService, GradingService
from src.basic.availability import check, to_html

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

dataService = DataService.DataService(ROOT_DIR)
questionService = QuestionService.QuestionService(ROOT_DIR)
gradingService = GradingService.GradingService(ROOT_DIR)

#Kíktu á flask blueprints fyrir modular routes
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        file = request.files['file']
        file_name = file.filename
        if asyncio.run(dataService.process_pdf(file_name)):
            return redirect('/myfiles')
        else:
            redirect('/settings')
    return render_template('uploads.html')

@app.route("/loading")
def loading_screen():
    return render_template('loading.html')

@app.route("/myfiles")
def markdown_page():
    def get_html(file):
        with open("./templates/file_actions.html", "r") as f:
            content = f.read()
            return render_template_string(content, file=file)
    files = check(ROOT_DIR)
    content = [get_html(file) for file in files]
    return render_template('list.html', content=content)

@app.route("/extract/<file>", methods=["GET"]) 
def extract(file=None):
    info = dataService.extract(file)
    return redirect("/myfiles")

@app.route("/generate/<file>", methods=["GET"]) 
def generate(file=None):
    print("works")
    full_name = file+".json"
    fact_file = os.path.join(ROOT_DIR, "./data/facts/", full_name)
    with open(fact_file, "r") as f:
        facts = json.load(f).get("info")
        questionService.clear_questions()
        for fact in facts:
            questionService.generate(fact.get("info"))

    dir_path = os.path.join(ROOT_DIR, "data/tests/", file+"/")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_count = len(os.listdir(dir_path))
    
    quesiont_file_name = file + str(file_count) +".json"
    with open(os.path.join(dir_path,quesiont_file_name),"w") as f:
        questions = questionService.get_json()
        json.dump(questions,f)

    return redirect(f"/test/{file}")
        

@app.route("/test")
def test_list():
    target_path = os.path.join(ROOT_DIR, "data/tests/")
    files = os.listdir(target_path)
    content = [f"<a href='/test/{file}'>{file}</a>" for file in files]
        
    return render_template("list.html", content=content)


@app.route("/test/<target>")
def test_target_dir(target):
    target_path = os.path.join(ROOT_DIR, "data/tests/", target)
    files = os.listdir(target_path)
    content = [f"<a href='/test/{target}/{i}'>Test {i}</a>" for i in range(len(files))]

    return render_template("list.html", content=content)

def handle_test_submit(request, questions):
    form_data = request.form
    print(form_data)
    grades = []
    for i in range(len(questions)):
        key = f"answer_{i+1}"
        if key in form_data:
            grades.append(gradingService.grade(questions[i], form_data[key]))
        else:
            grades.append(gradingService.empty_grade(questions[i]))
    gradings = gradingService.html(questions, grades)
    return render_template("answer.html", answers=gradings)

@app.route("/test/<target>/<test_id>", methods=['GET', 'POST'])
def test_page(target, test_id):
    target_file = os.path.join(ROOT_DIR, "data/tests/",target, f"{target}{test_id}.json")
    with open(target_file, 'r') as file:
        data = json.load(file)
        if request.method == 'POST':
            return handle_test_submit(request, data)
        else:
            questions = questionService.html(data)
            return render_template("question.html", questions=questions)


def handle_settings_submit(request, settings_file):
    form_data = request.form
    app_id = form_data.get("app_id")
    app_key = form_data.get("app_key")
    
    with open(settings_file, 'r') as file:
        settings = json.load(file)
    
    settings['app_id'] = app_id
    settings['app_key'] = app_key
    
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)
    return redirect('/')


@app.route("/settings", methods=['GET', 'POST'])
def settings_page():
    path = os.path.join(ROOT_DIR, "data/settings.json")
    if request.method == 'POST':
        return handle_settings_submit(request, path)
    with open(path, 'r') as file:
        settings = json.load(file)
        return render_template("settings.html", app_key=settings.get("app_key"), app_id = settings.get("app_id"))

    



if __name__ == '__main__':
	app.run()
