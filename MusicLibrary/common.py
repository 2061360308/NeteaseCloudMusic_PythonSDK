import json


def to_bytes(s):
    if isinstance(s, str):
        return s.encode("utf-8")
    elif isinstance(s, bytes):
        return s
    elif s is None:
        return b""
    else:
        raise TypeError(f"Unsupported type: {type(s)}")


class Response:
    def __init__(self, response_str: str):
        data = json.loads(response_str)

        headers = data.get("headers")
        body = data.get("body")
        status = data.get("status")

        self.headers = headers or {}
        self.body = body or {}
        self.status = status or 500

    @property
    def data(self):
        return self.body

    @property
    def cookies(self):
        return self.headers.get("Set-Cookie", "")

    def __repr__(self):
        return f"Response(\n status: {self.status} \n headers:\n{json.dumps(self.headers, indent=2, ensure_ascii=False)},\n body:\n{json.dumps(self.body, indent=2, ensure_ascii=False)}\n)"
