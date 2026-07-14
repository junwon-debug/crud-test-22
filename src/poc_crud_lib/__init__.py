import json


def create(file_path: str, data: dict) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        records = []

    next_id = max((r["id"] for r in records), default=0) + 1
    record = {"id": next_id, **data}
    records.append(record)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return record
