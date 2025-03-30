import json
import os 
from flask import render_template_string

def check(ROOT_DIR):
    files = os.listdir(os.path.join(ROOT_DIR, "data/markdown"))
    file_info = []
    for file in files:
        name, _ = os.path.splitext(file)
        full_name = name + ".json"
        extracted = os.path.exists(os.path.join(ROOT_DIR, "data/facts", full_name))
        tests = []
        if extracted:
            tests = os.listdir(os.path.join(ROOT_DIR, "data/facts/", name, "/"))

        file_info.append({
            "name": name,
            "extracted": extracted,
            "tests": tests
        })
    return file_info



def to_html(file):
    file = json.loads(json.dumps(file))
    name = file.get('name')
    extracted = file.get('extracted')
    tests = file.get('tests')
    template_string = """
<div class="list-item">
    <p>{{ name }}</p>
    <form action="/extract/{{ name }}" method="post" style="margin: 0;">
        <button type="submit" class="generate-button">Extract</button>
    </form>
    {% if extracted %}
    <form action="/generate/{{ name }}" method="post" style="margin: 0;">
        <button type="submit" class="generate-button">Generate</button>
    </form>
    {% endif %}
    {% if tests != [] %}
    <form action="/test/{{ name }}" method="get" style="margin: 0;">
        <button type="submit" class="generate-button">Tests</button>
    </form>
    {% endif %}
</div>
    """
    return render_template_string(template_string,
                           name=file.get('name'),
                           extracted= file.get('extracted'),
                           tests= file.get('files')
   )



