import json


def decode_json(s):
    if s == '':
        return None
    return json.loads(s)


def decode_lines(s, linefunc):
    if s == '':
        return []

    lines = s.strip().split('\n')
    result = []
    for line in lines:
        result.append(linefunc(line))

    return result
