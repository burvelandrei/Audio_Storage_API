from pydantic import BaseModel


class AudioFileSchema(BaseModel):
    id: int
    filename: str
    filepath: str
    owner_id: int
