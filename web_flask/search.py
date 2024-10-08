from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    data = {}
    for field in model.__searchable__:
        data[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, document=data)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page, fields=None):
    if not current_app.elasticsearch:
        return [], 0
    if fields:
        search = current_app.elasticsearch.search(
            index=index,
            query={"bool": {"must": [{"term": {"email.keyword": query}}]}},
            from_=(page - 1) * per_page,
            size=per_page,
        )
    else:
        fields = ["*"]
        search = current_app.elasticsearch.search(
            index=index,
            query={"multi_match": {"query": query, "fields": fields}},
            from_=(page - 1) * per_page,
            size=per_page,
        )
    ids = [hit["_id"] for hit in search["hits"]["hits"]]
    return ids
