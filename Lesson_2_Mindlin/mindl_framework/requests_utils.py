from quopri import decodestring


def _parse_params(query_str: str) -> dict:
    result = {}
    for param in query_str.split('&'):
        key, value = param.split('=')
        result[key] = value

    return result


def _get_wsgi_input_data(environ: dict) -> bytes:
    content_length = environ.get('CONTENT_LENGTH')
    content_length = int(content_length) if content_length else 0
    data = environ['wsgi.input'].read(content_length) if content_length else b''

    return data


def _parse_wsgi_input_data(data: bytes) -> dict:
    if not data:
        return {}

    data_str = data.decode('utf-8')
    result = _parse_params(data_str)

    return result


def _decode_data(data: dict) -> dict:
    result = {}
    for key, val in data.items():
        new_val = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        new_key = bytes(key.replace('%', '=').replace('+', ' '), 'UTF-8')
        new_val_str = decodestring(new_val).decode('UTF-8')
        new_key_str = decodestring(new_key).decode('UTF-8')
        result[new_key_str] = new_val_str

    return result


def get_get_params(environ: dict) -> dict:
    query_str = environ['QUERY_STRING']
    result = _parse_params(query_str) if query_str else {}

    return _decode_data(result)


def get_post_params(environ: dict) -> dict:
    data = _get_wsgi_input_data(environ)
    result = _parse_wsgi_input_data(data)

    return _decode_data(result)


