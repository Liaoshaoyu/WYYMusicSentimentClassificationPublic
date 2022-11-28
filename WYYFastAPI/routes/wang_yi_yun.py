import time

from fastapi import APIRouter, Body

from database.database import get_song_comments, update_song_comments, get_song_comments_indicator, \
    get_song_comments_category, get_song_comments_top10, get_song_comments_length, get_song_comments_word_cloud
from models.wang_yi_yun import SongCommentsRes, SongCommentsReq, SongCommentsUpdateReq

router = APIRouter()


@router.post(path="/song/comments", response_description="网易云音乐数据", response_model=SongCommentsRes)
async def api_song_comments(req: SongCommentsReq = Body(...)):
    song_comments_data = await get_song_comments(req=req.dict())
    cnt = song_comments_data[1]
    song_comments_data = song_comments_data[0]
    data = []
    for scd in song_comments_data:
        temp_dict = scd.dict()
        if isinstance(temp_dict.get('time'), int):
            time_array = time.localtime(temp_dict.get('time') / 1000)
            temp_dict['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        else:
            temp_dict['time_str'] = ''

        data.append(temp_dict)

    return {
        "status_code": 200,
        "data": {
            'list': data,
            'total': cnt
        }
    }


@router.put(path="/song/comments/update", response_description="评论更新")
async def api_song_comments_update(req: SongCommentsUpdateReq = Body(...)):
    await update_song_comments(req=req.dict())

    return {
        "status_code": 200
    }


@router.get(path="/song/comments/indicator", response_description="网易云音乐数据指标卡", response_model=SongCommentsRes)
async def api_song_comments_indicator():
    song_comments_indicator_data = await get_song_comments_indicator()

    return {
        "status_code": 200,
        "data": song_comments_indicator_data
    }

@router.get(path="/song/comments/category", response_description="网易云音乐数据饼图分类", response_model=SongCommentsRes)
async def api_song_comments_category():
    song_comments_category_data = await get_song_comments_category()

    return {
        "status_code": 200,
        "data": song_comments_category_data
    }

@router.get(path="/song/comments/top10", response_description="网易云音乐数据柱形图top10", response_model=SongCommentsRes)
async def api_song_comments_top10():
    song_comments_top10_data = await get_song_comments_top10()

    return {
        "status_code": 200,
        "data": song_comments_top10_data
    }

@router.get(path="/song/comments/length", response_description="网易云音乐数据直方图", response_model=SongCommentsRes)
async def api_song_comments_length():
    song_comments_length_data = await get_song_comments_length()

    return {
        "status_code": 200,
        "data": song_comments_length_data
    }

@router.get(path="/song/comments/word_cloud", response_description="网易云音乐数据词云", response_model=SongCommentsRes)
async def api_song_comments_word_cloud():
    song_comments_word_cloud_data = await get_song_comments_word_cloud()
    temp_dict = song_comments_word_cloud_data.dict()
    cnt = 0
    if temp_dict.get('word_cloud'):
        word_arr = []
        for key, val in temp_dict['word_cloud'].items():
            word_arr.append({'name': key, 'value': val})
            cnt += 1
            if cnt > 100:
                break
    else:
        word_arr = []
    return {
        "status_code": 200,
        "data": word_arr
    }