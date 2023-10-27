from app.db.session import engine
from app.models.cominfo_model import ComInfo


def create_table():
    """
        SqlAlchemy
    :return: None
    """
    print("create_tbale")
    ComInfo.metadata.create_all(bind=engine)
