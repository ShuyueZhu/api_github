import identity
import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
import json
import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

access_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6IlpZS3VuNHdUNVhqbm9JZlNCdEZMSF91UGxhUkFlWThYOWI3aF9fMTVNY2ciLCJhbGciOiJSUzI1NiIsIng1dCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSIsImtpZCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yYjg5NzUwNy1lZThjLTQ1NzUtODMwYi00ZjgyNjdjM2QzMDcvIiwiaWF0IjoxNzA5MjI0NDc5LCJuYmYiOjE3MDkyMjQ0NzksImV4cCI6MTcwOTMxMTE3OSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQVhvWGNtbzk2S0s0WGdhMWhkVTlYK0gxbGtxaGduWEJCeTlHK0NzR0ZzK2tHYmVjZy9Wb3BjQU1ZajNkTzZ1dVR2aTJoOGZxMEdvNmtvTnBJdUw2anRvZnc4ek9WT1pMRzU1czZ1eTgweFgwPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImNhcG9saWRzX2xhdGViaW5kIjpbImYwN2Q1YmI4LWYxMmMtNGE2My04NTY2LWVlMDE5NDUzNjJhZCJdLCJmYW1pbHlfbmFtZSI6IlpIVSIsImdpdmVuX25hbWUiOiJTSFVZVUUiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIzMS4yMDUuMjE0Ljk0IiwibmFtZSI6IlpIVSwgU0hVWVVFIiwib2lkIjoiY2E3YTBhOTUtYzY0Ny00MTEyLThmNjAtNTQyNWE3OGZlMTIyIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTI0MzAzNzIwNi00MTk1NTU1OC01NjEzMzIyNzUtMjQwNDQzNyIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzMjAwMjg5NTEzNzk5IiwicmgiOiIwLkFRa0FCM1dKSzR6dWRVV0RDMC1DWjhQVEJ3TUFBQUFBQUFBQXdBQUFBQUFBQUFBSkFGUS4iLCJzY3AiOiJBUElDb25uZWN0b3JzLlJlYWQuQWxsIEFQSUNvbm5lY3RvcnMuUmVhZFdyaXRlLkFsbCBBcHBsaWNhdGlvbi5SZWFkLkFsbCBBcHBsaWNhdGlvbi5SZWFkV3JpdGUuQWxsIEF1ZGl0TG9nLlJlYWQuQWxsIENhbGVuZGFycy5SZWFkIENhbGVuZGFycy5SZWFkQmFzaWMgQ2FsZW5kYXJzLlJlYWRXcml0ZSBDb250YWN0cy5SZWFkV3JpdGUgRGV2aWNlLkNvbW1hbmQgRGV2aWNlLlJlYWQgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5Qcml2aWxlZ2VkT3BlcmF0aW9ucy5BbGwgRGV2aWNlTWFuYWdlbWVudE1hbmFnZWREZXZpY2VzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZFdyaXRlLkFsbCBEaXJlY3RvcnkuQWNjZXNzQXNVc2VyLkFsbCBEaXJlY3RvcnkuUmVhZC5BbGwgRGlyZWN0b3J5LlJlYWRXcml0ZS5BbGwgRWR1QWRtaW5pc3RyYXRpb24uUmVhZCBFZHVSb3N0ZXIuUmVhZCBFZHVSb3N0ZXIuUmVhZFdyaXRlIEZpbGVzLlJlYWRXcml0ZS5BbGwgR3JvdXAuUmVhZFdyaXRlLkFsbCBNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbGJveFNldHRpbmdzLlJlYWQgTWFpbGJveFNldHRpbmdzLlJlYWRXcml0ZSBOb3Rlcy5SZWFkV3JpdGUuQWxsIG9wZW5pZCBQZW9wbGUuUmVhZCBQcmVzZW5jZS5SZWFkIFByZXNlbmNlLlJlYWQuQWxsIHByb2ZpbGUgUmVwb3J0cy5SZWFkLkFsbCBTZXJ2aWNlSGVhbHRoLlJlYWQuQWxsIFNpdGVzLkZ1bGxDb250cm9sLkFsbCBTaXRlcy5SZWFkV3JpdGUuQWxsIFRhc2tzLlJlYWRXcml0ZSBUZWFtc1RhYi5DcmVhdGUgVGVhbXNUYWIuUmVhZFdyaXRlLkFsbCBUZWFtd29ya0RldmljZS5SZWFkLkFsbCBUZWFtd29ya0RldmljZS5SZWFkV3JpdGUuQWxsIFVzZXIuUmVhZCBVc2VyLlJlYWQuQWxsIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBVc2VyLlJlYWRXcml0ZS5BbGwgVXNlckF1dGhlbnRpY2F0aW9uTWV0aG9kLlJlYWQgVXNlckF1dGhlbnRpY2F0aW9uTWV0aG9kLlJlYWQuQWxsIFVzZXJBdXRoZW50aWNhdGlvbk1ldGhvZC5SZWFkV3JpdGUgVXNlckF1dGhlbnRpY2F0aW9uTWV0aG9kLlJlYWRXcml0ZS5BbGwgV2luZG93c1VwZGF0ZXMuUmVhZFdyaXRlLkFsbCBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6ImZGYmE3WG1Tb3lZbnE1NUk4MEk5V2swRG5rQ09XelBJOGZTb1duNGJnOUkiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiRVUiLCJ0aWQiOiIyYjg5NzUwNy1lZThjLTQ1NzUtODMwYi00ZjgyNjdjM2QzMDciLCJ1bmlxdWVfbmFtZSI6InN6MjIyM0BpYy5hYy51ayIsInVwbiI6InN6MjIyM0BpYy5hYy51ayIsInV0aSI6Ik1XM1BUNHVveEVtcEhDMU5vUnhKQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2MiOlsiQ1AxIl0sInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6IjM1RVdkcWhtbmlsM2ZaNEFtZ3VqRzVrNThlS3NMUVdTVURTdVU1RFJ4ZncifSwieG1zX3RjZHQiOjE0MDU0MjQzMTh9.JRs0UajmSE7rNFOM6OaEwQNftrcpQHhmWnfG8u8HRff1oM1YYDPSdO7NUCTAnBdSFYI5KriLeWTZCFV2gT5V9qxyZDDR47tbt_TiRO0OnYVoXuZrl2-0MeT-SpbsywXUKm-NJjJp6qwXMFxRyytLS4peQ1iEt3FmWZfX053tAjw2CNwVNH3fOq593L3lMl4YGp_GLimj-03v2bX6pd8kJKSJOsMly-5OLEId5owLUukA5iKhNIpaxopBz64DmAayH-XbrhpbMnR8BfkHALrvTuujVAh_9WZ6ZXx5hH-s0ortjnEfODwYaN6h_PSSwqV8heH9Utequ6fIUYjUNF5MMQ'

