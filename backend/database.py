"""Minimal database access layer for the voice AI agent."""

class Database:
    def __init__(self, url="sqlite:///:memory:"):
        self.url = url
        self.connected = False
        self.storage = {}

    def connect(self):
        self.connected = True
        return self

    def query(self, query_text, *params, **kwargs):
        return []

    def insert(self, table, data):
        self.storage.setdefault(table, []).append(data)
        return data

    def update(self, table, record_id, data):
        items = self.storage.get(table, [])
        for index, item in enumerate(items):
            if item.get("id") == record_id:
                items[index] = {**item, **data}
                return items[index]
        return None

    def delete(self, table, record_id):
        items = self.storage.get(table, [])
        for index, item in enumerate(items):
            if item.get("id") == record_id:
                return items.pop(index)
        return None
