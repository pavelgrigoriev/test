from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    mail_enabled: bool = False
    destination_email: str = None
