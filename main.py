from nicegui import ui

ui.label("RPG Session Planner").classes("text-h4 text-weight-bold")
ui.badge("Version 0.1", color="green")

ui.run(port=8080, title="RPG Session Planner")