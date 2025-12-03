from pydantic import BaseModel, ConfigDict


class OAuthSessionModel(BaseModel):
    id: str
    user_id: str
    provider: str
    token: dict
    expires_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)
