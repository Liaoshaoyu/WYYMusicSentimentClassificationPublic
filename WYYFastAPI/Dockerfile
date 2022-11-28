FROM python:3.9

ADD ./WYYFastAPI /code

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /code

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 8080

CMD ["python", "/code/main.py"]