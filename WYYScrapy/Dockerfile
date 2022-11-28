FROM python:3.9

ADD ./WYYScrapy /code

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /code

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD ["nohup", "python", "/code/main.py", "&"]