{ flakeUri ? "github:anicolao/bcenv/59242ba9935d777f787596adfc0b2b1efc34650d" }:
let
  source = builtins.getFlake flakeUri;
  pkgs = import source.inputs.nixpkgs { system = "x86_64-linux"; };
in pkgs.runCommand "bcenv-published-replay-route-independent-review" {
  nativeBuildInputs = [ pkgs.python3 ];
} ''
  mkdir -p "$out"
  python ${./review_durable_replay.py} ${source.outPath} ${./review_replay_v1_registry_baseline.json} > "$out/test.log" 2>&1
  cat "$out/test.log"
''
