from pydantic import BaseModel


class AudioFileOut(BaseModel):
    id: int
    filename: str
    filepath: str
    owner_id: int
