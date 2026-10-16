{
  description = "Pinned tools for the bc-planner cloud runtime";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    packages.${system} = { tailscale = pkgs.tailscale; default = pkgs.tailscale; };
  };
}
