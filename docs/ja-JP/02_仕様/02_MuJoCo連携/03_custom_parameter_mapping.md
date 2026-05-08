<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000014Z-SVMJ
lang: ja-JP
canonical_title: custom parameter mapping
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > custom parameter mapping

# custom parameter mapping

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter における custom parameter mapping の方針を定義する。

custom parameter mapping は、SansaVRM 本体が保持する namespace 付き custom parameter と custom parameter schema を参照し、MuJoCo / MJCF / controller_config / diagnostics / conversion_report へどのように反映するかを決定するために使用する。

## 2. 基本方針

Adapter は、custom parameter の出力先を実装側の推測で判定してはならない。

Adapter は、SansaVRM 本体 API から取得した custom parameter schema に基づいて、以下を判定する。

- MJCF へ直接入出力できるか
- Adapter 側補助成果物へ出力するか
- MJCF と Adapter 側補助成果物の両方へ出力するか
- SansaVRM 内に保持するだけか
- 未対応として扱うか
- source_raw として扱うか

## 3. 入力情報

custom parameter mapping では、以下を入力とする。

- custom parameter value
- custom parameter schema
- namespace
- target_type
- target_id
- io_scope
- mjcf_mapping
- adapter_artifact
- mujoco_version
- supported_since
- deprecated_since
- fallback

## 4. 出力情報

custom parameter mapping では、以下のいずれかへ情報を出力する。

- MJCF
- controller_config
- runtime_config
- external_metadata
- conversion_report
- diagnostics
- preserve_only
- source_raw

## 5. namespace

custom parameter は namespace を持つ。

MuJoCo 固有パラメータは、原則として以下の namespace を使用する。

```text
mujoco
```

将来の拡張では、以下の namespace を使用できる。

- `urdf`
- `vrm`
- `unity`
- `o3de`
- `vendor`
- `experimental`

Adapter は、namespace が `mujoco` 以外の parameter を検出した場合、対象範囲に応じて preserve_only または diagnostics に記録する。

## 6. target_type

custom parameter は、適用対象を示す target_type を持つ。

初期候補は以下とする。

- model
- module
- connection
- slot
- property
- joint
- collider
- actuator
- sensor
- artifact

target_type が未対応の場合、diagnostics に記録する。

## 7. io_scope

`io_scope` は、custom parameter の入出力範囲を定義する。

`io_scope` は以下のいずれかとする。

- `mjcf`
- `adapter_artifact`
- `both`
- `preserve_only`
- `unsupported`
- `source_raw`

### 7.1 mjcf

`io_scope = mjcf` は、対象 parameter を MJCF へ直接入出力できることを示す。

この場合、原則として `mjcf_mapping` を定義する。

### 7.2 adapter_artifact

`io_scope = adapter_artifact` は、対象 parameter を MJCF へ直接入出力せず、Adapter 側補助成果物へ出力することを示す。

この場合、原則として `adapter_artifact` を定義する。

### 7.3 both

`io_scope = both` は、対象 parameter を MJCF と Adapter 側補助成果物の両方へ出力することを示す。

この場合、原則として `mjcf_mapping` と `adapter_artifact` の両方を定義する。

### 7.4 preserve_only

`io_scope = preserve_only` は、対象 parameter を SansaVRM 内に保持するが、MJCF または Adapter 側補助成果物へは出力しないことを示す。

Adapter は、preserve_only の情報を変換出力へ反映しない。

### 7.5 unsupported

`io_scope = unsupported` は、対象 parameter が登録済みであるが、現在の Adapter または対象 MuJoCo バージョンでは未対応であることを示す。

Adapter は、unsupported を diagnostics に記録する。

### 7.6 source_raw

`io_scope = source_raw` は、対象 parameter を解釈せず、元情報として保持することを示す。

Adapter は、source_raw を MJCF へ直接出力してはならない。

## 8. mjcf_mapping

`mjcf_mapping` は、MJCF へ直接入出力できる parameter の対応先を定義する。

`mjcf_mapping` は、少なくとも以下を持つ。

- element
- attribute
- path
- direction
- value_conversion
- required_mujoco_version

### 8.1 element

`element` は、出力先の MJCF 要素を表す。

例：

- `joint`
- `geom`
- `actuator`
- `sensor`
- `option`
- `default`

### 8.2 attribute

`attribute` は、出力先の MJCF 属性を表す。

例：

- `armature`
- `damping`
- `frictionloss`
- `forcerange`
- `ctrlrange`

### 8.3 path

`path` は、MJCF 内の対応箇所を表す。

例：

```text
joint.@armature
actuator.position.@forcerange
geom.@friction
```

### 8.4 direction

`direction` は、入出力方向を表す。

以下のいずれかとする。

- `import`
- `export`
- `import_export`

### 8.5 value_conversion

`value_conversion` は、値の単位変換、形式変換、範囲変換の方法を定義する。

例：

- degree to radian
- rpm to rad/s
- scalar to symmetric range
- boolean to enum

### 8.6 required_mujoco_version

`required_mujoco_version` は、対象 mapping を使用できる MuJoCo バージョン範囲を定義する。

対象バージョンで利用できない場合、fallback 方針に従う。

## 9. adapter_artifact

`adapter_artifact` は、MJCF に直接出力しない parameter の出力先を定義する。

