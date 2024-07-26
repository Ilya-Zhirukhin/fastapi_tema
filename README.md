pip install -r requirements.txt

$env:PYTHONPATH = "C:\Users\Илья\Desktop\py_upscale\fastapi_edu\fastapi_tema;$env:PYTHONPATH"

docker-compose -f docker-compose-local.yaml up -d



uvicorn "fastapi_tema.aplication.main:app" --host "localhost" --port "8000" --reload
