from webapp import create_app
from webapp.content_parser import get_content_entries

app = create_app()
counter = 1
with app.app_context():
    get_content_entries(counter)