from flask import Flask, request, jsonify, render_template
import os
import pycurl
from io import BytesIO

## Config App
app = Flask(__name__)


# Curl Function
def curl_url(target_url: str):
    """ This function performs basic curl against url - basic function """
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, target_url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return (body.decode('utf-8'))

## Create Homepage with CURL
@app.route("/")
def default():
    return render_template('index.html')

## Create Curl API Endpoint
@app.route("/curl")
def do_curl():
    ## Simple API interface for curl request
    target_url = request.args.get("target_url")

    if target_url is None:
        target_url = request.form.get("target_url")

    result = "EMPTY"
    
    print(f"Target URL: {target_url}")
    if target_url is not None:
        result = curl_url(target_url=target_url)
    
    return jsonify(result)

## info dump App Hosting
@app.route("/info")
def info_dump():
    ## Output options
    result = {}
    result["method"] = str(request.method)
    result["base_url"] = str(request.base_url)
    result["query_string"] = str(request.query_string)   
    result["url"] = str(request.url)
    result["headers"] = str(request.headers)
    result["host"] = str(request.host)
    result["host_url"] = str(request.host_url)
    result["full_path"] = str(request.full_path)
    result["endpoint"] = str(request.endpoint)
    result["form"] = str(request.form.to_dict())
    result["files"] = str(request.files.to_dict())
    result["data"] = str(request.data)
    result["content_encoding"] = str(request.content_encoding)
    result["content_length"] = str(request.content_length)
    result["content_type"] = str(request.content_type)
    result["stream"] = str(request.stream)
    result["cookies"] = str(request.cookies.to_dict())
    result["user_agent"] = str(request.user_agent)
    result["authorization"] = str(request.authorization)
    result["cache_control"] = str(request.cache_control)
    result["date"] = str(request.date)
    result["mimetype"] = str(request.mimetype)
    result["is_secure"] = str(request.is_secure)
    result["scheme"] = str(request.scheme)
    result["remote_addr"] = str(request.remote_addr)
    result["remote_user"] = str(request.remote_user)
    result["values"] = str(request.values.to_dict())
    envars = {}
    for k, v in os.environ.items():
        envars[k] = v
    result["environment_variables"] = envars

    if request.content_type == 'application/json':
        result["json"] = request.json

    return jsonify(result)


if __name__ == "__main__":
    ## Setup APP
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None:
        import google.cloud.logging
        LoggingClient = google.cloud.logging.Client()
        LoggingClient.get_default_handler()
        LoggingClient.setup_logging()

    ## Run APP

    app.run(host='0.0.0.0', port=8080, debug=True)