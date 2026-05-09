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

分離対象は、custom parameter schema の `io_scope` および `adapter_artifact` に基づいて判定する。

Adapter は、`controller_config` へ出力すべきかどうかを実装側の推測で判定してはならない。

## 3. 出力ファイル名

標準的な出力ファイル名は以下とする。

```text
controller_config.json
```

ローカル検証専用ファイルは以下の名称を使用できる。

```text
controller_config.local.json
```

`controller_config.local.json` は Git 管理対象外とする。

## 4. 対象情報

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

## 5. actuator設定

`controller_config` は、actuator 単位の設定を保持する。

actuator 設定は、少なくとも以下を持つ。

- actuator_id
- target_joint
- control_mode
- runtime_control_mode
- parameters
- diagnostics_ref

## 6. control_mode

`control_mode` は、SansaVRM 側または Adapter 側で扱う制御モードを表す。

初期候補は以下とする。

- `position`
- `velocity`
- `torque`
- `force`
- `external_controller`

## 7. runtime_control_mode

`runtime_control_mode` は、MuJoCo 実行時に Adapter runtime または外部 controller が使用する制御方式を表す。

初期候補は以下とする。

- `none`
- `position_pid`
- `velocity_pid`
- `torque_passthrough`
- `external`

## 8. command delay

command delay は、制御指令を遅延させるための設定である。

MJCF には直接出力しない。

`controller_config` では、以下のように記録する。

```json
{
  "command_delay_ms": 5
}
```

## 9. deadband

deadband は、制御誤差が一定範囲内にある場合の無反応領域を表す。

MJCF には直接出力しない。

`controller_config` では、以下のように記録する。

```json
{
  "deadband_rad": 0.01
}
```

## 10. velocity limit

velocity limit は、制御対象の最大速度を表す。

velocity actuator の `ctrlrange` へ直接写像できる場合は MJCF へ出力してよい。

position actuator の速度制限など、MJCF へ直接表現しにくい場合は `controller_config` へ分離する。

## 11. acceleration limit

acceleration limit は、制御対象の最大加速度を表す。

初期段階では MJCF へ直接出力しない。

`controller_config` へ分離する。

## 12. current limit / voltage limit

current limit と voltage limit は、原則として MJCF へ直接出力しない。

以下のいずれかとして扱う。

- torque limit 算出に使用する
- `controller_config` へ出力する
- preserve_only として保持する

算出に使用した場合は、conversion_report または diagnostics に記録する。

## 13. external PID configuration

外部 PID 設定は、MuJoCo runtime または Adapter runtime が制御入力を生成する場合に使用する。

初期候補は以下とする。

- kp
- ki
- kd
- integral_limit
- output_limit
- derivative_filter

MuJoCo の position actuator の `kp` / `kv` へ写像する場合と、外部 PID として扱う場合を混同してはならない。

## 14. thermal model settings

thermal model settings は、温度上昇、連続トルク、ピークトルク継続時間、温度保護などの情報を保持する。

初期段階では MJCF へ直接出力しない。

`controller_config` または将来の `runtime_config` へ分離する。

## 15. update rate

update rate は、controller runtime が actuator 指令を更新する周期を表す。

単位は Hz または seconds とする。

使用単位は custom parameter schema の `unit` に従う。

## 16. JSON構造案

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
      "diagnostics_ref": []
    }
  ]
}
```

## 17. diagnosticsとの関係

`controller_config` へ分離した情報は、必要に応じて diagnostics に記録する。

以下の事象は diagnostics 記録対象とする。

- MJCF へ直接出力せず `controller_config` へ分離した
- 必須パラメータが不足している
- parameter の単位が不明である
- custom parameter schema と値が一致しない
- controller runtime が未対応である

## 18. conversion_reportとの関係

conversion_report には、`controller_config` へ分離した件数、対象 actuator 数、fallback 適用数などの集計情報を記録する。

個別詳細は diagnostics に記録してよい。

## 19. Git管理方針

以下は Git 管理対象とする。

- controller_config schema
- controller_config 仕様ドキュメント
- 小規模なテスト用 controller_config サンプル

以下は Git 管理対象外とする。

- ローカル実行で生成された `controller_config.local.json`
- 大量の検証結果
- 個別環境依存の controller_config

## 20. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- controller runtime の実装
- 外部 PID の詳細アルゴリズム
- 熱シミュレーションの詳細実装
- FOC 制御の詳細実装
- ESC 制御の詳細実装
- UI 表示仕様

## 21. 関連ドキュメント

- [MJCF変換方針](./01_MJCF変換方針.md)
- [アクチュエータ写像](./02_アクチュエータ写像.md)
- [custom parameter mapping](./03_custom_parameter_mapping.md)
- [成果物仕様](../01_共通/03_成果物仕様.md)
- [diagnostics仕様](../01_共通/04_diagnostics仕様.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > controller_config仕様
