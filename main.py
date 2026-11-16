from contextlib import contextmanager
from datetime import date
from models import Adventure, Base, Campaign, Session, Scene, engine, SessionLocal
from nicegui import ui
from sqlalchemy.exc import SQLAlchemyError
import logging

Base.metadata.create_all(engine)

logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@ui.page('/')
def main_page():
    ui.label("Campaign Planner").classes("text-3xl font-bold mb-4")

    content_area = ui.column().classes("w-full gap-2")

    def render_campaign_list():
        content_area.clear()

        with get_db() as db:
            campaigns = db.query(Campaign).all()
            campaign_data = [
                (campaign.id, campaign.name, campaign.start_date)
                for campaign in campaigns
            ]

        with content_area:
            if not campaign_data:
                ui.label("No campaigns found. Create a new campaign to get started.").classes(
                    "text-gray-500 italic"
                )
                return

            for campaign_id, campaign_name, campaign_start_date in campaign_data:
                with ui.card().classes('w-full p-4 flex-row items-center justify-between'):
                    with ui.column():
                        ui.label(campaign_name).classes('text-lg font-semibold')
                        ui.label(f'Started: {campaign_start_date}').classes(
                            'text-sm text-gray-600'
                        )

                    ui.button(
                        "View Adventures",
                        on_click=lambda c=campaign_id: render_adventure_list(c),
                    ).props("flat dense")

    def render_adventure_list(campaign_id):
        content_area.clear()
        with get_db() as db:
            campaign = db.get(Campaign, campaign_id)

            if campaign is None:
                ui.notify("Campaign not found.", color="negative")
                render_campaign_list()
                return

            campaign_name = campaign.name
            adventures = db.query(Adventure).filter(
                Adventure.campaign_id == campaign_id
            ).all()
            adventure_data = [
                (adv.id, adv.name, adv.adventure_summary)
                for adv in adventures
            ]

        with content_area:
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label(f"Adventures in '{campaign_name}'").classes('text-xl font-semibold')
                ui.button("Back to Campaigns", on_click=render_campaign_list).classes('text-xl font-bold')

            adventure_list_container = ui.column().classes("w-full gap-2")

            with adventure_list_container:
                if not adventure_data:
                    ui.label(
                        'No adventures found for this campaign. Create a new one to get started.'
                        ).classes('text-gray-500 italic')
                else:
                    for adventure_id, adventure_name, adventure_summary in adventure_data:
                        with ui.card().classes('w-full p-4 flex-row items-center justify-between'):
                            with ui.column():
                                ui.label(adventure_name).classes('text-lg font-semibold')
                                ui.label(f"Summary: {adventure_summary or ''}").classes('text-sm text-gray-600'
                                )

                            ui.button('View Sessions', on_click=lambda a=adventure_id: ui.notify(
                                    f"Clicked adventure ID: {a}"
                                ),
                            ).props('flat dense')

            with ui.card().classes('w-full p-4 mt-4'):
                ui.label('Create new adventure').classes('text-xl font-semibold mb-2')
                with ui.row().classes('w-full items-center gap-4'):
                    adv_name_input = ui.input('Adventure Name').classes('flex-grow')

                    def handle_add_adventure():
                        name = adv_name_input.value.strip()
                        if not name:
                            ui.notify('Adventure name cannot be empty.', color='negative')
                            return

                        try:
                            with get_db() as adv_db:
                                new_adv = Adventure(name=name, campaign_id=campaign_id)
                                adv_db.add(new_adv)
                                adv_db.commit()
                        except SQLAlchemyError:
                            logger.exception("Error while creating new adventure.")
                            ui.notify('Could not create new adventure.', color='negative')
                            return

                        adv_name_input.value = ""
                        render_adventure_list(campaign_id)
                        ui.notify(f"Adventure '{name}' created successfully.", color='positive')

                    ui.button('Add Adventure', on_click=handle_add_adventure).props('color=primary')
    # Add a new campaign
    with ui.card().classes('w-full p-4 mt-4'):
        ui.label("Create New Campaign").classes('text-xl font-semibold mb-2')
        with ui.row().classes('w-full items-center gap-4'):
            name_input = ui.input("Campaign Name").classes('flex-grow')

            def handle_add_campaign():
                name = (name_input.value or "").strip()
                if not name:
                    ui.notify("Campaign name cannot be empty.", color="negative")
                    return

                try:
                    with get_db() as campaign_db:
                        new_campaign = Campaign(name=name)
                        campaign_name = new_campaign.name
                        campaign_db.add(new_campaign)
                        campaign_db.commit()
                except SQLAlchemyError:
                    logger.exception("Error while creating new campaign.")
                    ui.notify('Could not create new campaign.', color='negative')
                    return

                name_input.value = ""
                render_campaign_list()
                ui.notify(f"Campaign '{campaign_name}' created successfully.", color="positive")

            ui.button("Add Campaign", on_click=handle_add_campaign).props('color=primary')

        render_campaign_list()

# Run the app in a browser
# ui.run(port=8080, title="Campaign Planner", reload=True)

# Run the app in a standalone window
ui.run(native=True, title='Campaign Planner', reload=False)