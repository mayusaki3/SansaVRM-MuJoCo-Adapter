# SansaVRM-MuJoCo-Adapter

SansaVRM-MuJoCo-Adapter is an adapter project for connecting SansaVRM with MuJoCo, MJCF, and related controller configuration artifacts.

This repository keeps MuJoCo-specific conversion, approximation, simulation-support, and validation concerns outside the SansaVRM core repository.

## Status

This repository is in the early design and local-environment setup phase.

Current focus:

- Defining the boundary between SansaVRM core and this adapter
- Preparing a local MuJoCo development environment
- Verifying minimal MJCF loading and stepping
- Organizing documentation for future multilingual support

## Documentation

Project documentation is maintained under `docs/<language-code>/`.

| Language | Index |
| --- | --- |
| Japanese | [docs/ja-JP/目次.md](docs/ja-JP/目次.md) |

## Quick Start

For local MuJoCo setup and verification, see the Japanese documentation index.

- [docs/ja-JP/目次.md](docs/ja-JP/目次.md)

## Repository Role

SansaVRM core is expected to manage common model information, adapter-facing APIs, and custom parameter schemas.

This repository is expected to manage MuJoCo-specific behavior, including:

- MJCF generation
- MuJoCo actuator mapping
- controller configuration generation
- MuJoCo-specific diagnostics and conversion reports
- local MuJoCo validation examples

Detailed specifications are maintained in the documentation tree rather than in this README.

## License

This repository is licensed under the MIT License.
