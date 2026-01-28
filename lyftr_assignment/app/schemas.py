from pydantic import BaseModel, Field, field_validator
import re

class WebhookPayload(BaseModel):
    message_id: str = Field(..., min_length=1)
    from_msisdn: str = Field(..., alias="from")
    to_msisdn: str = Field(..., alias="to")
    ts: str
    text: str | None = Field(None, max_length=4096)

    @field_validator("from_msisdn", "to_msisdn")
    @classmethod
    def validate_e164(cls, v):
        if not re.match(r"^\+\d+$", v):
            raise ValueError("Must start with + and contain only digits")
        return v