pip install -r requirements.txt

docker-compose -f docker-compose-local.yaml up -d

uvicorn "fastapi_tema.aplication.main:app" --host "localhost" --port "8000" --reload
