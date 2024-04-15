{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  outputs = {nixpkgs, flake-utils, ...}:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs;[
          podman-compose
          (python3.withPackages (ps: with ps; [
            build
            pytest
            flake8
            requests
            lxml
            urllib3
          ]))
        ];
      };
    });
}
