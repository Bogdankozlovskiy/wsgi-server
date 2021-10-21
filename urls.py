import re
from views import view_register, chat


urlpatterns = [
    ("^/register$", view_register),
    ("^/chat$", chat),
]


def get_view(raw_uri, request_method, http_cookie, body):
    for regex_pattern, view_fun in urlpatterns:
        if pattern := re.match(regex_pattern, raw_uri):
            return view_fun(request_method, http_cookie, body, **pattern.groupdict())
    return "404 not found", [], b""
