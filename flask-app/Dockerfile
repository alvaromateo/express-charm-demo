# syntax=docker/dockerfile:1
FROM python:3.13-alpine
RUN addgroup -S app && adduser -S app -G app
RUN apk add --no-cache gcc musl-dev linux-headers
USER app

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --chown=app:app . ./

# TODO: add possibility to attach debugger

CMD ["python3", "-m", "flask", "run", "--debug"]
