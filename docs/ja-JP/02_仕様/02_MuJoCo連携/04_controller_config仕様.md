<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000015Z-SVMJ
lang: ja-JP
canonical_title: controller_config仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > controller_config仕様

# controller_config仕様

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter が生成する `controller_config` の目的、役割、記録対象、出力方針を定義する。

`controller_config` は、MJCF に直接出力しない制御・実行補助情報を保持する Adapter 側補助成果物である。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、MJCF に直接出力できないが MuJoCo 実行や制御に必要な情報を `controller_config` へ分離する。

分離対象は、Extension Property Schema または custom parameter schema の `io_scope`、`adapter_scope`、`adapter_artifact` に基づいて判定する。

Adapter は、`controller_config` へ出力すべきかどうかを実装側の推測で判定してはならない。

`controller_config` は、SansaVRM Core 標準仕様を拡張するものではない。

`controller_config` は、SansaVRM Extension Property に含まれる制御・実行補助情報を Adapter 側成果物として分離したものである。

## 3. runtime_requirementsとの関係

`controller_config` は、MuJoCo 実行時の制御・アクチュエータ補助情報を保持する。

`runtime_requirements` は、meridian-mujoco-runtime などの外部 runtime に必要な機能要求を保持する。

両者を混同してはならない。

例：

```text
controller_config:
  actuatorごとの command_delay / deadband / current_limit / external PID

runtime_requirements:
  requires_external_control_loop / requires_sysid_result / requires_hil / required_features
```

`adapter_scope = sansavrm_mujoco_adapter` かつ `io_scope = adapter_artifact` の情報は、原則として `controller_config` の対象とする。

`adapter_scope = meridian_mujoco_runtime` または `io_scope = runtime_artifact` の情報は、原則として `runtime_requirements` の対象とする。

## 4. 出力ファイル名

標準的な出力ファイル名は以下とする。

```text
controller_config.json
```

ローカル検証専用ファイルは以下の名称を使用できる。

```text
controller_config.local.json
```

`controller_config.local.json` は Git 管理対象外とする。

## 5. 対象情報

`controller_config` は、初期段階では以下の情報を対象とする。

- actuator control mode
- command delay
- deadband
- velocity limit
- acceleration limit
- current limit
- voltage limit
- external PID configuration
- thermal model settings
- runtime update rate
- controller runtime option
- diagnostics_ref
- conversion_report_ref

## 6. 入力となるExtension Property

`controller_config` へ分離する Extension Property は、原則として以下を満たす。

- `adapter_scope = sansavrm_mujoco_adapter`
- `io_scope = adapter_artifact` または `io_scope = both`
- `adapter_artifact.artifact_type = controller_config`

対象 Extension Property では、以下を参照する。

- namespace
- target_type
- target_id
- property_role
- io_scope
- adapter_scope
- normalized_value
- source_raw
- schema_ref
- adapter_artifact
- diagnostics_ref
- conversion_report_ref

Adapter は、`source_raw` だけを根拠に controller_config を生成してはならない。

Adapter は、Extension Property Schema または custom parameter schema に基づいて値を解釈する。

## 7. actuator設定

`controller_config` は、actuator 単位の設定を保持する。

actuator 設定は、少なくとも以下を持つ。

- actuator_id
- target_joint
- control_mode
- runtime_control_mode
- parameters
- diagnostics_ref

将来必要に応じて、以下を追加できる。

- conversion_report_ref
- source_extension_property_ref
- schema_ref

## 8. control_mode

`control_mode` は、SansaVRM 側または Adapter 側で扱う制御モードを表す。

初期候補は以下とする。

- `position`
- `velocity`
- `torque`
- `force`
- `external_controller`

## 9. runtime_control_mode

`runtime_control_mode` は、MuJoCo 実行時に Adapter runtime または外部 controller が使用する制御方式を表す。

初期候補は以下とする。

- `none`
- `position_pid`
- `velocity_pid`
- `torque_passthrough`
- `external`

`runtime_control_mode = external` の場合、runtime_requirements 側に外部制御ループ要求を出す必要がある。

## 10. command delay

command delay は、制御指令を遅延させるための設定である。

MJCF には直接出力しない。

`controller_config` では、以下のように記録する。

```json
{
  "command_delay_ms": 5
}
```

## 11. deadband

deadband は、制御誤差が一定範囲内にある場合の無反応領域を表す。

MJCF には直接出力しない。

`controller_config` では、以下のように記録する。

```json
{
  "deadband_rad": 0.01
}
```

## 12. velocity limit

velocity limit は、制御対象の最大速度を表す。

velocity actuator の `ctrlrange` へ直接写像できる場合は MJCF へ出力してよい。

position actuator の速度制限など、MJCF へ直接表現しにくい場合は `controller_config` へ分離する。

