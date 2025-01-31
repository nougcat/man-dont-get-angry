FROM python:slim-bookworm

WORKDIR /app

COPY requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy in the source code
COPY server.py /app
EXPOSE 2137

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "2137"]


# copied from https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
