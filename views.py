from jinja2 import Template
from short_cuts import parse_body, parse_cookies, parse_query_string
from models import connection


def main(request_method, http_cookie, body, http_host, url_scheme, query_string):
    with open("./templates/main") as file:
        template = Template(file.read())
    return "200 OK", [], template.render().encode()


def chat(request_method, http_cookie, body, http_host, url_scheme, query_string):
    body = parse_body(body)
    cookies = parse_cookies(http_cookie)
    user_id = int(cookies.get("user_id", "0"))
    cursor = connection.cursor()
    cursor.execute("SELECT login FROM user WHERE id=?", (user_id, ))
    user_name = cursor.fetchone()
    if user_name:
        user_name, = user_name
    if user_name is None:
        return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/register"), ("Set-Cookie", "location=chat")], b""
    with open("templates/chat") as file:
        template = Template(file.read())
    if request_method == "POST" and (msg := body.get("msg")):
        connection.execute("""
            INSERT INTO chat (message, user_id)
            VALUES (?, ?)
        """, (msg, user_id))
        connection.commit()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM chat_data
        LIMIT 10
    """)
    return "200 OK", [], template.render(chat=cursor.fetchall()).encode()


def view_register(request_method, http_cookie, body, http_host, url_scheme, query_string):
    if request_method == "GET":
        with open("./templates/register") as file:
            template = Template(file.read())
        return "200 OK", [], template.render().encode()
    body = parse_body(body)
    try:
        res = connection.execute("INSERT INTO user (login) values (?)", (body['name'], ))
        connection.commit()
    except Exception:
        return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/register")], b""
    user_id = res.lastrowid
    cookie = parse_cookies(http_cookie)
    if location := cookie.get("location"):
        response = "307 Temporary Redirect", [("Set-Cookie", f"user_id={user_id}"), ("Location", f"{url_scheme}://{http_host}/{location}")], b""
    else:
        response = "200 OK", [("Set-Cookie", f"user_id={user_id}")], b"register was success"
    return response


def remove_message(request_method, http_cookie, body, http_host, url_scheme, query_string, message_id=None):
    query_string = parse_query_string(query_string)
    if message_id is None:
        message_id = query_string.get("message_id")
    cookie = parse_cookies(http_cookie)
    user_id = int(cookie.get("user_id", "0"))
    connection.execute("DELETE FROM chat WHERE user_id=? AND id=?", (user_id, message_id))
    connection.commit()
    return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/chat")], b""
