from pydantic import BaseModel, field_serializer


class AudioFileOut(BaseModel):
    id: int
    filename: str
    filepath: str
    owner_id: int

    @field_serializer('filepath')
    def serialize_filepath(self, filepath: str) -> str:
        return filepath.replace('\\', '/')
