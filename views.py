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
        try:
            connection.execute("""
                INSERT INTO chat (message, user_id)
                VALUES (?, ?)
            """, (msg, user_id))
            connection.commit()
        except:
            pass
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM chat_data
        LIMIT 10
    """)
    # cursor.execute("""
    #         SELECT user.login, chat.publish_date, chat.message, chat.id, count(chat_to_user_like.chat_id) as likes
    #         FROM chat
    #         JOIN user
    #         ON user.id=chat.user_id
    #         LEFT JOIN chat_to_user_like
    #         ON chat.id=chat_to_user_like.chat_id
    #         GROUP BY user.login, chat.publish_date, chat.message, chat.id
    #         ORDER BY chat.publish_date desc
    #         LIMIT 10
    #     """)
    return "200 OK", [], template.render(chat=cursor.fetchall()).encode()


def view_register(request_method, http_cookie, body, http_host, url_scheme, query_string):
    if request_method == "GET":
        with open("./templates/register") as file:
            template = Template(file.read())
        return "200 OK", [], template.render().encode()
    body = parse_body(body)
    try:
        cursor = connection.execute("INSERT INTO user (login) values (?)", (body['name'], ))
        connection.commit()
    except Exception:
        return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/register")], b""
    user_id = cursor.lastrowid
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


def add_likes(request_method, http_cookie, body, http_host, url_scheme, query_string, message_id=None):
    cookie = parse_cookies(http_cookie)
    user_id = int(cookie.get("user_id", "0"))
    try:
        connection.execute("""
            INSERT INTO chat_to_user_like
            (user_id, chat_id)
            VALUES (?, ?)
        """, (user_id, message_id))
    except:
        connection.execute("""
            DELETE FROM chat_to_user_like
            WHERE user_id=? AND chat_id=?
        """, (user_id, message_id))
    connection.commit()
    return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/chat")], b""

def add_rate(request_method, http_cookie, body, http_host, url_scheme, query_string, message_id=None, rate=None):
    cookie = parse_cookies(http_cookie)
    user_id = int(cookie.get("user_id", "0"))
    try:
        connection.execute("""
            INSERT INTO chat_to_user_like
            (user_id, chat_id, rate)
            VALUES (?, ?, ?)
        """, (user_id, message_id, rate))
    except:
        connection.execute("""
            UPDATE chat_to_user_like
            SET rate=?
            WHERE user_id=? AND chat_id=?
        """, (rate, user_id, message_id))
    connection.commit()
    return "307 Temporary Redirect", [("Location", f"{url_scheme}://{http_host}/chat")], b""
