class APIError(Exception):
    status_code: int
    reason: str
    
    def __init__(self, status_code: int, reason: str, *args) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.reason = reason
