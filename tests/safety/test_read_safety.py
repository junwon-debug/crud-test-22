from poc_crud_lib import create, read_all, read_by_id


def test_read_all_on_existing_empty_array_file(tmp_path):
    file_path = tmp_path / "data.json"
    file_path.write_text("[]")

    assert read_all(str(file_path)) == []


def test_read_by_id_does_not_match_wrong_type(tmp_path):
    """id는 int 체계이므로 문자열 "1"과 정수 1은 다른 값으로 취급되어야 한다."""
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})  # id=1

    assert read_by_id(str(file_path), "1") is None


def test_read_by_id_on_missing_file_returns_none(tmp_path):
    file_path = tmp_path / "data.json"

    assert read_by_id(str(file_path), 1) is None


def test_read_all_returns_independent_copies_not_shared_state(tmp_path):
    """반환된 리스트/레코드를 변경해도 파일에 저장된 원본 데이터에 영향이 없어야 한다."""
    file_path = tmp_path / "data.json"
    create(str(file_path), {"name": "foo"})

    records = read_all(str(file_path))
    records[0]["name"] = "mutated"
    records.append({"id": 999, "name": "injected"})

    fresh = read_all(str(file_path))
    assert fresh == [{"id": 1, "name": "foo"}]
