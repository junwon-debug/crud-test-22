# poc-crud-lib

JSON 파일을 저장소로 사용하는 CRUD POC 라이브러리입니다. 자세한 설계 배경과 스펙은 [CLAUDE.md](./CLAUDE.md)를 참고하세요.

## 설치

```bash
uv sync
```

## 사용 예제

```python
from poc_crud_lib import create, read_all, read_by_id, update, delete

file_path = "data.json"

# Create: 데이터를 저장하면 자동 증가 id가 부여된 레코드가 반환된다.
foo = create(file_path, {"name": "foo", "value": 1})
# {"name": "foo", "value": 1, "id": 1}

bar = create(file_path, {"name": "bar"})
# {"name": "bar", "id": 2}

# Read: 전체 목록 조회
read_all(file_path)
# [{"name": "foo", "value": 1, "id": 1}, {"name": "bar", "id": 2}]

# Read: id로 단건 조회 (없으면 None)
read_by_id(file_path, foo["id"])
# {"name": "foo", "value": 1, "id": 1}

read_by_id(file_path, 999)
# None

# Update: 일부 필드만 부분 갱신(patch), 나머지 필드는 유지된다.
update(file_path, foo["id"], {"value": 2})
# {"name": "foo", "value": 2, "id": 1}

# Update: 존재하지 않는 id는 ValueError
update(file_path, 999, {"value": 3})
# ValueError: record with id 999 not found

# Delete: 대상이 없으면 삭제 전 ValueError를 발생시키고 원본 파일은 유지된다.
delete(file_path, bar["id"])

delete(file_path, 999)
# ValueError: record with id 999 not found
```

## 함수 시그니처

```python
def create(file_path: str, data: dict) -> dict: ...
def read_all(file_path: str) -> list[dict]: ...
def read_by_id(file_path: str, id: int) -> dict | None: ...
def update(file_path: str, id: int, fields: dict) -> dict: ...
def delete(file_path: str, id: int) -> None: ...
```

## 테스트 실행

```bash
uv run pytest
```

- `tests/regression/`: 정상 동작(happy path) 회귀 테스트
- `tests/safety/`: 경계 조건을 파고드는 공격적 안전성 테스트
