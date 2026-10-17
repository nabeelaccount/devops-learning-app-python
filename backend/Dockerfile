FROM        python:3.14.6-alpine AS build

WORKDIR     /app

RUN         python -m venv /venv
ENV         PATH="/venv/bin:$PATH"

COPY        requirements.txt .
RUN         python -m pip install --upgrade pip && \
            python -m pip install -r requirements.txt



FROM        python:3.14.6-alpine AS development

WORKDIR     /app

COPY        --from=build /venv /venv
ENV         PATH="/venv/bin:$PATH"


COPY        . .
ENV         DATA_DIR=data 
EXPOSE      8080

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c  "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

ENTRYPOINT ["gunicorn"]
CMD         ["--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]