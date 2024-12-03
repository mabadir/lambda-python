from base64 import b64decode
from urllib.parse import urlencode
import awsgi
from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(status=200, message="Hello Flask!")


def handler(event, context):
    body = event.get("body", "") or ""
    if event.get("isBase64Encoded", False):
        body = b64decode(body)
    body = awsgi.convert_byte(body)

    httpMethod = ""
    path = ""
    if "httpMethod" in event and "path" in event:
        httpMethod = event["httpMethod"]
        path = event["path"]
    elif "http" in event["requestContext"]:
        if "method" in event["requestContext"]["http"]:
            httpMethod = event["requestContext"]["http"]["method"]
        if "path" in event["requestContext"]["http"]:
            path = event["requestContext"]["http"]["path"]

    queryStringParameters = ""
    if "queryStringParameters" in event and event["queryStringParameters"] is not None:
        queryStringParameters = urlencode(event["queryStringParameters"])
    # Create a copy of the event to avoid mutating the original event
    modified_event = dict(event)

    # Set or change the httpMethod to "GET"
    modified_event["httpMethod"] = httpMethod
    modified_event["path"] = path
    modified_event["queryStringParameters"] = queryStringParameters
    return awsgi.response(app, modified_event, context)
