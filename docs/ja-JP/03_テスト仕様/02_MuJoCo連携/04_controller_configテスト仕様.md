<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000022Z-SVMJ
lang: ja-JP
canonical_title: controller_configテスト仕様
document_type: testspec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > テスト仕様 > MuJoCo連携 > controller_configテスト仕様

# controller_configテスト仕様

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter における controller_config 生成のテスト仕様を定義する。

本テスト仕様は、MJCF に直接出力しない制御・実行補助情報を controller_config へ正しく分離・出力できることを確認するために使用する。

## 2. 基本方針

controller_config テストでは、以下を確認する。

- controller_config を生成できる
- actuator 単位の設定を出力できる
- command delay を出力できる
- deadband を出力できる
- current limit / voltage limit を出力できる
- diagnostics_ref を保持できる
- MJCF へ直接出力しない情報を controller_config に分離できる

## 3. 前提条件

以下が完了していること。

- controller_config 仕様が定義されている
- custom parameter mapping 仕様が定義されている
- アクチュエータ写像仕様が定義されている
- diagnostics 仕様が定義されている
- テスト結果レポート仕様が定義されている

## 4. テスト対象

テスト対象は以下とする。

- controller_config JSON 生成
- actuator 設定出力
- command delay 出力
- deadband 出力
- velocity limit 出力
- current limit 出力
- voltage limit 出力
- diagnostics_ref 出力
- schema_version 出力
- target 情報出力

## 5. テスト一覧

| テスト番号 | テスト名 | 目的 |
| --- | --- | --- |
| T-CONTROLLERCONFIG-001 | controller_config生成 | controller_config を生成できることを確認する |
| T-CONTROLLERCONFIG-002 | actuator設定出力 | actuator 単位の設定を出力できることを確認する |
| T-CONTROLLERCONFIG-003 | command_delay出力 | command_delay を出力できることを確認する |
| T-CONTROLLERCONFIG-004 | deadband出力 | deadband を出力できることを確認する |
| T-CONTROLLERCONFIG-005 | diagnostics参照保持 | diagnostics_ref を保持できることを確認する |
| T-CONTROLLERCONFIG-006 | current_limit出力 | current_limit を出力できることを確認する |
| T-CONTROLLERCONFIG-007 | voltage_limit出力 | voltage_limit を出力できることを確認する |

## 6. T-CONTROLLERCONFIG-001: controller_config生成

### 6.1 目的

controller_config JSON を生成できることを確認する。

### 6.2 入力

controller_config 出力対象を含む fixture を入力とする。

初期 fixture 候補：

```text
tests/fixtures/controller_config/minimal_controller_config.json
```

### 6.3 期待結果

- controller_config JSON が生成される
- `schema_version` が出力される
- `target` が出力される
- `actuators` が配列として出力される
- JSON として読み込める

### 6.4 diagnostics期待結果

通常成功時は error / fatal を出力しない。

## 7. T-CONTROLLERCONFIG-002: actuator設定出力

### 7.1 目的

actuator 単位の設定を controller_config へ出力できることを確認する。

### 7.2 入力

actuator 設定を含む fixture を入力とする。

### 7.3 期待結果

- `actuators[]` に actuator 設定が出力される
- `actuator_id` が出力される
- `target_joint` が出力される
- `control_mode` が出力される
- `runtime_control_mode` が出力される
- `parameters` が出力される

### 7.4 diagnostics期待結果

必須項目が不足している場合は diagnostics に記録する。

## 8. T-CONTROLLERCONFIG-003: command_delay出力

### 8.1 目的

command delay を controller_config へ出力できることを確認する。

### 8.2 入力

command delay を持つ actuator fixture を入力とする。

### 8.3 期待結果

- `parameters.command_delay_ms` が出力される
- MJCF へ command delay 相当の独自属性を出力しない
- command delay の出力先は custom parameter schema の `adapter_artifact` に従う

### 8.4 diagnostics期待結果

command delay を controller_config へ分離したことを info として記録してよい。

## 9. T-CONTROLLERCONFIG-004: deadband出力

### 9.1 目的

deadband を controller_config へ出力できることを確認する。

### 9.2 入力

deadband を持つ actuator fixture を入力とする。

### 9.3 期待結果

