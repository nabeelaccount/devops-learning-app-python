FROM        dhi.io/python:3-alpine3.23-dev AS build

WORKDIR     /app

RUN         python -m venv /venv
ENV         PATH="/venv/bin:$PATH"

# Final stage has no SHELL to create directory and runs as non-root
RUN         mkdir /data

COPY        requirements.txt .
RUN         python -m pip install --upgrade pip && \
            python -m pip install -r requirements.txt



FROM        dhi.io/python:3-alpine AS runtime

WORKDIR     /app

COPY        --from=build /venv /venv
ENV         PATH="/venv/bin:$PATH"

COPY        --from=build --chown=65532:65532 /data /data

# used '--chown' instead of doing it at the build stage because:
# - once COPY here, the directoy will be assigned to root user (0)
# - even if the content/files inside will be for user 65532.
# - using' --chown' both the directory files inside will be of user 65532


COPY        . .
ENV         DATA_DIR=/data 
EXPOSE      8080


HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c  "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"


ENTRYPOINT ["gunicorn"]
CMD         ["--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]