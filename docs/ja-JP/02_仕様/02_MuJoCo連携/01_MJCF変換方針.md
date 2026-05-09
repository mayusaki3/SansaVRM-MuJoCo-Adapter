<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000012Z-SVMJ
lang: ja-JP
canonical_title: MJCF変換方針
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > MJCF変換方針

# MJCF変換方針

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter における SansaVRM から MJCF への変換方針を定義する。

MJCF 変換方針は、SansaVRM 本体 API から取得した情報を、MuJoCo が読み込める MJCF XML として出力するための基本方針、対象要素、非可逆情報の扱い、Adapter 側補助成果物との分離方針を明確にするために定義する。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、SansaVRM 本体 API から取得した情報をもとに MJCF を生成する。

Adapter は、SansaVRM 本体の内部データ構造へ直接依存してはならない。

MJCF に直接出力できる情報は、SansaVRM 側の custom parameter schema に定義された `io_scope` および `mjcf_mapping` に基づいて判定する。

MJCF に直接出力できない情報は、`adapter_artifact` に基づいて controller_config などの Adapter 側補助成果物へ分離する。

## 3. 入力情報

MJCF 生成時の入力情報は、SansaVRM 本体 API から取得する。

初期対象は以下とする。

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

## 4. 出力情報

MJCF 変換処理は、以下を出力する。

- MJCF XML ファイル
- conversion_report
- diagnostics

MJCF に含めない制御・実行補助情報が存在する場合は、以下の補助成果物へ分離する。

- controller_config
- runtime_config
- external_metadata

初期段階では、補助成果物として controller_config を優先する。

## 5. MJCF出力対象要素

初期段階で MJCF へ出力する対象要素は以下とする。

- mujoco
- compiler
- option
- worldbody
- body
- joint
- geom
- actuator
- sensor
- site
- material
- mesh
- default

以下は将来拡張対象とする。

- tendon
- equality
- contact
- pair
- exclude
- keyframe
- plugin

## 6. body変換方針

SansaVRM の構造要素は、MuJoCo の `body` へ変換する。

body 変換では、以下を扱う。

- body name
- parent-child relationship
- position
- rotation
- mass properties
- inertial information

SansaVRM 側に MuJoCo body へ直接対応しない情報がある場合、diagnostics に記録する。

## 7. joint変換方針

SansaVRM の joint 情報は、MuJoCo の `joint` へ変換する。

初期段階では、以下の joint type を対象とする。

- hinge
- slide
- ball
- free

joint 変換では、以下を扱う。

- joint name
- joint type
- axis
- range
- damping
- frictionloss
- armature

`armature` などの MuJoCo 固有パラメータは、custom parameter schema の `mjcf_mapping` に基づいて出力する。

## 8. geom変換方針

SansaVRM の collider / geometry 情報は、MuJoCo の `geom` へ変換する。

初期段階では、以下の geom type を対象とする。

- box
- sphere
- capsule
- cylinder
- plane
- mesh

geom 変換では、以下を扱う。

- geom name
- geom type
- size
- position
- rotation
- mass
- density
- friction
- material

SansaVRM 側の collision 表現が MuJoCo の geom へ直接対応しない場合、diagnostics に記録する。

## 9. actuator変換方針

SansaVRM の actuator 情報は、MuJoCo の `actuator` 要素へ変換する。

初期段階では、以下を対象とする。

- position actuator
- motor actuator
- velocity actuator

以下は将来拡張対象とする。

- general actuator
- dcmotor
- muscle

actuator 変換では、以下を扱う。

- actuator name
- target joint
- control mode
- gear
- ctrlrange
- forcerange
- kp
- kv

MJCF に直接出力できない制御情報は、controller_config へ分離する。

## 10. sensor変換方針

SansaVRM の sensor 情報は、MuJoCo の `sensor` 要素へ変換する。

初期段階では、以下を対象とする。

- jointpos
- jointvel
- actuatorfrc
- framepos
- framequat
- accelerometer
- gyro

sensor 変換で未対応の sensor type が存在する場合、diagnostics に記録する。

## 11. custom parameter mapping

MuJoCo 固有パラメータの MJCF 出力可否は、custom parameter schema に基づいて判定する。

`io_scope = mjcf` または `io_scope = both` のパラメータは、`mjcf_mapping` に従って MJCF へ出力する。

`io_scope = adapter_artifact` のパラメータは、MJCF へ出力せず、Adapter 側補助成果物へ分離する。

`io_scope = preserve_only` のパラメータは、SansaVRM 内に保持するが、MJCF へ出力しない。

`io_scope = unsupported` のパラメータは、diagnostics に記録する。

`io_scope = source_raw` のパラメータは、解釈せず source_raw として扱う。

## 12. controller_configへの分離

MJCF へ直接出力できないが MuJoCo 実行や制御に必要な情報は、controller_config へ分離する。

例：

- command delay
- deadband
- external PID configuration
- thermal model settings
- current limit
- voltage limit
- runtime control mode
- actuator update rate

controller_config へ分離した情報は、diagnostics または conversion_report に記録する。

## 13. 非可逆変換の扱い

SansaVRM から MJCF への変換で情報が完全再現できない場合、その情報を非可逆変換として扱う。

非可逆変換が発生した場合、以下を記録する。

- 対象情報
- 変換元
- 変換先
- 失われた情報
- fallback の有無
- severity

非可逆変換情報は diagnostics または conversion_report に記録する。

## 14. fallback方針

変換対象の情報が MJCF へ直接出力できない場合、custom parameter schema の fallback 方針に従う。

fallback 方針は以下を想定する。

- `use_default`
- `preserve_only`
- `warn`
- `error`
- `ignore`

fallback を適用した場合、diagnostics に記録する。

## 15. MuJoCoバージョン対応

MJCF の要素、属性、意味、推奨値は MuJoCo バージョンにより変化する可能性がある。

Adapter は、対象 MuJoCo バージョンに対する対応可否を custom parameter schema の version 情報に基づいて判定する。

未対応または非推奨のパラメータを検出した場合、diagnostics に記録する。

## 16. 出力ファイル名

標準的な MJCF 出力名は以下とする。

```text
model.xml
```

ローカル検証で生成した派生ファイルは Git 管理対象外とする。

## 17. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- MJCF XML writer の詳細実装
- controller_config schema の完全定義
- MuJoCo runtime の実装
- 強化学習環境の構築
- UI / editor 実装

## 18. 関連ドキュメント

- [仕様概要](../01_共通/01_仕様概要.md)
- [AdapterAPI前提](../01_共通/02_AdapterAPI前提.md)
- [成果物仕様](../01_共通/03_成果物仕様.md)
- [diagnostics仕様](../01_共通/04_diagnostics仕様.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > MJCF変換方針
