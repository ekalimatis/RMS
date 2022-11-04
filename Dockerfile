FROM python:3.9-alpine

WORKDIR /rms

COPY ./requirements.txt /rms/requirements.txt

RUN apk add build-base

RUN apk add --no-cache supervisor \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /rms

EXPOSE 5000

ENTRYPOINT [ "sh" ]

CMD ["run.sh"]

