"""Trusted materialization of the exact public-runtime synthetic fixture.

No downloads, installation, mount operations, credentials or model input.
The source root must already contain the pinned Nix closure in the manifest.
"""
import argparse
import json
from pathlib import Path
import re
import shutil

BASE = Path('/workspace/shared/bc23-sandbox-probe')
DEFAULT_SOURCE_ROOT = Path('/workspace/scratch/1523a3f802eb/nix-canonical-root/root')
STORE_NAME = re.compile(r'/nix/store/[0-9a-z]{32}-[A-Za-z0-9+._?=-]+\Z')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true', help='read-only prerequisite verification')
    group.add_argument('--materialize', action='store_true', help='create only an absent fresh fixture')
    parser.add_argument('--source-root', type=Path, default=DEFAULT_SOURCE_ROOT,
                        help='trusted existing root containing the exact pinned public Nix store paths')
    args = parser.parse_args()
    manifest = json.loads((BASE / 'fixture-manifest.json').read_text())
    paths = manifest['closure']
    if type(paths) is not list or len(paths) != 22 or len(set(paths)) != len(paths):
        raise ValueError('invalid_pinned_closure')
    if any(type(path) is not str or not STORE_NAME.fullmatch(path) for path in paths):
        raise ValueError('invalid_pinned_store_path')
    source = args.source_root.resolve(strict=True)
    for path in paths:
        if not (source / path.lstrip('/')).is_dir():
            raise ValueError('pinned_closure_path_missing')
    if not (source / manifest['python'].lstrip('/')).is_file():
        raise ValueError('pinned_python_missing')
    helper = BASE / 'io_worker.py'
    if not helper.is_file():
        raise ValueError('trusted_io_helper_missing')
    if args.check:
        print(json.dumps({'status': 'prerequisites_present', 'closure_paths': len(paths),
                          'materialized': False, 'network_used': False}))
        return
    root, writable, outside = BASE / 'fixture-root', BASE / 'writable', BASE / 'host-canary.txt'
    # Refuse replacement, recovery deletion or merging into any existing state.
    if any(path.exists() or path.is_symlink() for path in (root, writable, outside)):
        raise ValueError('fresh_fixture_required_no_existing_target')
    root.mkdir()
    for path in paths:
        shutil.copytree(source / path.lstrip('/'), root / path.lstrip('/'), symlinks=True)
    for path in ('workspace/src', 'workspace/scratch', 'workspace/docs', 'workspace/artifacts',
                 'workspace/self_play', 'proc', 'dev', 'tmp', 'opt', 'etc'):
        (root / path).mkdir(parents=True, exist_ok=True)
    for name in ('src', 'scratch'):
        (writable / name).mkdir(parents=True)
    shutil.copy2(helper, root / 'opt/io_worker.py')
    (root / 'workspace/docs/canary.txt').write_text('synthetic-read-only-reference\n')
    outside.write_text('SYNTHETIC-OUTSIDE-ROOT-CANARY\n')
    print(json.dumps({'status': 'synthetic_fixture_materialized', 'closure_paths': len(paths),
                      'network_used': False, 'security_settings_changed': False,
                      'runtime_acceptance': 'not_granted'}))


if __name__ == '__main__':
    main()
