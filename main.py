from nicegui import ui
from datetime import date
from models import Adventure, Base, Campaign, Session, Scene, engine, SessionLocal

Base.metadata.create_all(engine)

@ui.page('/')
def main_page():
    ui.label("Campaign Planner").classes("text-3xl font-bold mb-4")

    campaign_list_container = ui.column().classes("w-full gap-2")

    def refresh_campaign_list():
        campaign_list_container.clear()
        db = SessionLocal()
        campaigns = db.query(Campaign).all()
        db.close()

        with campaign_list_container:
            if not campaigns:
                ui.label("No campaigns found. Create a new campaign to get started.").classes(
                    "text-gray-500 italic"
                )
                return

            for campaign in campaigns:
                with ui.card().classes('w-full p-4 flex-row items-center justify-between'):
                    with ui.column():
                        ui.label(campaign.name).classes('text-lg font-semibold')
                        ui.label(f'Started: {campaign.start_date}').classes(
                            'text-sm text-gray-600'
                        )

                    ui.button(
                        "View Adventures",
                        on_click=lambda c=campaign.id: ui.notify(
                            f"Clicked campaign ID: {c}"
                        ),
                    ).props('flat dense')

    # Add a new campaign
    with ui.card().classes('w-full p-4 mt-4'):
        ui.label("Create New Campaign").classes('text-xl font-semibold mb-2')
        with ui.row().classes('w-full items-center gap-4'):
            name_input = ui.input("Campaign Name").classes('flex-grow')

            def handle_add_campaign():
                if not name_input.value:
                    ui.notify("Campaign name cannot be empty.", color="negative")
                    return

                db = SessionLocal()
                new_campaign = Campaign(name=name_input.value)
                db.add(new_campaign)
                campaign_name = new_campaign.name  # Store the campaign name before committing
                db.commit()
                db.close()

                name_input.value = ""
                refresh_campaign_list()
                ui.notify(f"Campaign '{campaign_name}' created successfully.", color="positive")

            ui.button("Add Campaign", on_click=handle_add_campaign).props('color=primary')

        refresh_campaign_list()

# Run the app in a browser
# ui.run(port=8080, title="Campaign Planner", reload=True)

# Run the app in a standalone window
ui.run(native=True, title='Campaign Planner', reload=False)