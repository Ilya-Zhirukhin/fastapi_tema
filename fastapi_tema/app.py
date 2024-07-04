""" main app """

from fastapi import FastAPI
from pydantic import BaseModel
from .settings import settings


app = FastAPI()

class Status(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    status:str = "ok"
    
@app.get(settings.main_url)
async def status():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Status()

