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

custom parameter は、SansaVRM Extension Property の一種として扱う。

## 2. 基本方針

Adapter は、custom parameter の出力先を実装側の推測で判定してはならない。

Adapter は、SansaVRM 本体 API から取得した Extension Property Schema または custom parameter schema に基づいて、以下を判定する。

- MJCF へ直接入出力できるか
- Adapter 側補助成果物へ出力するか
- runtime 側成果物へ出力するか
- MJCF と Adapter 側補助成果物の両方へ出力するか
- SansaVRM 内に保持するだけか
- 未対応として扱うか
- source_raw として扱うか

## 3. Extension Propertyとの関係

custom parameter は、Extension Property の一種である。

今後の上位概念は Extension Property とし、custom parameter は既存互換のために維持する。

```text
extension_property
  └─ custom parameter
```

Extension Property として扱う場合、以下の項目を参照する。

- namespace
- target_type
- target_id
- property_role
- io_scope
- adapter_scope
- source_format
- source_raw
- normalized_value
- schema_ref
- diagnostics_ref
- conversion_report_ref

custom parameter schema に存在しない項目が必要な場合は、Extension Property Schema を優先する。

## 4. 入力情報

custom parameter mapping では、以下を入力とする。

- custom parameter value
- custom parameter schema
- extension property
- extension property schema
- namespace
- target_type
- target_id
- property_role
- io_scope
- adapter_scope
- mjcf_mapping
- adapter_artifact
- external_runtime_mapping
- mujoco_version
- supported_since
- deprecated_since
- fallback

## 5. 出力情報

custom parameter mapping では、以下のいずれかへ情報を出力する。

- MJCF
- controller_config
- runtime_requirements
- runtime_config
- external_metadata
- conversion_report
- diagnostics
- preserve_only
- source_raw

## 6. namespace

custom parameter は namespace を持つ。

MuJoCo 固有パラメータは、原則として以下の namespace を使用する。

```text
mujoco
```

Project Meridian / runtime / sysid / HIL-SIL 連携では、以下の namespace を使用できる。

- `meridian`
- `sysid`
- `hil`
- `sil`
- `controller_config`
- `diagnostics`
- `conversion_report`
- `source_raw`

将来の拡張では、以下の namespace を使用できる。

- `urdf`
- `vrm`
- `unity`
- `o3de`
- `vendor`
- `experimental`

Adapter は、namespace が `mujoco` 以外の parameter を検出した場合、`adapter_scope` と `io_scope` に基づいて処理対象、runtime成果物対象、preserve_only、unsupported のいずれかに分類する。

## 7. target_type

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
- device
- runtime
- artifact

target_type が未対応の場合、diagnostics に記録する。

## 8. property_role

`property_role` は、Extension Property としての意味上の役割を表す。

初期候補は以下とする。

- `physics`
- `actuator`
- `sensor`
- `control`
- `runtime`
- `sysid`
- `hil`
- `sil`
- `diagnostics`
- `conversion_report`
- `source_raw`

custom parameter schema に `property_role` がない場合、Adapter は namespace、target_type、schema_ref に基づいて分類してよい。

分類できない場合は diagnostics に記録する。

## 9. io_scope

`io_scope` は、custom parameter または Extension Property の入出力範囲を定義する。

`io_scope` は以下のいずれかとする。

- `mjcf`
- `adapter_artifact`
- `runtime_artifact`
- `both`
- `preserve_only`
- `unsupported`
- `source_raw`

### 9.1 mjcf

`io_scope = mjcf` は、対象 parameter を MJCF へ直接入出力できることを示す。

この場合、原則として `mjcf_mapping` を定義する。

### 9.2 adapter_artifact

`io_scope = adapter_artifact` は、対象 parameter を MJCF へ直接入出力せず、Adapter 側補助成果物へ出力することを示す。

この場合、原則として `adapter_artifact` を定義する。

### 9.3 runtime_artifact

`io_scope = runtime_artifact` は、対象 parameter を Project Meridian / meridian-mujoco-runtime などの runtime 側成果物へ出力することを示す。

この場合、原則として `external_runtime_mapping` を定義する。

### 9.4 both

`io_scope = both` は、対象 parameter を MJCF と Adapter 側補助成果物、または MJCF と runtime 側成果物の両方へ出力することを示す。

