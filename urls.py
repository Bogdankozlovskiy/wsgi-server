import re
from views import view_register, chat, remove_message, main, add_likes, add_rate


urlpatterns = [
    (r"^/$", main),
    (r"^/register$", view_register),
    (r"^/chat$", chat),
    (r"^/delete_message/(?P<message_id>\d+)$", remove_message),
    (r"^/add_like/(?P<message_id>\d+)$", add_likes),
    (r"^/delete_message$", remove_message),
    (r"^/add_rate/(?P<message_id>\d+)/(?P<rate>\d+)$", add_rate),
]


def get_view(raw_uri, request_method, http_cookie, http_host, url_scheme, query_string, body):
    for regex_pattern, view_fun in urlpatterns:
        if pattern := re.match(regex_pattern, raw_uri):
            return view_fun(request_method, http_cookie, body, http_host, url_scheme, query_string, **pattern.groupdict())
    return "404 not found", [], b""
