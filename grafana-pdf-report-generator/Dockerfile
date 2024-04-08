FROM python:3.12.0-alpine3.18

RUN apk add go=1.20.10-r0 texlive=20230506.66984-r0

RUN go install -v github.com/IzakMarais/reporter/cmd/grafana-reporter@latest

RUN mv /root/go/bin/grafana-reporter /usr/local/bin/

RUN mkdir -p /app &&\
    chown nobody:nogroup /app

WORKDIR /app

COPY --chown=nobody:nogroup requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY --chown=nobody:nogroup ./main.py .

USER nobody

CMD ["python3", "main.py"]

