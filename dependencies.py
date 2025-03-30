from nicegui import APIRouter, app, ui
import os
from src.components.local_file_picker import local_file_picker

router = APIRouter(prefix="/helper")

@router.get("/")
async def pick_file() -> None:
    result = await local_file_picker('~', multiple=True)
    ui.notify(f'You chose {result}')
    return result
