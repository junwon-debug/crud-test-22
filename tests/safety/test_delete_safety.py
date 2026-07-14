import json

import pytest

from poc_crud_lib import create, delete, read_all


def test_delete_only_removes_target_record(tmp_path):
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    target = create(str(file_path), {"name": "bar"})
    create(str(file_path), {"name": "baz"})

    delete(str(file_path), target["id"])

    assert read_all(str(file_path)) == [
        {"id": 1, "name": "foo"},
        {"id": 3, "name": "baz"},
    ]


def test_delete_all_records_results_in_valid_empty_array_file(tmp_path):
    file_path = tmp_path / "data.json"
    record = create(str(file_path), {"name": "foo"})

    delete(str(file_path), record["id"])

    assert json.loads(file_path.read_text()) == []
    assert read_all(str(file_path)) == []


def test_delete_on_missing_file_raises_value_error(tmp_path):
    file_path = tmp_path / "data.json"

    with pytest.raises(ValueError):
        delete(str(file_path), 1)


def test_delete_failure_leaves_original_file_untouched(tmp_path):
    """존재하지 않는 id로 delete 실패 시, 원본 파일 내용이 손상되지 않아야 한다."""
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})
    before = file_path.read_text()

    with pytest.raises(ValueError):
        delete(str(file_path), 999)

    assert file_path.read_text() == before
