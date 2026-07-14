import json


def _load(file_path: str) -> list[dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def create(file_path: str, data: dict) -> dict:
    records = _load(file_path)

    next_id = max((r["id"] for r in records), default=0) + 1
    record = {"id": next_id, **data}
    records.append(record)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return record


def read_all(file_path: str) -> list[dict]:
    return _load(file_path)


def read_by_id(file_path: str, id: int) -> dict | None:
    for record in _load(file_path):
        if record["id"] == id:
            return record
    return None
