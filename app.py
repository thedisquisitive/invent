from app import app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Manufacturer, Category, Location, Financing, Stock

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Manufacturer': Manufacturer, 'Category': Category, 'Location': Location, 'Financing': Financing, 'Stock': Stock}
