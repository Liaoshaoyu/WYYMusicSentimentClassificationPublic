# 生产容器
FROM nginx:1.16.0-alpine

ADD ./dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]