from pydantic import BaseModel

class AskRequest(BaseModel):
    text: str

class AskResponse(BaseModel):
    answer: str
