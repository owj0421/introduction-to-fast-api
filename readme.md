sudo docker compse run --entrypoint "poetry init --name demo-app --dependency fastapi --dependency uvicorn[standard]" demo-app

sudo docker compose run --entrypoint "poetry install --no-root" demo-app

sudo docker compose up