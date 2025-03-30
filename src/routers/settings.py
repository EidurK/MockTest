from nicegui import APIRouter, ui, app

router = APIRouter(prefix='/settings')

@router.page('/')
def page():
    ui.markdown("# Settings")
    app_id_field = ui.input(label='app_id', value = '')
    app_key_field = ui.input(label='app_key', value = '')
    ui.button('see values', on_click=lambda: ui.notify(f"{app_id_field.value}", type='info'))




