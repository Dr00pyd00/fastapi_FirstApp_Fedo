from typing import Optional

from pydantic import BaseModel



#========== TOKEN SCHEMAS =================#
class TokenDataSchema(BaseModel):
    id: Optional[int] = None


class TokenOutSchema(BaseModel):
    access_token: str
    token_type: str
