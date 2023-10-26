from app.db.session import engine
from app.models.cominfo_model import ComInfo


def create_table():
    ComInfo.metadata.create_all(bind=engine)
