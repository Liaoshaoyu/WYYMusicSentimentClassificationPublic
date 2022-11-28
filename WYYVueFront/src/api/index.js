import request from './request';

export const fetchData = query => {
    return request({
        url: './table.json',
        method: 'get',
        params: query
    });
};

export function get_song_comments(req) {
    return request.post('/wyy/song/comments', req)
}

export function update_song_comments(req) {
    return request.put('/wyy/song/comments/update', req)
}

export function get_song_comments_indicator() {
    return request.get('/wyy/song/comments/indicator')
}

export function get_song_comments_category() {
    return request.get('/wyy/song/comments/category')
}

export function get_song_comments_top10() {
    return request.get('/wyy/song/comments/top10')
}

export function get_song_comments_length() {
    return request.get('/wyy/song/comments/length')
}

export function get_song_comments_word_cloud() {
    return request.get('/wyy/song/comments/word_cloud')
}