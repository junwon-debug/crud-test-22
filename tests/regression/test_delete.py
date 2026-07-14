import pytest

from poc_crud_lib import create, delete, read_all, read_by_id


def test_delete_removes_record(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo"})
    create(str(file_path), {"name": "bar"})

    delete(str(file_path), record["id"])

    assert read_by_id(str(file_path), record["id"]) is None
    assert read_all(str(file_path)) == [{"id": 2, "name": "bar"}]


def test_delete_raises_value_error_when_id_not_found(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})

    with pytest.raises(ValueError):
        delete(str(file_path), 999)
