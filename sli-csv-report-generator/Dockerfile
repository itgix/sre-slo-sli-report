
FROM python:3.12.0-alpine3.18

RUN apk add --no-cache build-base libffi-dev

RUN mkdir -p /app &&\
    chown nobody:nogroup /app

WORKDIR /app

COPY --chown=nobody:nogroup requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY --chown=nobody:nogroup ./main.py .

USER nobody

CMD ["python3", "main.py"]
