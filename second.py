import socket

Code = 'utf-8'
Host = ''
Port = 8080

CodeText = {
    100: 'Continue',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Parmanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Payload Too Large',
    414: 'URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Range Not Satisfiable',
    417: 'Exceptation Failed',
    418: "I'm a teapot",
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
}


def gen_response(header: str, body: str):
    return f"""{header}\n\n{body}""".encode(Code)


def gen_header(code: int):
    return f"HTTP/1.1 {code} {CodeText[code]}"


def split_one(string: str, word: str):
    result = string.split(word, maxsplit=1)
    return result[0], '' if len(result) == 1 else result[1]


def parse(raw: str):
    header, body = split_one(raw, '\n\n')
    header_lines = header.splitlines(keepends=False)
    method, path, version = header_lines[0].split(' ')
    headers = []
    for line in header_lines[1:]:
        key, value = split_one(line, ':')
        if value != '':
            headers.append((key, value))
    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers,
        'body': body
    }


def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((Host, Port))
    listen_socket.listen(1)

    print(f'Serving HTTP on port {Port} ...')

    while True:
        client_connection, client_address = listen_socket.accept()
        request_data = client_connection.recv(1024)
        request = parse(request_data.decode(Code))
        print(request)
        if request['method'] == 'GET':
            header = gen_header(200)
            http_response = gen_response(header, f"Hello, {request['path']}")
            client_connection.sendall(http_response)
            client_connection.close()
        else:
            header = gen_header(404)
            http_response = gen_response(header, 'Not Found')
            client_connection.sendall(http_response)
            client_connection.close()


if __name__ == '__main__':
    main()
