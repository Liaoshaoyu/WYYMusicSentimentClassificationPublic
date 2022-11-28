from datetime import datetime, timedelta
import time
from typing import List, Union

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from models.admin import Admin
from models.student import Student
from models.wang_yi_yun import SongCommentsData, CommentLengthData, WordCloudData

admin_collection = Admin
student_collection = Student
song_comments_data = SongCommentsData


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False


async def get_song_comments(req: dict) -> (List[SongCommentsData], int):
    condition = {'deleted': 0}
    if req.get('positive') is not None:
        condition['positive'] = req.get('positive')
    if req.get('content'):
        condition['content'] = {'$regex': req.get('content')}

    data = await song_comments_data.find_many(
        condition, sort=[('time', -1)], skip=(req.get('page') - 1) * 10, limit=req.get('page_size')
    ).to_list()
    cnt = await song_comments_data.find_many(condition).count()

    return data, cnt


async def update_song_comments(req: dict) -> None:
    des_body = {k: v for k, v in req.items() if k != 'id'}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    comment = await song_comments_data.get(req['id'])

    if comment:
        await comment.update(update_query)


async def get_song_comments_indicator() -> dict:
    data = dict()
    today_start = datetime.strptime(datetime.now().strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')
    ytd_start = int(time.mktime((today_start - timedelta(days=1)).timetuple()) * 1000)
    ytd_end = int(time.mktime(today_start.timetuple()) * 1000)

    condition = {'deleted': 0}
    data['comments_total'] = await song_comments_data.find_many(condition).count()

    condition['time'] = {'$gte': ytd_start, '$lt': ytd_end}
    data['comments_ytd'] = await song_comments_data.find_many(condition).count()

    condition.pop('time')
    condition['positive'] = {'$ne': None}
    data['has_emotion'] = await song_comments_data.find_many(condition).count()

    condition.pop('positive')
    condition['classify_by'] = '手动分类'
    data['manual'] = await song_comments_data.find_many(condition).count()

    return data


async def get_song_comments_category() -> list:
    data = []
    condition = {'deleted': 0}
    condition['positive'] = {'$eq': True}
    positive_num = await song_comments_data.find_many(condition).count()
    data.append({'name': '积极评论数', 'value': positive_num})

    condition['positive'] = {'$eq': False}
    negative_num = await song_comments_data.find_many(condition).count()
    data.append({'name': '消极评论数', 'value': negative_num})

    return data


async def get_song_comments_top10() -> dict:
    data = {}
    condition = {'deleted': 0, 'positive': {'$eq': True}}

    class OutputItem(BaseModel):
        song_name: str = Field(None, alias="_id")
        cnt: int


    positive_result = await song_comments_data.find(condition).aggregate(
        [{"$group": {"_id": "$song_name", "cnt": {"$sum": 1}}},
         {"$sort": {"cnt": -1}},
         {"$limit": 10}],
        projection_model=OutputItem
    ).to_list()
    positive_arr = []
    for ps in positive_result:
        positive_arr.append(
            [ps.song_name, ps.cnt]
        )
    data['positive'] = positive_arr

    condition['positive'] = {'$eq': False}
    negative_result = await song_comments_data.find(condition).aggregate(
        [{"$group": {"_id": "$song_name", "cnt": {"$sum": 1}}}],
        projection_model=OutputItem
    ).to_list()
    negative_arr = []
    for arr in data['positive']:
        song_name = arr[0]
        negative_num = 0
        for ns in negative_result:
            if song_name == ns.song_name:
                negative_num = ns.cnt
                break

        negative_arr.append([song_name, negative_num])
    data['negative'] = negative_arr

    return data

async def get_song_comments_length() -> dict:
    condition = {'deleted': 0}
    result = await CommentLengthData.find_many(condition, sort=[('create_time', -1)], limit=1).to_list()

    return result[0]

async def get_song_comments_word_cloud() -> dict:
    condition = {'deleted': 0}
    result = await WordCloudData.find_many(condition, sort=[('create_time', -1)], limit=1).to_list()

    return result[0]