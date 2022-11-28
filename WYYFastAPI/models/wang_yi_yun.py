import datetime
from typing import Any, Optional

from beanie import Document
from pydantic import BaseModel


class SongCommentsRes(BaseModel):
    status_code: int
    data: Optional[Any]

class SongCommentsReq(BaseModel):
    page: int
    page_size: int
    positive: Optional[bool]
    content: Optional[str]


class SongCommentsData(Document):
    comment_id: int
    content: str
    song_name: str
    time: int
    positive: Any
    classify_by: Any
    deleted: int

    class Collection:
        name = "CommentInfo"

class SongCommentsUpdateReq(BaseModel):
    id: str
    positive: bool
    classify_by: str

class CommentLengthData(Document):
    create_time: datetime.datetime
    xaxis: Any
    yaxis: Any
    deleted: int

    class Collection:
        name = "ContentLength"


class WordCloudData(Document):
    create_time: datetime.datetime
    word_cloud: Any
    deleted: int

    class Collection:
        name = "WordCloud"
