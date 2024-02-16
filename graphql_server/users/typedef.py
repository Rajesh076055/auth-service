import strawberry


@strawberry.type
class UserData:
    id: int
    name: str
    email: str
    number: int
    address: str


@strawberry.type
class UserToken:
    token: str