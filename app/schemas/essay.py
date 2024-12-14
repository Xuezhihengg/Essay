from pydantic import BaseModel

class Essay(BaseModel):
    content: str
    grade: str
    title: str
    model_content: str