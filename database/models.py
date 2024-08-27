from sqlmodel import SQLModel, Field

# create model to register access servers

class Image(SQLModel, table=True):
    id: int = Field(
        default=None, primary_key=True
    )
    name: str = Field(
        max_length=100
    )
    url: str = Field(
        max_length=100
    )

    realPath: str = Field(
        max_length=100
    )

    contentType: str = Field(
        max_length=100
    )




