import pytest

from poc_crud_lib import create, read_by_id, update


def test_update_patches_existing_record(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo", "value": 1})

    updated = update(str(file_path), record["id"], {"value": 2})

    assert updated == {"id": record["id"], "name": "foo", "value": 2}


def test_update_persists_change_to_file(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo"})

    update(str(file_path), record["id"], {"name": "bar"})

    assert read_by_id(str(file_path), record["id"]) == {"id": record["id"], "name": "bar"}


def test_update_raises_value_error_when_id_not_found(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})

    with pytest.raises(ValueError):
        update(str(file_path), 999, {"name": "bar"})
