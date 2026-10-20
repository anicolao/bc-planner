"""Read/write probe helper, executed exclusively after the fixed chroot."""
import base64
import json
import os
import sys


def open_parent(path):
    parts = path.split('/')
    if len(parts) < 2 or parts[0] not in ('src', 'scratch', 'docs', 'artifacts', 'self_play'):
        raise ValueError('invalid_path')
    if any(not p or p in ('.', '..') or '/' in p or '\\' in p for p in parts):
        raise ValueError('invalid_path')
    descriptor = os.open('/workspace', os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor, parts[-1]
    except BaseException:
        os.close(descriptor)
        raise


def main():
    request = json.loads(sys.stdin.buffer.read(1048577))
    parent, leaf = open_parent(request['path'])
    try:
        if request['operation'] == 'read':
            fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)
            with os.fdopen(fd, 'rb') as file:
                file.seek(request['offset'])
                data = file.read(request['limit'])
            print(json.dumps({'status': 'ok', 'bytes': base64.b64encode(data).decode()}))
        elif request['operation'] == 'write' and request['path'].split('/')[0] in ('src', 'scratch'):
            data = base64.b64decode(request['content'], validate=True)
            fd = os.open(leaf, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW | os.O_CLOEXEC,
                         0o600, dir_fd=parent)
            with os.fdopen(fd, 'wb') as file:
                file.write(data)
            print(json.dumps({'status': 'ok'}))
        else:
            raise ValueError('invalid_operation')
    finally:
        os.close(parent)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('{"status":"failed"}')
        raise SystemExit(1)
