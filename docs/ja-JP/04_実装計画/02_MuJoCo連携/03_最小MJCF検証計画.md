<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000025Z-SVMJ
lang: ja-JP
canonical_title: 最小MJCF検証計画
document_type: usage
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 実装計画 > MuJoCo連携 > 最小MJCF検証計画

# 最小MJCF検証計画

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter における最小 MJCF 検証の作業計画を定義する。

最小 MJCF 検証は、Adapter 実装前に MuJoCo 環境、MJCF サンプル、pytest テスト、diagnostics / test report の基礎を確認するために実施する。

## 2. 基本方針

最小 MJCF 検証では、SansaVRM 本体 API との連携を前提にしない。

初期段階では、手書きの MJCF サンプルを使用して以下を確認する。

- MJCF を MuJoCo で読み込める
- `MjModel` を生成できる
- `MjData` を生成できる
- `mj_step` を実行できる
- body / joint / geom / actuator / sensor の基本要素を段階的に確認できる

## 3. 対象ファイル

初期検証対象は以下とする。

```text
examples/mujoco/minimal_body/model.xml
```

段階的に追加する候補は以下とする。

```text
examples/mujoco/joint_body/model.xml
examples/mujoco/position_servo/model.xml
examples/mujoco/sensor_body/model.xml
```

## 4. 検証ステップ

最小 MJCF 検証は以下の順で実施する。

1. 最小 body / geom モデルの読み込み
2. joint 付きモデルの読み込み
3. position actuator 付きモデルの読み込み
4. sensor 付きモデルの読み込み
5. 各サンプルの pytest 化
6. diagnostics / test report への記録方針確認

## 5. Step 1: 最小body / geomモデル検証

### 5.1 目的

最小 body / geom を持つ MJCF が MuJoCo で読み込めることを確認する。

### 5.2 対象

```text
examples/mujoco/minimal_body/model.xml
```

### 5.3 対応テスト

- T-LOCAL-002
- T-LOCAL-003
- T-LOCAL-004
- T-LOCAL-005
- T-MJCF-001

### 5.4 完了条件

- `MjModel.from_xml_path` で読み込める
- `MjData` を生成できる
- `mj_step` を実行できる
- `nbody >= 1` である
- `ngeom >= 1` である

## 6. Step 2: joint付きモデル検証

### 6.1 目的

joint を持つ MJCF が MuJoCo で読み込めることを確認する。

### 6.2 追加予定ファイル

```text
examples/mujoco/joint_body/model.xml
```

### 6.3 対応テスト

- T-MJCF-002

### 6.4 完了条件

- `MjModel.from_xml_path` で読み込める
- `njnt >= 1` である
- `mj_step` を実行できる

## 7. Step 3: position actuator付きモデル検証

### 7.1 目的

position actuator を持つ MJCF が MuJoCo で読み込めることを確認する。

### 7.2 追加予定ファイル

```text
examples/mujoco/position_servo/model.xml
```

### 7.3 対応テスト

- T-MJCF-003
- T-ACTUATOR-001

### 7.4 完了条件

- `MjModel.from_xml_path` で読み込める
- `nu >= 1` である
- actuator が対象 joint を参照している
- `mj_step` を実行できる

## 8. Step 4: sensor付きモデル検証

### 8.1 目的

sensor を持つ MJCF が MuJoCo で読み込めることを確認する。

### 8.2 追加予定ファイル

```text
examples/mujoco/sensor_body/model.xml
```

### 8.3 対応テスト

- T-MJCF-004

### 8.4 完了条件

- `MjModel.from_xml_path` で読み込める
- `nsensor >= 1` である
- sensor が参照対象を持つ
- `mj_step` を実行できる

## 9. Step 5: pytest化

### 9.1 目的

最小 MJCF 検証を pytest で再現可能にする。

### 9.2 作業

以下を作成する。

```text
tests/mujoco/test_local_mujoco_environment.py
tests/mujoco/test_mjcf_loading.py
```

### 9.3 実装対象テスト

- T-LOCAL-001
- T-LOCAL-002
- T-LOCAL-003
- T-LOCAL-004
- T-LOCAL-005
- T-MJCF-001
- T-MJCF-002
- T-MJCF-003
- T-MJCF-004

未作成サンプルに依存するテストは、サンプル追加まで skip 扱いとする。

## 10. Step 6: diagnostics連携確認

### 10.1 目的

MJCF 読み込み失敗時の diagnostics 記録方針を確認する。

### 10.2 記録候補

以下を diagnostics に記録できるようにする。

- MJCF load failure
- invalid XML
- invalid MJCF element
- invalid MJCF attribute
- missing referenced joint
- missing referenced body
- unsupported MuJoCo version

### 10.3 完了条件

- 読み込み失敗を diagnostics の category / code / severity へ分類できる
- test report から diagnostics_ref を参照できる

## 11. Step 7: test report連携確認

### 11.1 目的

テスト結果を `test_report.local.json` へ記録する方針を確認する。

### 11.2 記録候補

以下を記録候補とする。

- test_id
- status
- input_file
- expected_counts
- actual_counts
- exception
- diagnostics_ref
- duration_ms

### 11.3 完了条件

- ローカル実行結果を JSON として保存できる
- `test_report.local.json` が Git 管理対象外である

## 12. Git管理方針

以下は Git 管理対象とする。

- 小規模な MJCF サンプル
- pytest テストコード
- fixture
- schema
- テスト仕様ドキュメント

以下は Git 管理対象外とする。

- `test_report.local.json`
- `diagnostics.local.json`
- `conversion_report.local.json`
- `controller_config.local.json`
- `*.mjb`
- ローカルログ

## 13. 失敗時の切り分け

最小 MJCF 検証で失敗した場合は、以下の順に確認する。

1. `mujoco` package を import できるか
2. 対象 MJCF ファイルが存在するか
3. XML として正しいか
4. MJCF として正しいか
5. 参照先 joint / body / site が存在するか
6. target MuJoCo version で対応している要素か
7. viewer ではなく headless で再現するか

## 14. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM 本体 API との連携検証
- MJCF writer の完全実装
- controller runtime の実装
- MuJoCo viewer 起動確認
- OS / GPU / OpenGL 互換性検証
- 実機サーボとの sysid 検証

## 15. 関連ドキュメント

- `04_実装計画/01_共通/01_初版実装ロードマップ.md`
- `04_実装計画/02_MuJoCo連携/01_ローカルMuJoCo環境構築.md`
- `04_実装計画/02_MuJoCo連携/02_ローカル動作確認手順.md`
- `03_テスト仕様/02_MuJoCo連携/01_ローカル動作確認テスト仕様.md`
- `03_テスト仕様/02_MuJoCo連携/02_MJCF読み込みテスト仕様.md`

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 実装計画 > MuJoCo連携 > 最小MJCF検証計画
