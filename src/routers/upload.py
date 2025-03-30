from nicegui import APIRouter, ui, app
from fastapi import Request 
from ..components.local_file_picker import local_file_picker
import asyncio
import requests
import os
import tkinter as tk
from tkinter import filedialog
import json

router = APIRouter(prefix='/upload')


def handle_file_lookup():
    root = tk.Tk()
    root.withdraw()
    temp = filedialog.askopenfilename()

    if temp.endswith('.pdf'):
        app.storage.general['file'] = temp


async def submit():
    print("submit called")
    file = app.storage.general['file']
    print("File:",file)
    ui.navigate.to("/data/generate")

@router.page('/')
def page():
    storage = app.storage.general
    storage['file'] = ''

    with ui.stepper().props('vertical') as stepper:
        with ui.step('Set reading material'):
            ui.button('Choose file', on_click=handle_file_lookup, icon='folder')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                
        with ui.step('Generate'):
            with ui.stepper_navigation():
                ui.button('Test', on_click=lambda: print("Test:", storage['file']))
                ui.button('Generate test', on_click=submit)
                ui.button('Back', on_click=stepper.previous).props('flat')

    

