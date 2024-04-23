from pydantic import BaseModel


class UserSchema(BaseModel):
    mail_enabled: bool
    destination_email: str | None = None
