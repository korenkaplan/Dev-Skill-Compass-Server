from pydantic import BaseModel


class ProxyObjectDto(BaseModel):
    ip_address: str
    port: int
    https: bool

    class Config:
        arbitrary_types_allowed = True
