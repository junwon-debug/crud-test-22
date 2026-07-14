import json

import pytest

from poc_crud_lib import create, read_all, update


def test_update_with_empty_fields_keeps_record_unchanged(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo", "value": 1})

    updated = update(str(file_path), record["id"], {})

    assert updated == record


def test_update_does_not_affect_other_records(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    target = create(str(file_path), {"name": "bar"})
    create(str(file_path), {"name": "baz"})

    update(str(file_path), target["id"], {"name": "updated"})

    records = read_all(str(file_path))
    assert records == [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "updated"},
        {"id": 3, "name": "baz"},
    ]


def test_update_can_add_new_field_not_previously_present(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo"})

    updated = update(str(file_path), record["id"], {"tag": "new"})

    assert updated == {"id": record["id"], "name": "foo", "tag": "new"}


def test_update_on_missing_file_raises_value_error(tmp_path):
    file_path = tmp_path / "data.json"

    with pytest.raises(ValueError):
        update(str(file_path), 1, {"name": "bar"})


def test_update_failure_leaves_original_file_untouched(tmp_path):
    """존재하지 않는 id로 update 실패 시, 원본 파일 내용이 손상되지 않아야 한다."""
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    before = file_path.read_text()

    with pytest.raises(ValueError):
        update(str(file_path), 999, {"name": "bar"})

    assert file_path.read_text() == before
    assert json.loads(before) == [{"id": 1, "name": "foo"}]
