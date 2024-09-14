from web_flask.search import add_to_index, remove_from_index, query_index
from web_flask import db
import sqlalchemy as sa


class SearchableMixin:
    @classmethod
    def search(cls, expression, page, per_page, fields=None):
        if cls.__abstract__:  # Check if the class is abstract
            results = []
            for subclass in cls.__subclasses__():
                ids = query_index(
                    subclass.__tablename__, expression, page, per_page, fields
                )
                if len(ids) > 0:
                    when = []
                    for i in range(len(ids)):
                        when.append((ids[i], i))
                    query = (
                        sa.select(subclass)
                        .where(subclass.id.in_(ids))
                        .order_by(db.case(*when, value=subclass.id))
                    )
                    results.extend(db.session.scalars(query))
            return results

        ids = query_index(cls.__tablename__, expression, page, per_page, fields)
        if len(ids) == 0:
            return []
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        query = (
            sa.select(cls).where(cls.id.in_(ids)).order_by(db.case(*when, value=cls.id))
        )
        return db.session.scalars(query)

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        if cls.__abstract__ == True:
            for subclass in cls.__subclasses__():
                for obj in db.session.scalars(sa.select(subclass)):
                    add_to_index(subclass.__tablename__, obj)
        else:
            for obj in db.session.scalars(sa.select(cls)):
                add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
