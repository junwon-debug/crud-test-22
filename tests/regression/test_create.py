import json

from poc_crud_lib import create, delete


def test_create_assigns_incremental_id_and_persists_to_file(tmp_path):
    file_path = tmp_path / "data.json"

    record = create(str(file_path), {"name": "foo"})

    assert record == {"id": 1, "name": "foo"}
    assert json.loads(file_path.read_text()) == [{"id": 1, "name": "foo"}]


def test_create_reuses_id_after_deletion_via_max_plus_one(tmp_path):
    """CLAUDE.md: id는 파일 내 최댓값 + 1로 부여되므로, 삭제로 id가 비면 재사용될 수 있다."""
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})  # id=1
    create(str(file_path), {"name": "bar"})  # id=2

    delete(str(file_path), 2)
    record = create(str(file_path), {"name": "baz"})

    assert record["id"] == 2
