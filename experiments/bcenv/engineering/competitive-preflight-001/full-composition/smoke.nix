{ flakeUri ? "github:anicolao/bcenv/be041d3d18ecd9fa474cbfb076c86c336d5b6ff3" }:
let
  flake = builtins.getFlake flakeUri;
  pkgs = import flake.inputs.nixpkgs { system = "x86_64-linux"; };
in pkgs.runCommand "bcenv-full-offline-composition-smoke-portable" {
  nativeBuildInputs = [ pkgs.python3 ];
} ''
  mkdir -p "$out"
  python ${./smoke.py} ${./snapshot} ${./source-manifest.json} "$out/results.json" > "$out/test.log" 2>&1 || { cat "$out/test.log"; exit 1; }
  cat "$out/test.log"
''
