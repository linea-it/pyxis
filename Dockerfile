FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN apk update && apk add gcc python3-dev musl-dev libressl-dev openldap-dev
RUN pip install -r requirements.txt
CMD ["/bin/sh"]
