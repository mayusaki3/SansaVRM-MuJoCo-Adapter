# SansaVRM-MuJoCo-Adapter

SansaVRM-MuJoCo-Adapter は、SansaVRM 形式と MuJoCo / MJCF / controller configuration を接続するための Adapter です。

本リポジトリは、SansaVRM 本体に MuJoCo 実行環境への直接依存を持ち込まず、MuJoCo 固有の変換・近似・実行補助を分離することを目的とします。

## Status

This repository is in the early design phase.

Current scope:

- SansaVRM から MJCF への変換方針の検討
- SansaVRM の物理・ジョイント・アクチュエータ情報の MuJoCo 連携検証
- MJCF に直接出力できる情報と controller_config 等へ分離する情報の分類
- MuJoCo 固有パラメータの扱いの検討
- SansaVRM 本体 API との責務境界の整理

## Purpose

SansaVRM は、VRM 0.x / VRM 1.0 / URDF などのファイル変換対象に加え、MuJoCo との連携を想定します。

MuJoCo は単なるファイル形式変換だけではなく、以下を含むため、SansaVRM 本体とは分離した Adapter として扱います。

- MJCF 生成
- アクチュエータ写像
- 物理パラメータ変換
- controller_config 生成
- MuJoCo 固有パラメータの解釈
- シミュレーション実行補助
- 変換レポート生成
- MuJoCo バージョン差分への追従

## Relationship with SansaVRM

SansaVRM 本体と本 Adapter の責務境界は以下の通りです。

### SansaVRM Core

SansaVRM 本体は以下を担当します。

- SansaVRM 共通仕様の管理
- Module / Connection / Slot / Property の共通表現
- 物理モデル情報の保持
- ジョイント情報の保持
- コライダー情報の保持
- アクチュエータ情報の保持
- センサ情報の保持
- Adapter が参照する入出力 API の提供
- namespace 付き custom parameter の保持
- custom parameter schema の管理
- MJCF 入出力可否の判定に必要な schema 情報の保持

### SansaVRM-MuJoCo-Adapter

本 Adapter は以下を担当します。

- SansaVRM API からの情報取得
- SansaVRM から MJCF への変換
- 必要に応じた MJCF から SansaVRM への変換
- MuJoCo actuator への写像
- controller_config の生成
- MuJoCo 固有パラメータの解釈
- MuJoCo 固有の近似変換
- diagnostics / conversion report の生成
- MuJoCo 実行環境に依存する検証

## Design Principle

本 Adapter は、SansaVRM 本体の内部データ構造へ直接依存しません。

Adapter は、SansaVRM 本体が提供する安定した公開 API を経由して、以下の情報を取得します。

- model metadata
- modules
- connections
- slots
- properties
- physics parameters
- joints
- colliders
- actuators
- sensors
- custom parameters
- custom parameter schemas

## MuJoCo Integration Scope

本 Adapter が扱う主な MuJoCo / MJCF 要素は以下です。

- body
- joint
- geom
- actuator
- sensor
- site
- equality constraint
- tendon
- material
- mesh
- option
- default

初期段階では、以下を優先します。

1. body / joint / geom の最小変換
2. position actuator の出力
3. motor actuator の出力
4. actuator parameter mapping
5. controller_config 生成
6. diagnostics / conversion report 生成

## Custom Parameter Handling

MuJoCo 固有パラメータは、SansaVRM 側の custom parameter schema に基づいて扱います。

custom parameter schema では、各パラメータが以下のどれに該当するかを識別します。

- MJCF に直接入出力できる
- Adapter 側補助成果物へ分離する
- MJCF と Adapter 側補助成果物の両方へ出力する
- SansaVRM 内に保持するのみ
- 現在は未対応
- source_raw として保持する

想定する `io_scope` は以下です。

