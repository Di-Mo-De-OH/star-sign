.PHONY: format type test coverage check

# 코드 포맷팅 + 린트 검사 + 린트 자동 수정
format:
	poetry run black .
	poetry run ruff check --fix .
	poetry run ruff check .

# 타입 검사
type:
	poetry run mypy .

# 테스트 실행
test:
	poetry run pytest

# 커버리지 실행
coverage:
	poetry run coverage run -m pytest
	poetry run coverage report

# 전체 검사 (포맷 + 린트 + 타입 + 테스트 + 커버리지)
check:
	poetry run black --check .
	poetry run ruff check .
	poetry run mypy .
	poetry run coverage run -m pytest
	poetry run coverage report
