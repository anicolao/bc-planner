"""Trusted fixed-package collector; executed only in read-only export namespace.

Private stdout is a bounded deterministic ZIP consumed by the trusted backend.
It is never a candidate process output or a model-visible packaging assertion.
"""
import io
import os
import re
import stat
import sys
import zipfile

PACKAGE = 'fixturebot'
MAX_ARCHIVE = 1048576
MAX_FILES = 128
MAX_FILE = 524288
MAX_SOURCE = 2097152
MAX_ENTRIES = 256
MAX_DEPTH = 16
MAX_PATH = 240
WORD = re.compile(r'[A-Za-z_][A-Za-z0-9_]*\Z')


class Rejected(Exception):
    pass


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def collect():
    mounts = {parts[4]: set(parts[5].split(',')) for line in open('/proc/self/mountinfo')
              if (parts := line.split())[4] in ('/', '/workspace/src', '/workspace/scratch')}
    if len(mounts) != 3 or any('ro' not in flags for flags in mounts.values()):
        raise Rejected()
    files, source_size, zip_size, visited = [], 0, 22, 0

    def walk(directory, components):
        nonlocal source_size, zip_size, visited
        if len(components) > MAX_DEPTH:
            raise Rejected()
        names = []
        with os.scandir(directory) as entries:
            for entry in entries:
                visited += 1
                if visited > MAX_ENTRIES or not entry.name.isascii():
                    raise Rejected()
                names.append(entry.name)
        for name in sorted(names):
            path = '/'.join(components + (name,))
            if len(path) > MAX_PATH:
                raise Rejected()
            info = os.stat(name, dir_fd=directory, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                if not WORD.fullmatch(name) or (not components and name != PACKAGE):
                    raise Rejected()
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                                dir_fd=directory)
                try:
                    if fingerprint(os.fstat(child)) != fingerprint(info):
                        raise Rejected()
                    walk(child, components + (name,))
                finally:
                    os.close(child)
                continue
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or
                    not path.startswith(PACKAGE + '/') or not name.endswith('.java') or
                    not WORD.fullmatch(name[:-5]) or not 0 < info.st_size <= MAX_FILE or
                    len(files) >= MAX_FILES):
                raise Rejected()
            source_size += info.st_size
            zip_size += 76 + 2 * len(path) + info.st_size  # exact ZIP_STORED metadata/data cost
            if source_size > MAX_SOURCE or zip_size > MAX_ARCHIVE:
                raise Rejected()
            descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                                 dir_fd=directory)
            try:
                if fingerprint(os.fstat(descriptor)) != fingerprint(info):
                    raise Rejected()
                chunks, remaining = [], info.st_size
                while remaining:
                    chunk = os.read(descriptor, min(8192, remaining))
                    if not chunk:
                        raise Rejected()
                    chunks.append(chunk)
                    remaining -= len(chunk)
                if os.read(descriptor, 1) or fingerprint(os.fstat(descriptor)) != fingerprint(info):
                    raise Rejected()
                content = b''.join(chunks)
                content.decode('utf-8')
                if b'\x00' in content:
                    raise Rejected()
                files.append((path, content))
            finally:
                os.close(descriptor)

    root = os.open('/workspace/src', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        walk(root, ())
    finally:
        os.close(root)
    if not files:
        raise Rejected()
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
        for path, content in sorted(files):
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o444) << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_STORED)
    data = output.getvalue()
    if len(data) != zip_size or len(data) > MAX_ARCHIVE:
        raise Rejected()
    return data


if __name__ == '__main__':
    try:
        result = collect()
    except Exception:
        sys.stderr.buffer.write(b'source_export_rejected\n')
        raise SystemExit(2)
    sys.stdout.buffer.write(result)
