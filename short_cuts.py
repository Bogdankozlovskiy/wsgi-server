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
