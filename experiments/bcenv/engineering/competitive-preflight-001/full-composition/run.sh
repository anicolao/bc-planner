#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
runner=/workspace/scratch/1523a3f802eb/nix-canonical-root/nix-root
flake_uri="git+file:///workspace/shared/bcenv-responses-transport?rev=be041d3d18ecd9fa474cbfb076c86c336d5b6ff3"
"$runner" build --impure --file ./smoke.nix --argstr flakeUri "$flake_uri" --option sandbox-paths '' --out-link ./result -L 2>&1 | tee nix-build.log
store_path=$(readlink ./result)
case "$store_path" in /nix/store/*) ;; *) echo "unexpected Nix output path" >&2; exit 1 ;; esac
# This configured runner uses an alternate physical store root.
materialized="/workspace/scratch/1523a3f802eb/nix-canonical-root/root$store_path"
cp --remove-destination "$materialized/test.log" test.log
cp --remove-destination "$materialized/results.json" results.json

cat test.log
