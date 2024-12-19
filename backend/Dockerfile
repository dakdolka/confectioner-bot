FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry install
RUN poetry update

ENTRYPOINT [ "python", "run.py" ]