この場合、原則として `mjcf_mapping` と `adapter_artifact` または `external_runtime_mapping` を定義する。

### 9.5 preserve_only

`io_scope = preserve_only` は、対象 parameter を SansaVRM 内に保持するが、MJCF または Adapter 側補助成果物へは出力しないことを示す。

Adapter は、preserve_only の情報を変換出力へ反映しない。

### 9.6 unsupported

`io_scope = unsupported` は、対象 parameter が登録済みであるが、現在の Adapter または対象 MuJoCo バージョンでは未対応であることを示す。

Adapter は、unsupported を diagnostics に記録する。

### 9.7 source_raw

`io_scope = source_raw` は、対象 parameter を解釈せず、元情報として保持することを示す。

Adapter は、source_raw を MJCF へ直接出力してはならない。

## 10. adapter_scope

`adapter_scope` は、対象 parameter または Extension Property を扱う主体を示す。

初期候補は以下とする。

- `sansavrm_mujoco_adapter`
- `meridian_mujoco_runtime`
- `nisocon_vr_battle_runtime`
- `preserve_only`
- `unknown`

SansaVRM-MuJoCo-Adapter は、`adapter_scope = sansavrm_mujoco_adapter` の項目を直接処理対象とする。

`adapter_scope = meridian_mujoco_runtime` の項目は、`runtime_requirements` または runtime 側成果物へ分離する。

`adapter_scope = nisocon_vr_battle_runtime` の項目は、原則として Adapter では処理せず、preserve_only または unsupported として扱う。

## 11. mjcf_mapping

`mjcf_mapping` は、MJCF へ直接入出力できる parameter の対応先を定義する。

`mjcf_mapping` は、少なくとも以下を持つ。

- element
- attribute
- path
- direction
- value_conversion
- required_mujoco_version

### 11.1 element

`element` は、出力先の MJCF 要素を表す。

例：

- `joint`
- `geom`
- `actuator`
- `sensor`
- `option`
- `default`

### 11.2 attribute

`attribute` は、出力先の MJCF 属性を表す。

例：

- `armature`
- `damping`
- `frictionloss`
- `forcerange`
- `ctrlrange`

### 11.3 path

`path` は、MJCF 内の対応箇所を表す。

例：

```text
joint.@armature
actuator.position.@forcerange
geom.@friction
```

### 11.4 direction

`direction` は、入出力方向を表す。

以下のいずれかとする。

- `import`
- `export`
- `import_export`

### 11.5 value_conversion

`value_conversion` は、値の単位変換、形式変換、範囲変換の方法を定義する。

例：

- degree to radian
- rpm to rad/s
- scalar to symmetric range
- boolean to enum

### 11.6 required_mujoco_version

`required_mujoco_version` は、対象 mapping を使用できる MuJoCo バージョン範囲を定義する。

対象バージョンで利用できない場合、fallback 方針に従う。

## 12. adapter_artifact

`adapter_artifact` は、MJCF に直接出力しない parameter の出力先を定義する。

`adapter_artifact` は、少なくとも以下を持つ。

- artifact_type
- path
- direction
- value_conversion
- required_adapter_version

### 12.1 artifact_type

`artifact_type` は、出力先の Adapter 側補助成果物を表す。

初期候補は以下とする。

- `controller_config`
- `runtime_config`
- `external_metadata`
- `conversion_report`
- `diagnostics`

### 12.2 path

`path` は、補助成果物内の出力先を表す。

例：

```text
actuators[].command_delay_ms
actuators[].deadband_rad
actuators[].current_limit_a
```

### 12.3 direction

`direction` は、入出力方向を表す。

以下のいずれかとする。

- `import`
- `export`
- `import_export`

### 12.4 value_conversion

`value_conversion` は、補助成果物へ出力する際の値変換を定義する。

### 12.5 required_adapter_version

`required_adapter_version` は、対象 mapping を使用できる Adapter バージョン範囲を定義する。

対象バージョンで利用できない場合、fallback 方針に従う。

## 13. external_runtime_mapping

`external_runtime_mapping` は、Project Meridian / meridian-mujoco-runtime などの外部 runtime 側成果物へ渡す情報の出力先を定義する。

`external_runtime_mapping` は、少なくとも以下を持つ。

- runtime
- artifact_type
- path
- direction
- value_conversion
- required_runtime_version

初期 runtime 候補は以下とする。

