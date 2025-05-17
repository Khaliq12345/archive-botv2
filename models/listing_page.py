from pydantic import BaseModel, Field


# the model to extract the article detailed information
class Single_ListingPage_Article(BaseModel):
    title: str | None = Field(
        alias="Title",
        description="Extract the title of the article, return None if not found",
    )
    url: str | None = Field(
        alias="URL",
        description="Extract the URL of the article, return None if not found",
    )
    date: str | None = Field(
        alias="Date",
        description="Extract the date of the article, return None if not found",
    )


class Multi_ListingPage_Article(BaseModel):
    data: list[Single_ListingPage_Article]
