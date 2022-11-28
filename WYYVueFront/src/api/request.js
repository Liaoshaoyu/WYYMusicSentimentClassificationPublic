import axios from 'axios';

let baseURL = 'http://0.0.0.0:8001/';
if (process.env.NODE_ENV === 'production') {
  baseURL = '/';
}

const service = axios.create({
    baseURL,
    timeout: 10000
});

service.interceptors.request.use(
    config => {
        return config;
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
);

service.interceptors.response.use(
    response => {
        if (response.status === 200) {
            return response.data;
        } else {
            Promise.reject();
        }
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
);

export default service;
