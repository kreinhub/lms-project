from webapp import create_app
from webapp.articles import get_habr, get_tproger

app = create_app()
with app.app_context():
    get_habr()
    get_tproger()