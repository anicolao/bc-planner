# Caller supplies nixpkgs pinned to the revision recorded in the catalog JSON.
{ pkgs }:
let catalog = import ../bc23-public-source-catalog.nix { inherit (pkgs) fetchzip; };
in builtins.mapAttrs (_: entry: entry.src) catalog
