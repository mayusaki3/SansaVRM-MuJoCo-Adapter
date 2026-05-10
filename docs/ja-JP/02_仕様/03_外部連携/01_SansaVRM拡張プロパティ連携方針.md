<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260510-000001Z-SVMJ
lang: ja-JP
canonical_title: SansaVRM拡張プロパティ連携方針
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 外部連携 > SansaVRM拡張プロパティ連携方針

# SansaVRM拡張プロパティ連携方針

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter が SansaVRM Core と SansaVRM Extension Property をどのように扱うかを定義する。

本方針は、MuJoCo / Project Meridian / sysid / HIL-SIL / runtime 固有情報を SansaVRM Core 標準仕様へ直接組み込まず、SansaVRM 内に保存可能な拡張プロパティとして扱うために定義する。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、SansaVRM Core 標準仕様に MuJoCo / Project Meridian / sysid / HIL-SIL 固有仕様が直接組み込まれることを前提にしない。

Adapter は、以下を入力として扱う。

- SansaVRM Core 標準構造
- SansaVRM Extension Property
- Extension Property Schema
- Source raw data
- Normalized value
- Diagnostics reference
- Conversion report reference

MuJoCo / Project Meridian / sysid / HIL-SIL / runtime 固有情報は、SansaVRM Extension Property として読み取り、必要に応じて Adapter 成果物へ変換する。

## 3. SansaVRM Coreの責務

SansaVRM Core は、外部フォーマット間の semantic integration を目的とする。

SansaVRM Core は、特定 runtime、特定 adapter、特定 hardware、特定 firmware、特定 sysid 結果へ依存してはならない。

SansaVRM Core が標準的に保持する対象は以下とする。

- Module
- Connection
- Slot
- Property
- structure semantic
- transform semantic
- humanoid semantic
- expression semantic
- basic physics semantic

## 4. Extension Propertyの責務

Extension Property は、SansaVRM Core に固定導入しない追加情報を保持する。

以下は Extension Property 側で扱う。

- device_category
- device_identity
- capability_profile
- command_semantics
- command_transport
- actuator_model
- behavior_model
- sysid_result_ref
- runtime_requirements
- HIL / SIL metadata
- Project Meridian runtime metadata
- controller_config metadata
- diagnostics_ref
- conversion_report_ref
- source_raw

## 5. Adapterの責務

SansaVRM-MuJoCo-Adapter は、SansaVRM Core 標準構造と Extension Property を参照し、MuJoCo 向け成果物を生成する。

Adapter は、以下を担当する。

- SansaVRM Core 標準構造の読み取り
- Extension Property の読み取り
- Extension Property の namespace / target_type / property_role / io_scope / adapter_scope による分類
- MJCF へ直接出力できる情報の `model.xml` への出力
- MJCF へ直接出力しない情報の `controller_config.json` への分離
- runtime 側で必要な情報の `runtime_requirements.json` への分離
- unsupported / preserve_only / source_raw の diagnostics 記録
- conversion_report への変換結果記録
- Project Meridian 由来の更新結果を Extension Property として再格納できる形式への変換

## 6. Adapterの非責務

SansaVRM-MuJoCo-Adapter は、以下を担当しない。

- SansaVRM Core 仕様の肥大化
- MuJoCo runtime の継続実行
- sysid optimizer
- 実測ログ処理
- HIL / SIL bridge
- 実ボード通信
- device specific driver
- firmware 固有制御
- ニソコンVRの試合・ルール・判定・進行管理

## 7. 関連プロジェクトとの関係

関連プロジェクトの責務境界は以下とする。

```text
SansaVRM
  ↓
SansaVRM-MuJoCo-Adapter
  ↓
Project Meridian / meridian-mujoco-runtime
  ↓
MuJoCo

nisocon-vr-battle-runtime
  ↓ uses
meridian-mujoco-runtime
```

### 7.1 SansaVRM

SansaVRM は、Core 標準構造と Extension Property を保持する。

SansaVRM は、MuJoCo / Project Meridian / sysid / HIL-SIL の実行処理を担当しない。

### 7.2 SansaVRM-MuJoCo-Adapter

SansaVRM-MuJoCo-Adapter は、SansaVRM から MuJoCo / Project Meridian 向け成果物を生成する。

### 7.3 meridian-mujoco-runtime

meridian-mujoco-runtime は、MuJoCo runtime、sysid、ActuatorModel runtime、HIL / SIL、実ボード同期を担当する。

### 7.4 nisocon-vr-battle-runtime

nisocon-vr-battle-runtime は、試合、ルール、判定、進行管理を担当する。

SansaVRM-MuJoCo-Adapter は、nisocon-vr-battle-runtime と直接結合しない。

## 8. Extension Property構造案

Extension Property は、以下の構造を持つことを想定する。

```json
{
  "extension_property": {
    "namespace": "mujoco",
    "target_type": "actuator",
    "target_id": "left_knee_servo",
    "property_role": "control",
    "io_scope": "adapter_artifact",
    "adapter_scope": "sansavrm_mujoco_adapter",
    "source_format": "sansavrm_extension_property",
    "source_raw": null,
    "normalized_value": {
      "command_delay_ms": 5
    },
    "schema_ref": "schemas/extension_property/mujoco/control/command_delay.schema.json",
    "diagnostics_ref": [],
    "conversion_report_ref": []
  }
}
```

## 9. namespace

`namespace` は、拡張プロパティが属する領域を示す。

初期候補は以下とする。

- `mujoco`
- `meridian`
- `sysid`
- `hil`
- `sil`
- `controller_config`
- `diagnostics`
- `conversion_report`
- `source_raw`
- `vendor`
- `experimental`

