from nicegui import APIRouter, ui, app

router = APIRouter(prefix='/test')

@router.page('/id/{id}')
def page(id: str):
    response = 

