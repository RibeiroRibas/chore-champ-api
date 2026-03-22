from datetime import datetime


class RefreshTokenEntity:
    def __init__(self, id: int, auth_id: int, refresh_token: str, created_at: datetime):
        self.id = id
        self.auth_id = auth_id
        self.refresh_token = refresh_token
        self.created_at = created_at
