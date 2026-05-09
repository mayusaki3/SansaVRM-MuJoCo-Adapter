<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000020Z-SVMJ
lang: ja-JP
canonical_title: MJCF読み込みテスト仕様
document_type: testspec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > テスト仕様 > MuJoCo連携 > MJCF読み込みテスト仕様

# MJCF読み込みテスト仕様

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter が扱う MJCF ファイルを MuJoCo で読み込めることを確認するためのテスト仕様を定義する。

MJCF 読み込みテストは、MJCF 生成処理、サンプルモデル、将来の変換テストの前提として使用する。

## 2. 基本方針

MJCF 読み込みテストは、headless 実行を基本とする。

MuJoCo viewer の起動確認は本テストの必須条件に含めない。

テスト対象 MJCF は、MuJoCo の `MjModel.from_xml_path` で読み込める必要がある。

## 3. 前提条件

以下が完了していること。

- ローカル MuJoCo 環境が構築されている
- `mujoco` package を import できる
- 対象 MJCF ファイルが存在する
- リポジトリ直下でテストを実行する

## 4. 対象ファイル

初期対象は以下とする。

```text
examples/mujoco/minimal_body/model.xml
```

将来追加する対象候補は以下とする。

```text
examples/mujoco/joint_body/model.xml
examples/mujoco/position_servo/model.xml
examples/mujoco/sensor_body/model.xml
```

## 5. テスト一覧

| テスト番号 | テスト名 | 目的 |
| --- | --- | --- |
| T-MJCF-001 | 最小bodyモデル読み込み | 最小 body / geom を持つ MJCF を読み込めることを確認する |
| T-MJCF-002 | joint付きモデル読み込み | joint を持つ MJCF を読み込めることを確認する |
| T-MJCF-003 | actuator付きモデル読み込み | actuator を持つ MJCF を読み込めることを確認する |
| T-MJCF-004 | sensor付きモデル読み込み | sensor を持つ MJCF を読み込めることを確認する |

## 6. T-MJCF-001: 最小bodyモデル読み込み

### 6.1 目的

最小 body / geom を持つ MJCF を MuJoCo で読み込めることを確認する。

### 6.2 入力

```text
examples/mujoco/minimal_body/model.xml
```

### 6.3 実行内容

```powershell
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('examples/mujoco/minimal_body/model.xml'); print('ok', m.nbody, m.ngeom)"
```

### 6.4 期待結果

- 終了コードが 0 である
- `MjModel.from_xml_path` が例外を出さない
- `nbody >= 1` である
- `ngeom >= 1` である

### 6.5 失敗時の扱い

失敗した場合は、MJCF ファイル不正または MuJoCo 実行環境不備として扱う。

## 7. T-MJCF-002: joint付きモデル読み込み

### 7.1 目的

joint を持つ MJCF を MuJoCo で読み込めることを確認する。

### 7.2 入力

```text
examples/mujoco/joint_body/model.xml
```

### 7.3 実行内容

```powershell
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('examples/mujoco/joint_body/model.xml'); print('ok', m.nbody, m.njnt, m.ngeom)"
```

### 7.4 期待結果

- 終了コードが 0 である
- `MjModel.from_xml_path` が例外を出さない
- `njnt >= 1` である

### 7.5 失敗時の扱い

失敗した場合は、joint 定義または MJCF 構造不備として扱う。

### 7.6 初期状態

本テストは、対象サンプル `examples/mujoco/joint_body/model.xml` を追加後に有効化する。

## 8. T-MJCF-003: actuator付きモデル読み込み

### 8.1 目的

actuator を持つ MJCF を MuJoCo で読み込めることを確認する。

### 8.2 入力

```text
examples/mujoco/position_servo/model.xml
```

### 8.3 実行内容

```powershell
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('examples/mujoco/position_servo/model.xml'); print('ok', m.nu)"
```

### 8.4 期待結果

- 終了コードが 0 である
- `MjModel.from_xml_path` が例外を出さない
- `nu >= 1` である

### 8.5 失敗時の扱い

失敗した場合は、actuator 定義または対象 joint 参照不備として扱う。

### 8.6 初期状態

本テストは、対象サンプル `examples/mujoco/position_servo/model.xml` を追加後に有効化する。

## 9. T-MJCF-004: sensor付きモデル読み込み

### 9.1 目的

sensor を持つ MJCF を MuJoCo で読み込めることを確認する。

### 9.2 入力

```text
examples/mujoco/sensor_body/model.xml
```

### 9.3 実行内容

```powershell
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('examples/mujoco/sensor_body/model.xml'); print('ok', m.nsensor)"
```

### 9.4 期待結果

- 終了コードが 0 である
- `MjModel.from_xml_path` が例外を出さない
- `nsensor >= 1` である

### 9.5 失敗時の扱い

失敗した場合は、sensor 定義または参照対象不備として扱う。

### 9.6 初期状態

本テストは、対象サンプル `examples/mujoco/sensor_body/model.xml` を追加後に有効化する。

## 10. pytest化方針

本テスト仕様は、将来的に `pytest` により自動化する。

初期配置候補は以下とする。

```text
tests/mujoco/test_mjcf_loading.py
```

pytest 実装時は、各テスト番号と test 関数を対応付ける。

例：

```text
T-MJCF-001 -> test_t_mjcf_001_load_minimal_body
T-MJCF-002 -> test_t_mjcf_002_load_joint_body
```

未追加サンプルに依存するテストは、サンプル追加まで skip 扱いとする。

## 11. テスト結果レポートへの記録

テスト結果は、必要に応じて `test_report.local.json` に記録する。

記録対象は以下とする。

- test_id
- status
- input_file
- expected_counts
- actual_counts
- exception
- diagnostics_ref

## 12. diagnosticsとの関係

MJCF 読み込みで失敗した場合、diagnostics に以下を記録してよい。

- MJCF load failure
- invalid XML
- invalid MJCF element
- invalid MJCF attribute
- missing referenced joint
- missing referenced body
- unsupported MuJoCo version

## 13. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM から MJCF への変換ロジック検証
- actuator 写像ロジック検証
- controller_config 生成検証
- MuJoCo viewer 起動確認
- OS / GPU / OpenGL 互換性テスト

## 14. 関連ドキュメント

- [テスト方針](../01_共通/01_テスト方針.md)
- [ローカル動作確認テスト仕様](./01_ローカル動作確認テスト仕様.md)
- [MJCF変換方針](../../02_仕様/02_MuJoCo連携/01_MJCF変換方針.md)
- [ローカルMuJoCo環境構築](../../04_実装計画/02_MuJoCo連携/01_ローカルMuJoCo環境構築.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > テスト仕様 > MuJoCo連携 > MJCF読み込みテスト仕様
