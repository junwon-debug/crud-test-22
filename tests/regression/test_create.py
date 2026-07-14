import json

from poc_crud_lib import create


def test_create_assigns_incremental_id_and_persists_to_file(tmp_path):
    file_path = tmp_path / "data.json"

    record = create(str(file_path), {"name": "foo"})

    assert record == {"id": 1, "name": "foo"}
    assert json.loads(file_path.read_text()) == [{"id": 1, "name": "foo"}]
