FROM python:3.9

EXPOSE 80

COPY ./app /app

WORKDIR /app

CMD pwd

RUN pip install -r app/requirement.txt

CMD ["uvicorn", "server.app:server", "--host", "0.0.0.0", "--port", "80"]
