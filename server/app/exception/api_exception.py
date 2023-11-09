class APIExceptionBase(Exception):
    status: int
    message: str

    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

    def make_content(self):
        return {"message": self.message}


class UserNotFoundException(APIExceptionBase):
    user_id: str

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(404, f"user not found.")

    def make_content(self):
        return {"message": self.message, "user_id": self.user_id}
