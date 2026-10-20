let
  route = builtins.getFlake "git+file:///workspace/shared/bcenv-durable-replay-route";
  producer = builtins.getFlake "git+file:///workspace/shared/bcenv-replay-page-v2?rev=f3963b7f16857bf6aad837196b8262441ff7c1e3";
  pkgs = import route.inputs.nixpkgs { system = "x86_64-linux"; };
in pkgs.runCommand "bcenv-independent-durable-replay-review" {
  nativeBuildInputs = [ pkgs.python3 ];
} ''
  cp -r ${producer.outPath} source
  chmod -R u+w source
  for file in ledger.py controller.py responses_transport.py replay_store.py replay_route.py replay_protocol.py; do
    cp ${route.outPath}/services/$file source/services/$file
  done
  python ${/workspace/shared/review_durable_replay.py} "$PWD/source" ${/workspace/shared/review_replay_v1_registry_baseline.json}
  touch "$out"
''
