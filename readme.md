sudo docker compse run --entrypoint "poetry init --name demo-app --dependency fastapi --dependency uvicorn[standard]" demo-app

# 라이브러리 설치
sudo docker compose run --entrypoint "poetry install --no-root" demo-app

# 실행
sudo docker compose up

# DB 테이블 생성
docker compose exec demo-app poetry run python -m api.migrate_db

# SQL 생성 확인
docker compose exec db mysql demo

