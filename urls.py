import re
from views import view_register, chat, remove_message, main, add_like


urlpatterns = [
    (r"^/$", main),
    (r"^/register$", view_register),
    (r"^/chat$", chat),
    (r"^/delete_message/(?P<message_id>\d+)$", remove_message),
    (r"^/add_like/(?P<message_id>\d+)$", add_like),
    (r"^/delete_message$", remove_message),
]


def get_view(raw_uri, request_method, http_cookie, http_host, url_scheme, query_string, body):
    for regex_pattern, view_fun in urlpatterns:
        if pattern := re.match(regex_pattern, raw_uri):
            return view_fun(request_method, http_cookie, body, http_host, url_scheme, query_string, **pattern.groupdict())
    return "404 not found", [], b""