`adapter_artifact` は、少なくとも以下を持つ。

- artifact_type
- path
- direction
- value_conversion
- required_adapter_version

### 9.1 artifact_type

`artifact_type` は、出力先の Adapter 側補助成果物を表す。

初期候補は以下とする。

- `controller_config`
- `runtime_config`
- `external_metadata`
- `conversion_report`
- `diagnostics`

### 9.2 path

`path` は、補助成果物内の出力先を表す。

例：

```text
actuators[].command_delay_ms
actuators[].deadband_rad
actuators[].current_limit_a
```

### 9.3 direction

`direction` は、入出力方向を表す。

以下のいずれかとする。

- `import`
- `export`
- `import_export`

### 9.4 value_conversion

`value_conversion` は、補助成果物へ出力する際の値変換を定義する。

### 9.5 required_adapter_version

`required_adapter_version` は、対象 mapping を使用できる Adapter バージョン範囲を定義する。

対象バージョンで利用できない場合、fallback 方針に従う。

## 10. value_conversion方針

Adapter は、value_conversion が定義されている場合、その変換規則に従う。

value_conversion が未定義の場合は、値をそのまま出力する。

ただし、単位不一致が疑われる場合、diagnostics に記録する。

初期候補は以下とする。

- `none`
- `degree_to_radian`
- `radian_to_degree`
- `rpm_to_rad_per_sec`
- `rad_per_sec_to_rpm`
- `scalar_to_symmetric_range`
- `kgf_cm_to_nm`

## 11. MuJoCoバージョン対応

custom parameter mapping は、MuJoCo バージョン情報を持つことができる。

Adapter は、対象 MuJoCo バージョンに対して mapping が有効かを確認する。

未対応、非推奨、または廃止された parameter を検出した場合、diagnostics に記録する。

## 12. fallback方針

mapping が適用できない場合、custom parameter schema の fallback 方針に従う。

fallback 方針は以下を想定する。

- `use_default`
- `preserve_only`
- `warn`
- `error`
- `ignore`

fallback を適用した場合、diagnostics または conversion_report に記録する。

## 13. diagnostics記録対象

custom parameter mapping では、以下を diagnostics に記録する。

- 未対応 namespace
- 未対応 target_type
- 未対応 io_scope
- mjcf_mapping 不足
- adapter_artifact 不足
- value_conversion 不明
- MuJoCo バージョン非対応
- Adapter バージョン非対応
- fallback 適用
- source_raw 扱い

## 14. 出力例: MJCF出力対象

```json
{
  "namespace": "mujoco",
  "name": "armature",
  "target_type": "joint",
  "value_type": "number",
  "unit": "kg*m^2",
  "io_scope": "mjcf",
  "mjcf_mapping": {
    "element": "joint",
    "attribute": "armature",
    "path": "joint.@armature",
    "direction": "import_export",
    "value_conversion": null,
    "required_mujoco_version": {
      "min": "2.3.0",
      "max": null
    }
  },
  "adapter_artifact": null,
  "fallback": {
    "behavior": "use_default",
    "value": 0.0
  }
}
```

## 15. 出力例: Adapter補助成果物対象

```json
{
  "namespace": "mujoco",
  "name": "command_delay_ms",
  "target_type": "actuator",
  "value_type": "number",
  "unit": "ms",
  "io_scope": "adapter_artifact",
  "mjcf_mapping": null,
  "adapter_artifact": {
    "artifact_type": "controller_config",
    "path": "actuators[].command_delay_ms",
    "direction": "export",
    "value_conversion": null,
    "required_adapter_version": {
      "min": "0.1.0",
      "max": null
    }
  },
  "fallback": {
    "behavior": "warn",
    "value": 0
  }
}
```

## 16. 出力例: 両方へ出力する対象

```json
{
  "namespace": "mujoco",
  "name": "torque_limit_nm",
  "target_type": "actuator",
  "value_type": "number",
  "unit": "N*m",
  "io_scope": "both",
  "mjcf_mapping": {
    "element": "actuator",
    "attribute": "forcerange",
    "path": "actuator.*.@forcerange",
    "direction": "export",
    "value_conversion": {
      "type": "scalar_to_symmetric_range",
      "source_unit": "N*m",
      "target_format": "-value value"
    },
    "required_mujoco_version": {
      "min": "2.3.0",
      "max": null
    }
  },
  "adapter_artifact": {
    "artifact_type": "controller_config",
    "path": "actuators[].torque_limit_nm",
    "direction": "export",
    "value_conversion": null,
    "required_adapter_version": {
      "min": "0.1.0",
      "max": null
    }
  },
  "fallback": {
    "behavior": "error"
  }
}
```

## 17. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM 本体側 custom parameter schema の正本定義
- MJCF writer の詳細実装
- controller_config schema の完全定義
- UI 表示仕様
- MuJoCo runtime の実装

## 18. 関連ドキュメント

- `02_仕様/02_MuJoCo連携/01_MJCF変換方針.md`
- `02_仕様/02_MuJoCo連携/02_アクチュエータ写像.md`
- `02_仕様/02_MuJoCo連携/04_controller_config仕様.md`
- `02_仕様/02_MuJoCo連携/05_MuJoCoバージョン対応方針.md`

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > custom parameter mapping
