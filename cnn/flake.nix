{
  description = "Python development environment with pinned nixpkgs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
        pythonEnv = pkgs.python3.withPackages (python-pkgs:
          with python-pkgs; [
            pandas
            pillow
            torch
            torchvision
            scikit-learn
            tqdm
            matplotlib
            numpy
          ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [pythonEnv];
        };
      }
    );
}