@app.route("/login")
def login():
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        ))


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/")
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user(), version=identity.__version__)


@app.route("/list_onenote_notebooks")
def list_onenote_notebooks():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    # 初始化笔记本名称列表
    notebook_names = []
    # 获取笔记本列表
    notebooks_response = requests.get(
        "https://graph.microsoft.com/v1.0/me/onenote/notebooks",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    )

    if notebooks_response.status_code != 200:
        return json.dumps({"error": "Failed to fetch notebooks. Status code: {}".format(notebooks_response.status_code)})

    notebooks_data = notebooks_response.json()

    # 遍历笔记本，提取名称
    for notebook in notebooks_data["value"]:
        notebook_names.append(notebook["displayName"])

    # 返回笔记本名称列表的 JSON 格式
    return json.dumps(notebook_names)


@app.route("/create_notebook")
def create_notebook_form():
    return render_template("create_notebook.html")

@app.route("/create_onenote_notebook", methods=["POST"])
def create_onenote_notebook():
    # 获取用户输入的笔记本名称
    notebook_name = request.form.get("notebook_name")
    if not notebook_name:
        return json.dumps({"error": "Notebook name is required"})

    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    # 创建笔记本
    create_notebook_url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks"
    create_notebook_payload = {
        "displayName": notebook_name
    }
    create_notebook_headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    create_notebook_response = requests.post(
        create_notebook_url,
        headers=create_notebook_headers,
        json=create_notebook_payload,
        timeout=30,
    )

    if create_notebook_response.status_code != 201:
        return json.dumps({"error": "Failed to create notebook. Status code: {}".format(create_notebook_response.status_code)})

    return render_template("create_notebook.html", version=identity.__version__)


@app.route("/list_calendar_events")
def list_calendar_events():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    # 获取日历事件列表
    events_response = requests.get(
        "https://graph.microsoft.com/v1.0/me/calendar/events",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    )

    if events_response.status_code != 200:
        return json.dumps({"error": "Failed to fetch events. Status code: {}".format(events_response.status_code)})

    events_data = events_response.json()

    # 初始化事件列表
    event_list = []

    # 遍历日历事件，提取必要信息
    for event in events_data["value"]:
        event_info = {
            "subject": event.get("subject"),
            "start_time": event.get("start", {}).get("dateTime"),
            "end_time": event.get("end", {}).get("dateTime"),
        }
        event_list.append(event_info)

    # 返回事件列表的 JSON 格式
    return jsonify(event_list)

from flask import redirect, url_for, jsonify

@app.route("/create_meeting", methods=["GET", "POST"])
def create_meeting():
    if request.method == "GET":
        return render_template("create_meeting.html")
    elif request.method == "POST":
        # 获取表单数据
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        subject = request.form.get("subject")

        if not (start_time and end_time and subject):
            return jsonify({"error": "All fields are required."}), 400  # 返回错误消息和状态码
        
        token = auth.get_token_for_user(app_config.SCOPE)
        if "error" in token:
            return redirect(url_for("login"))

        # 获取当前用户的邮箱
        user_email = auth.get_user().get("email")
        
        # 在此处添加创建会议的代码

        # 返回成功消息
        return jsonify({"success": "Meeting created successfully."}), 200  # 返回成功消息和状态码


@app.route("/list_todo_tasks", methods=["GET"])
def list_todo_tasks():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return jsonify({"error": "Failed to obtain access token."}), 500

    endpoint = "https://graph.microsoft.com/v1.0/me/todo/lists"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json"
    }

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            todo_lists = response.json().get("value", [])
            tasks = []

            for todo_list in todo_lists:
                list_id = todo_list["id"]
                list_name = todo_list["displayName"]
                tasks_endpoint = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
                tasks_response = requests.get(tasks_endpoint, headers=headers)
                if tasks_response.status_code == 200:
                    tasks.extend(tasks_response.json().get("value", []))

            return jsonify(tasks)
        else:
            return jsonify({"error": "Failed to fetch tasks from Microsoft To-Do."}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
