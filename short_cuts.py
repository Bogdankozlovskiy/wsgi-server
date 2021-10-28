def parse_body(body):
    data = {}
    if body is None:
        return data
    for input_ in body.decode().split("&"):
        key, value = input_.split("=")
        data[key] = value
    return data


def parse_cookies(http_cookie):
    data = {}
    if http_cookie is None:
        return data
    for input_ in http_cookie.split("; "):
        key, *value = input_.split("=")
        value = "=".join(value)
        data[key] = value
    return data


def parse_query_string(query_string):
    result = {}
    if not query_string:
        return result
    for pair in query_string.split("&"):
        key, value = pair.split("=")
        result[key] = value
    return result