## 10. target_type / target_id

`target_type` は、拡張プロパティの適用対象を示す。

初期候補は以下とする。

- `model`
- `module`
- `connection`
- `slot`
- `property`
- `joint`
- `collider`
- `actuator`
- `sensor`
- `device`
- `runtime`
- `artifact`

`target_id` は、対象を識別する ID である。

対象がモデル全体または runtime 全体である場合は `null` を許容する。

## 11. property_role

`property_role` は、拡張プロパティの意味上の役割を表す。

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

## 12. io_scope

`io_scope` は、拡張プロパティの出力先または保持方針を定義する。

初期候補は以下とする。

- `mjcf`
- `adapter_artifact`
- `runtime_artifact`
- `both`
- `preserve_only`
- `unsupported`
- `source_raw`

### 12.1 mjcf

`io_scope = mjcf` は、対象情報を MJCF へ直接出力できることを示す。

### 12.2 adapter_artifact

`io_scope = adapter_artifact` は、対象情報を Adapter 側成果物へ出力することを示す。

初期対象は以下とする。

- `controller_config.json`
- `diagnostics.json`
- `conversion_report.json`

### 12.3 runtime_artifact

`io_scope = runtime_artifact` は、対象情報を runtime 側成果物へ出力することを示す。

初期対象は以下とする。

- `runtime_requirements.json`
- meridian runtime metadata
- HIL / SIL metadata

### 12.4 both

`io_scope = both` は、MJCF と Adapter / runtime 成果物の両方に関係することを示す。

### 12.5 preserve_only

`io_scope = preserve_only` は、SansaVRM 内に保持するが、Adapter は出力しないことを示す。

### 12.6 unsupported

`io_scope = unsupported` は、登録済みだが現在の Adapter では未対応であることを示す。

### 12.7 source_raw

`io_scope = source_raw` は、解釈せずに元情報として保持することを示す。

## 13. adapter_scope

`adapter_scope` は、対象拡張プロパティを扱う主体を示す。

初期候補は以下とする。

- `sansavrm_mujoco_adapter`
- `meridian_mujoco_runtime`
- `nisocon_vr_battle_runtime`
- `preserve_only`
- `unknown`

SansaVRM-MuJoCo-Adapter は、`adapter_scope = sansavrm_mujoco_adapter` の項目を直接処理対象とする。

`adapter_scope = meridian_mujoco_runtime` の項目は、runtime_requirements または Project Meridian 向け情報として分離する。

`adapter_scope = nisocon_vr_battle_runtime` の項目は、原則として Adapter では処理せず、preserve_only または unsupported として扱う。

## 14. source_raw / normalized_value

Extension Property は、必要に応じて `source_raw` と `normalized_value` を同時に保持できる。

`source_raw` は、元フォーマット、通信パケット、vendor 固有値、runtime 固有値を保存するために使用する。

`normalized_value` は、Adapter / runtime / sysid が共通処理できる正規化値として使用する。

Adapter は、`source_raw` だけを根拠に推測変換してはならない。

変換には、schema_ref または Extension Property Schema を使用する。

## 15. schema_ref

`schema_ref` は、Extension Property の構造、値型、単位、mapping、fallback を定義する schema を参照する。

Adapter は、schema_ref がある場合、schema に基づいて処理する。

schema_ref がない場合は、以下のいずれかとして扱う。

- preserve_only
- unsupported
- diagnostics 記録

## 16. diagnostics_ref / conversion_report_ref

Extension Property は、関連する diagnostics と conversion_report を参照できる。

`diagnostics_ref` は、変換、分離、fallback、unsupported、source_raw 扱いの理由を追跡するために使用する。

`conversion_report_ref` は、どの変換処理により生成または更新されたかを追跡するために使用する。

## 17. runtime更新結果の再格納

meridian-mujoco-runtime により sysid、ActuatorModel、HIL / SIL、runtime metadata が更新された場合、更新結果は Extension Property として SansaVRM に再格納できる形式にする。

再格納時は、以下を記録する。

- namespace
- target_type
- target_id
- property_role
- adapter_scope
- source_format
- normalized_value
- source_raw
- schema_ref
- diagnostics_ref
- conversion_report_ref

## 18. custom parameterとの関係

既存の custom parameter は、Extension Property の一種として扱う。

今後の上位概念は Extension Property とし、custom parameter は以下のように位置づける。

```text
extension_property
  └─ custom parameter
```

既存仕様で `custom parameter` と記載している箇所は、当面互換性維持のため残す。

ただし、今後の拡張では `Extension Property` を優先用語とする。

## 19. Adapter成果物との関係

SansaVRM-MuJoCo-Adapter は、Extension Property を参照して以下を生成する。

- `model.xml`
- `controller_config.json`
- `diagnostics.json`
- `conversion_report.json`
- `runtime_requirements.json`

## 20. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM Core 標準仕様の詳細定義
- Extension Property Schema の完全定義
- meridian-mujoco-runtime の実装
- sysid optimizer の実装
- HIL / SIL bridge の実装
- nisocon-vr-battle-runtime の実装

## 21. 関連ドキュメント

- [AdapterAPI前提](../01_共通/02_AdapterAPI前提.md)
- [成果物仕様](../01_共通/03_成果物仕様.md)
- [diagnostics仕様](../01_共通/04_diagnostics仕様.md)
- [custom parameter mapping](../02_MuJoCo連携/03_custom_parameter_mapping.md)
- [controller_config仕様](../02_MuJoCo連携/04_controller_config仕様.md)
- [トレーサビリティ運用方針](../../05_トレーサビリティ/01_共通/00_トレーサビリティ運用方針.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 外部連携 > SansaVRM拡張プロパティ連携方針
