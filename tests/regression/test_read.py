from poc_crud_lib import create, read_all, read_by_id


def test_read_all_returns_empty_list_when_file_missing(tmp_path):
    file_path = tmp_path / "data.json"

    assert read_all(str(file_path)) == []


def test_read_all_returns_all_records(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    create(str(file_path), {"name": "bar"})

    assert read_all(str(file_path)) == [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]


def test_read_by_id_returns_matching_record(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    record = create(str(file_path), {"name": "bar"})

    assert read_by_id(str(file_path), record["id"]) == {"id": 2, "name": "bar"}


def test_read_by_id_returns_none_when_not_found(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})

    assert read_by_id(str(file_path), 999) is None
