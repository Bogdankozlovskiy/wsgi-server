from jinja2 import Template
from short_cuts import parse_body, parse_cookies
from datetime import datetime


COUNT = 1
db = {}
chat_message = []


def chat(request_method, http_cookie, body):
    body = parse_body(body)
    cookies = parse_cookies(http_cookie)
    user_id = int(cookies.get("user_id"))
    user_name = db.get(user_id)
    if user_name is None:
        return "307 Temporary Redirect", [("Location", f"http://localhost:8000/register"), ("Set-Cookie", "location=chat")], b""
    with open("templates/chat") as file:
        template = Template(file.read())
    if request_method == "POST" and (msg := body.get("msg")):
        chat_message.append(
            (user_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
        )
    return "200 OK", [], template.render(chat=chat_message).encode()


def view_register(request_method, http_cookie, body):
    if request_method == "GET":
        with open("./templates/register") as file:
            template = Template(file.read())
        return "200 OK", [], template.render().encode()
    body = parse_body(body)
    global COUNT
    db[COUNT] = body['name']
    cookie = parse_cookies(http_cookie)
    if location := cookie.get("location"):
        response = "307 Temporary Redirect", [("Location", f"http://localhost:8000/{location}")], b""
    else:
        response = "200 OK", [("Set-Cookie", f"user_id={COUNT}")], b"register was success"
    COUNT += 1
    return response

