import json

from poc_crud_lib import create


def test_create_ignores_user_supplied_id_and_assigns_auto_id(tmp_path):
    """CLAUDE.md: create는 id가 이미 포함된 data를 받아도 무시하고 자동 부여한 id로 덮어쓴다."""
    file_path = tmp_path / "data.json"

    record = create(str(file_path), {"id": 999, "name": "foo"})

    assert record == {"id": 1, "name": "foo"}
    assert json.loads(file_path.read_text()) == [{"id": 1, "name": "foo"}]


def test_create_with_empty_data_dict(tmp_path):
    file_path = tmp_path / "data.json"

    record = create(str(file_path), {})

    assert record == {"id": 1}


def test_create_does_not_corrupt_file_when_called_repeatedly(tmp_path):
    file_path = tmp_path / "data.json"

    for i in range(20):
        create(str(file_path), {"n": i})

    records = json.loads(file_path.read_text())
    assert [r["id"] for r in records] == list(range(1, 21))