| io_scope | Meaning |
| --- | --- |
| `mjcf` | MJCF に直接入出力できる |
| `adapter_artifact` | controller_config 等の Adapter 側補助成果物へ出力する |
| `both` | MJCF と Adapter 側補助成果物の両方へ出力する |
| `preserve_only` | SansaVRM 内に保持するが出力しない |
| `unsupported` | 登録済みだが現在は未対応 |
| `source_raw` | 解釈せず元情報として保持する |

## Expected Outputs

本 Adapter は、将来的に以下のような成果物を生成する想定です。

```text
output/
├─ model.xml
├─ controller_config.json
├─ conversion_report.json
└─ diagnostics.json
```

### model.xml

MuJoCo / MJCF モデルです。

主に以下を含みます。

- body
- joint
- geom
- actuator
- sensor
- material
- mesh

### controller_config.json

MJCF に直接出力しない制御・実行補助情報です。

例：

- command delay
- deadband
- external PID configuration
- thermal model settings
- current limit
- voltage limit
- runtime control mode
- actuator update rate

### conversion_report.json

変換結果の概要です。

例：

- converted elements
- skipped elements
- fallback results
- non-reversible conversions
- warnings
- unsupported parameters

### diagnostics.json

検証・警告・エラー情報です。

例：

- missing required parameter
- unsupported MuJoCo parameter
- unsupported target MuJoCo version
- invalid custom parameter schema
- invalid joint tree structure

## Planned Repository Structure

```text
SansaVRM-MuJoCo-Adapter/
├─ README.md
├─ LICENSE
├─ docs/
│  └─ ja-JP/
│     ├─ 01_目的と前提.md
│     ├─ 02_責務境界.md
│     ├─ 03_MJCF変換方針.md
│     ├─ 04_アクチュエータ写像.md
│     ├─ 05_custom_parameter_mapping.md
│     └─ 06_検証方針.md
├─ schemas/
│  ├─ controller_config.schema.json
│  ├─ conversion_report.schema.json
│  └─ diagnostics.schema.json
├─ examples/
│  ├─ minimal_body/
│  ├─ position_servo/
│  └─ torque_motor/
├─ src/
│  └─ sansavrm_mujoco_adapter/
│     ├─ __init__.py
│     ├─ converter.py
│     ├─ mjcf_writer.py
│     ├─ controller_config_writer.py
│     └─ diagnostics.py
└─ tests/
   ├─ test_minimal_body.py
   ├─ test_position_servo.py
   └─ test_custom_parameter_mapping.py
```

## Development Phases

### Phase 1: Documentation and Boundary Definition

- SansaVRM 本体との責務境界を定義する
- MJCF に出力する情報と Adapter 側補助成果物へ分離する情報を整理する
- custom parameter schema の扱いを整理する

### Phase 2: Minimal MJCF Export

- Module から body を生成する
- Connection から joint を生成する
- Property から geom を生成する
- 最小 MJCF を出力する

### Phase 3: Actuator Mapping

- position actuator を出力する
- motor actuator を出力する
- actuator range / torque limit / gear / kp / kv を扱う
- controller_config への分離を検証する

### Phase 4: Diagnostics and Validation

- 変換レポートを生成する
- diagnostics を生成する
- 未対応パラメータを検出する
- fallback の適用結果を記録する

### Phase 5: Import and Round-trip Support

- MJCF から SansaVRM への読み戻しを検討する
- 非可逆情報を diagnostics に記録する
- source_raw の保持方針を検証する

## Non-goals

本リポジトリの初期段階では、以下は対象外です。

- SansaVRM 本体仕様の定義
- SansaVRM validator 本体の実装
- MuJoCo runtime 全体の実装
- 強化学習環境の実装
- リアルタイムネットワーク同期
- UI / editor 実装
- VRM / URDF の標準変換実装

## Related Projects

- SansaVRM
- SansaVRM-MuJoCo-Adapter
- MuJoCo
- MJCF
- VRM
- URDF

## License

This repository is licensed under the MIT License.
