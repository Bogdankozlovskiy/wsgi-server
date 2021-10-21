from urls import get_view


def application(env, start_response):
    http_cookie = env['HTTP_COOKIE']
    raw_uri = env['PATH_INFO']
    request_method = env['REQUEST_METHOD']
    body = None
    if request_method == "POST":
        content_length = int(env['CONTENT_LENGTH'])
        body = env['wsgi.input'].read(content_length)
    response_from_get_view = get_view(raw_uri, request_method, http_cookie, body)
    status_code, headers, view = response_from_get_view
    start_response(status_code, [('Content-Type', 'text/html')] + headers)
    return [view]
