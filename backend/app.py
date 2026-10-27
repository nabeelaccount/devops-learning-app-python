import hmac
import json
import logging
import os
import re
import socket
import sys
import uuid
from datetime import datetime

from flask import Flask, g, jsonify, request

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)

DATA_DIR = os.getenv("DATA_DIR", "/data")
DATA_FILE = os.path.join(DATA_DIR, "people.json")

# Fail at startup if the secret was not injected: a broken secret
# pipeline should be loud, not discovered later.
SECRET = os.environ.get("SECURE_PASSWORD")
if not SECRET:
    sys.exit("SECURE_PASSWORD is not set")

# Client-supplied IDs are untrusted: allow only a safe charset and length
# so nobody can inject newlines or junk into your logs.
SAFE_ID = re.compile(r"^[A-Za-z0-9\-_=;.:]{1,128}$")


@app.before_request
def assign_request_id():
    incoming = request.headers.get("X-Request-Id") or request.headers.get("X-Amzn-Trace-Id")
    g.request_id = incoming if incoming and SAFE_ID.match(incoming) else str(uuid.uuid4())


@app.after_request
def finish_request(response):
    response.headers["X-Request-Id"] = g.request_id
    logging.info("%s %s %s id=%s", request.method, request.path, response.status_code, g.request_id)
    return response


def load_people():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_people(people):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(people, f)


@app.route("/")
def index():
    return {"message": "Welcome to the backend! 🚀"}


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/whoami")
def whoami():
    return {"served_by": socket.gethostname()}


@app.route("/secure")
def secure():
    supplied = request.headers.get("X-API-Key", "")
    if not hmac.compare_digest(supplied.encode(), SECRET.encode()):
        return {"error": "invalid or missing API key"}, 401
    return {"secret_loaded": True, "length": len(SECRET)}


@app.route("/people", methods=["GET"])
def list_people():
    return jsonify(load_people())


@app.route("/people", methods=["POST"])
def create_person():
    data = request.get_json(silent=True) or {}
    name, email, dob = data.get("name"), data.get("email"), data.get("dob")

    if not (name and email and dob):
        return {"error": "name, email and dob are required"}, 400

    try:
        datetime.strptime(dob, "%d-%m-%Y")
    except ValueError:
        return {"error": "dob must be DD-MM-YYYY"}, 400

    person = {"name": name, "email": email, "dob": dob}
    people = load_people()
    people.append(person)
    save_people(people)

    return person, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)