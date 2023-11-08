from app.db.session import engine

from app.models.cominfo_model import ComInfo, ComInfoRT
from app.models.commanage_model import ComManage
from app.models.user_model import User


def create_table():
    ComInfo.metadata.create_all(bind=engine)
    ComInfoRT.metadata.create_all(bind=engine)
    ComManage.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("DB Init")

    create_table()