- `meridian_mujoco_runtime`

初期 artifact_type 候補は以下とする。

- `runtime_requirements`
- `runtime_config`
- `sysid_result_ref`
- `hil_sil_metadata`

## 14. value_conversion方針

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

## 15. MuJoCoバージョン対応

custom parameter mapping は、MuJoCo バージョン情報を持つことができる。

Adapter は、対象 MuJoCo バージョンに対して mapping が有効かを確認する。

未対応、非推奨、または廃止された parameter を検出した場合、diagnostics に記録する。

## 16. fallback方針

mapping が適用できない場合、Extension Property Schema または custom parameter schema の fallback 方針に従う。

fallback 方針は以下を想定する。

- `use_default`
- `preserve_only`
- `warn`
- `error`
- `ignore`

fallback を適用した場合、diagnostics または conversion_report に記録する。

## 17. diagnostics記録対象

custom parameter mapping では、以下を diagnostics に記録する。

- 未対応 namespace
- 未対応 target_type
- 未対応 property_role
- 未対応 io_scope
- 未対応 adapter_scope
- mjcf_mapping 不足
- adapter_artifact 不足
- external_runtime_mapping 不足
- value_conversion 不明
- MuJoCo バージョン非対応
- Adapter バージョン非対応
- runtime バージョン非対応
- fallback 適用
- source_raw 扱い

## 18. 出力例: MJCF出力対象

```json
{
  "namespace": "mujoco",
  "name": "armature",
  "target_type": "joint",
  "property_role": "physics",
  "value_type": "number",
  "unit": "kg*m^2",
  "io_scope": "mjcf",
  "adapter_scope": "sansavrm_mujoco_adapter",
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
  "external_runtime_mapping": null,
  "fallback": {
    "behavior": "use_default",
    "value": 0.0
  }
}
```

## 19. 出力例: Adapter補助成果物対象

```json
{
  "namespace": "mujoco",
  "name": "command_delay_ms",
  "target_type": "actuator",
  "property_role": "control",
  "value_type": "number",
  "unit": "ms",
  "io_scope": "adapter_artifact",
  "adapter_scope": "sansavrm_mujoco_adapter",
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
  "external_runtime_mapping": null,
  "fallback": {
    "behavior": "warn",
    "value": 0
  }
}
```

## 20. 出力例: runtime成果物対象

```json
{
  "namespace": "meridian",
  "name": "requires_external_control_loop",
  "target_type": "runtime",
  "property_role": "runtime",
  "value_type": "boolean",
  "unit": null,
  "io_scope": "runtime_artifact",
  "adapter_scope": "meridian_mujoco_runtime",
  "mjcf_mapping": null,
  "adapter_artifact": null,
  "external_runtime_mapping": {
    "runtime": "meridian_mujoco_runtime",
    "artifact_type": "runtime_requirements",
    "path": "runtime_requirements.requires_external_control_loop",
    "direction": "export",
    "value_conversion": null,
    "required_runtime_version": {
      "min": "0.1.0",
      "max": null
    }
  },
  "fallback": {
    "behavior": "warn",
    "value": false
  }
}
```

## 21. 出力例: 両方へ出力する対象

```json
{
  "namespace": "mujoco",
  "name": "torque_limit_nm",
  "target_type": "actuator",
  "property_role": "control",
  "value_type": "number",
  "unit": "N*m",
  "io_scope": "both",
  "adapter_scope": "sansavrm_mujoco_adapter",
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
  "external_runtime_mapping": null,
  "fallback": {
    "behavior": "error"
  }
}
```

## 22. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM 本体側 Extension Property Schema の正本定義
- SansaVRM 本体側 custom parameter schema の正本定義
- MJCF writer の詳細実装
- controller_config schema の完全定義
- runtime_requirements schema の完全定義
- UI 表示仕様
- MuJoCo runtime の実装
- Project Meridian runtime の実装

## 23. 関連ドキュメント

- [MJCF変換方針](./01_MJCF変換方針.md)
- [アクチュエータ写像](./02_アクチュエータ写像.md)
- [controller_config仕様](./04_controller_config仕様.md)
- [MuJoCoバージョン対応方針](./05_MuJoCoバージョン対応方針.md)
- [SansaVRM拡張プロパティ連携方針](../03_外部連携/01_SansaVRM拡張プロパティ連携方針.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > custom parameter mapping