分類は Extension Property Schema または custom parameter schema の `io_scope` と mapping に従う。

## 13. acceleration limit

acceleration limit は、制御対象の最大加速度を表す。

初期段階では MJCF へ直接出力しない。

`controller_config` へ分離する。

## 14. current limit / voltage limit

current limit と voltage limit は、原則として MJCF へ直接出力しない。

以下のいずれかとして扱う。

- torque limit 算出に使用する
- `controller_config` へ出力する
- runtime_requirements へ機能要求として出力する
- preserve_only として保持する

算出に使用した場合は、conversion_report または diagnostics に記録する。

## 15. external PID configuration

外部 PID 設定は、MuJoCo runtime または Adapter runtime が制御入力を生成する場合に使用する。

初期候補は以下とする。

- kp
- ki
- kd
- integral_limit
- output_limit
- derivative_filter

MuJoCo の position actuator の `kp` / `kv` へ写像する場合と、外部 PID として扱う場合を混同してはならない。

外部制御ループが必須となる場合は、runtime_requirements にも要求を記録する。

## 16. thermal model settings

thermal model settings は、温度上昇、連続トルク、ピークトルク継続時間、温度保護などの情報を保持する。

初期段階では MJCF へ直接出力しない。

`controller_config`、runtime_requirements、または将来の `runtime_config` へ分離する。

分類は Extension Property Schema または custom parameter schema に従う。

## 17. update rate

update rate は、controller runtime が actuator 指令を更新する周期を表す。

単位は Hz または seconds とする。

使用単位は Extension Property Schema または custom parameter schema の `unit` に従う。

## 18. JSON構造案

初期段階の JSON 構造案は以下とする。

```json
{
  "schema_version": "0.1.0",
  "target": {
    "adapter": "SansaVRM-MuJoCo-Adapter",
    "mujoco_version": null
  },
  "actuators": [
    {
      "actuator_id": "left_knee_servo",
      "target_joint": "left_knee",
      "control_mode": "position",
      "runtime_control_mode": "position_pid",
      "parameters": {
        "command_delay_ms": 5,
        "deadband_rad": 0.01,
        "velocity_limit_rad_s": 10.0,
        "current_limit_a": 12.0
      },
      "diagnostics_ref": [],
      "conversion_report_ref": [],
      "source_extension_property_ref": []
    }
  ]
}
```

## 19. diagnosticsとの関係

`controller_config` へ分離した情報は、必要に応じて diagnostics に記録する。

以下の事象は diagnostics 記録対象とする。

- MJCF へ直接出力せず `controller_config` へ分離した
- runtime_requirements との分類境界により `controller_config` 対象外とした
- 必須パラメータが不足している
- parameter の単位が不明である
- Extension Property Schema と値が一致しない
- custom parameter schema と値が一致しない
- controller runtime が未対応である
- source_raw のみで schema_ref が存在しない

## 20. conversion_reportとの関係

conversion_report には、`controller_config` へ分離した件数、対象 actuator 数、fallback 適用数などの集計情報を記録する。

Extension Property の分類結果、adapter_artifact への出力件数、runtime_artifact への分離件数も conversion_report に記録してよい。

個別詳細は diagnostics に記録してよい。

## 21. updated_extension_propertiesとの関係

controller_config 生成時に、Adapter が新たな normalized_value、diagnostics_ref、conversion_report_ref を生成した場合、SansaVRM 側へ再格納する Extension Property 候補を `updated_extension_properties.json` に出力できる。

ただし、controller_config そのものを SansaVRM Core へ直接統合してはならない。

## 22. Git管理方針

以下は Git 管理対象とする。

- controller_config schema
- controller_config 仕様ドキュメント
- 小規模なテスト用 controller_config サンプル

以下は Git 管理対象外とする。

- ローカル実行で生成された `controller_config.local.json`
- 大量の検証結果
- 個別環境依存の controller_config

## 23. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- controller runtime の実装
- runtime_requirements schema の完全定義
- updated_extension_properties schema の完全定義
- 外部 PID の詳細アルゴリズム
- 熱シミュレーションの詳細実装
- FOC 制御の詳細実装
- ESC 制御の詳細実装
- UI 表示仕様

## 24. 関連ドキュメント

- [MJCF変換方針](./01_MJCF変換方針.md)
- [アクチュエータ写像](./02_アクチュエータ写像.md)
- [custom parameter mapping](./03_custom_parameter_mapping.md)
- [成果物仕様](../01_共通/03_成果物仕様.md)
- [diagnostics仕様](../01_共通/04_diagnostics仕様.md)
- [SansaVRM拡張プロパティ連携方針](../03_外部連携/01_SansaVRM拡張プロパティ連携方針.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > controller_config仕様