- `parameters.deadband_rad` または schema で定義された deadband 項目が出力される
- MJCF へ deadband 相当の独自属性を出力しない
- deadband の出力先は custom parameter schema の `adapter_artifact` に従う

### 9.4 diagnostics期待結果

deadband を controller_config へ分離したことを info として記録してよい。

## 10. T-CONTROLLERCONFIG-005: diagnostics参照保持

### 10.1 目的

controller_config の actuator 設定から diagnostics を参照できることを確認する。

### 10.2 入力

diagnostics を伴う controller_config 出力 fixture を入力とする。

### 10.3 期待結果

- actuator 設定に `diagnostics_ref` が出力される
- `diagnostics_ref` は配列である
- diagnostics が存在しない場合は空配列を許容する
- diagnostics が存在する場合は diagnostic_id を保持する

### 10.4 diagnostics期待結果

参照先 diagnostics が存在しない場合は warning または error として記録する。

## 11. T-CONTROLLERCONFIG-006: current_limit出力

### 11.1 目的

current limit を controller_config へ出力できることを確認する。

### 11.2 入力

current limit を持つ actuator fixture を入力とする。

### 11.3 期待結果

- `parameters.current_limit_a` または schema で定義された current limit 項目が出力される
- torque limit 算出に使用した場合は conversion_report または diagnostics に記録される
- MJCF へ直接出力しない場合は controller_config へ分離される

### 11.4 diagnostics期待結果

以下を diagnostics に記録できる。

- current limit を controller_config へ分離した
- current limit を torque limit 算出に使用した
- current limit の単位が不明である

## 12. T-CONTROLLERCONFIG-007: voltage_limit出力

### 12.1 目的

voltage limit を controller_config へ出力できることを確認する。

### 12.2 入力

voltage limit を持つ actuator fixture を入力とする。

### 12.3 期待結果

- `parameters.voltage_limit_v` または schema で定義された voltage limit 項目が出力される
- MJCF へ直接出力しない場合は controller_config へ分離される
- custom parameter schema の `adapter_artifact` に従う

### 12.4 diagnostics期待結果

以下を diagnostics に記録できる。

- voltage limit を controller_config へ分離した
- voltage limit の単位が不明である

## 13. JSON構造検証

controller_config は JSON として読み込めなければならない。

将来的に schema を定義した場合、schema validation を行う。

初期段階では、最低限以下を確認する。

- root が object である
- `schema_version` が存在する
- `target` が存在する
- `actuators` が存在する
- `actuators` が array である

## 14. pytest化方針

本テスト仕様は、将来的に `pytest` により自動化する。

初期配置候補は以下とする。

```text
tests/mujoco/test_controller_config.py
```

pytest 実装時は、各テスト番号と test 関数を対応付ける。

例：

```text
T-CONTROLLERCONFIG-001 -> test_t_controllerconfig_001_generate_controller_config
T-CONTROLLERCONFIG-003 -> test_t_controllerconfig_003_output_command_delay
```

## 15. テスト結果レポートへの記録

テスト結果は、必要に応じて `test_report.local.json` に記録する。

記録対象は以下とする。

- test_id
- status
- input_fixture
- generated_controller_config_path
- expected
- actual
- diagnostics_ref
- conversion_report_ref

## 16. diagnosticsとの関係

controller_config テストで失敗または分離が発生した場合、diagnostics に以下を記録してよい。

- controller_config generation failure
- missing actuator_id
- missing target_joint
- invalid control_mode
- invalid runtime_control_mode
- invalid parameter unit
- diagnostics_ref mismatch
- adapter_artifact mapping missing

## 17. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- controller runtime の実装検証
- 外部 PID の挙動検証
- 熱シミュレーションの挙動検証
- MuJoCo runtime と controller_config の統合実行検証
- UI 表示仕様

## 18. 関連ドキュメント

- [controller_config仕様](../../02_仕様/02_MuJoCo連携/04_controller_config仕様.md)
- [custom parameter mapping](../../02_仕様/02_MuJoCo連携/03_custom_parameter_mapping.md)
- [アクチュエータ写像](../../02_仕様/02_MuJoCo連携/02_アクチュエータ写像.md)
- [テスト方針](../01_共通/01_テスト方針.md)
- [テスト結果レポート仕様](../01_共通/02_テスト結果レポート仕様.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > テスト仕様 > MuJoCo連携 > controller_configテスト仕様
