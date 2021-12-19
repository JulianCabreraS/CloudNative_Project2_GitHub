FROM python:3.7-alpine
LABEL maintainer="Julian CabreraS"

COPY ./app /app
WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev build-base python3-dev
RUN pip install -r requirements.txt

EXPOSE 5006

CMD [ "python", "main.py"]
