FROM:python:3.10-slim


WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY ..

CMD ['uvicom","main:app","--host","--port","8000"]
