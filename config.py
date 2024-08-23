import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "7887faad8f665eb5670dfd5f68292268f878d9907784c5469455f655a6ab8db9"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
