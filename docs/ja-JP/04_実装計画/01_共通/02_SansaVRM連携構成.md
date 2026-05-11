<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260511-000001Z-SVMJ
lang: ja-JP
canonical_title: SansaVRM連携構成
document_type: usage
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 実装計画 > 共通 > SansaVRM連携構成

# SansaVRM連携構成

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter を SansaVRM の Rust モジュールと組み合わせて使用する際の構成方針を定義する。

本ドキュメントでは、開発用構成と利用用構成を分け、Adapter 単体開発、SansaVRM Rust モジュール連携、MuJoCo 成果物生成、Project Meridian / meridian-mujoco-runtime への接続の想定を整理する。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、SansaVRM Core の内部実装へ直接依存してはならない。

Adapter は、SansaVRM Rust モジュールが提供する公開 API、CLI、または中間 JSON 成果物を通じて SansaVRM Core 標準構造と Extension Property を受け取る。

SansaVRM-MuJoCo-Adapter は Python 実装を初期想定とする。

SansaVRM 側は Rust 実装を初期想定とする。

Rust と Python を直接密結合させず、初期段階では JSON ベースの中間成果物連携を優先する。

## 3. 全体構成

想定する全体構成は以下とする。

```text
SansaVRM Rust module
  ↓ export / API / CLI
SansaVRM Core + Extension Property JSON
  ↓ input
SansaVRM-MuJoCo-Adapter
  ↓ output
model.xml
controller_config.json
runtime_requirements.json
updated_extension_properties.json
diagnostics.json
conversion_report.json
  ↓ optional
meridian-mujoco-runtime
```

## 4. 開発用構成

開発用構成は、SansaVRM 本体が未完成または変更中でも Adapter 側の検証を進められるようにするための構成である。

開発用構成では、SansaVRM Rust モジュールの実 API へ必ずしも接続しない。

初期段階では、fixture または中間 JSON を使用する。

```text
fixtures / mock_sansavrm_export.json
  ↓
SansaVRM-MuJoCo-Adapter
  ↓
MuJoCo artifacts
```

## 5. 開発用構成の目的

開発用構成の目的は以下とする。

- Adapter 単体の schema 検証を可能にする
- MJCF 生成処理を SansaVRM 本体完成前に検証する
- controller_config 生成を fixture ベースで検証する
- runtime_requirements 生成を fixture ベースで検証する
- updated_extension_properties 生成を fixture ベースで検証する
- diagnostics / conversion_report を再現可能に検証する
- CI で SansaVRM 本体に依存しない headless テストを実行する

## 6. 開発用入力

開発用入力は以下を想定する。

- SansaVRM export fixture
- Extension Property fixture
- custom parameter fixture
- actuator fixture
- controller_config fixture
- runtime_requirements fixture
- updated_extension_properties fixture

配置候補は以下とする。

```text
tests/fixtures/sansavrm_export/
tests/fixtures/extension_property/
tests/fixtures/actuator/
tests/fixtures/controller_config/
tests/fixtures/runtime_requirements/
tests/fixtures/updated_extension_properties/
```

## 7. 開発用出力

開発用出力は以下を想定する。

```text
output/
├─ model.xml
├─ controller_config.json
├─ runtime_requirements.json
├─ updated_extension_properties.json
├─ diagnostics.json
└─ conversion_report.json
```

`output/` 配下はローカル生成物であり、Git 管理対象外とする。

## 8. 利用用構成

利用用構成は、実際の SansaVRM Rust モジュールと SansaVRM-MuJoCo-Adapter を組み合わせて利用する構成である。

利用用構成では、SansaVRM Rust モジュールが SansaVRM Core 標準構造と Extension Property を出力し、Adapter がそれを入力として扱う。

```text
SansaVRM file / model package
  ↓
SansaVRM Rust module
  ↓ export
SansaVRM Adapter Input JSON
  ↓
SansaVRM-MuJoCo-Adapter
  ↓
MuJoCo artifacts
```

## 9. 利用用入力境界

利用用入力境界は、SansaVRM Rust モジュールが出力する Adapter 入力用 JSON とする。

初期候補名は以下とする。

```text
sansavrm_adapter_input.json
```

` sansavrm_adapter_input.json` には、少なくとも以下を含める。

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
- extension_properties
- extension_property_schemas
- custom_parameters
- custom_parameter_schemas

## 10. 利用用出力境界

利用用出力境界は、Adapter が生成する成果物一式とする。

標準成果物は以下とする。

```text
model.xml
controller_config.json
runtime_requirements.json
updated_extension_properties.json
diagnostics.json
conversion_report.json
```

SansaVRM Rust モジュールは、必要に応じて `updated_extension_properties.json` を読み込み、SansaVRM Extension Property として再格納する。

## 11. Rust / Python 連携方式

初期段階の Rust / Python 連携方式は、ファイルベース連携を優先する。

### 11.1 推奨: JSONファイル連携

```text
SansaVRM Rust module
  ↓ writes sansavrm_adapter_input.json
SansaVRM-MuJoCo-Adapter Python CLI
  ↓ reads sansavrm_adapter_input.json
Adapter outputs
```

利点は以下とする。

- Rust と Python の実装境界を明確にできる
- CI で fixture を使いやすい
- SansaVRM 本体 API の変更影響を抑えられる
- 中間成果物を保存して再現検証できる

### 11.2 将来候補: CLI連携

SansaVRM Rust モジュールと Adapter を CLI で連携する構成を将来候補とする。

```powershell
sansavrm export-adapter-input --input robot.sansavrm --output sansavrm_adapter_input.json
python -m sansavrm_mujoco_adapter convert --input sansavrm_adapter_input.json --output output/
sansavrm import-extension-properties --input robot.sansavrm --extension-properties output/updated_extension_properties.json
```

### 11.3 将来候補: FFI / Python binding

Rust と Python の直接連携は将来候補とする。

初期段階では、PyO3、maturin、C ABI、gRPC などの直接連携方式は必須にしない。

直接連携方式は、Adapter API と中間 JSON schema が安定した後に検討する。

## 12. 開発用手順

開発者は、以下の順で作業する。

1. SansaVRM-MuJoCo-Adapter リポジトリを取得する
2. Python 仮想環境を作成する
3. `requirements-dev.txt` をインストールする
4. fixture を使用して schema 検証を実行する
5. fixture を使用して Adapter 変換処理を実行する
6. 生成された MJCF を MuJoCo で読み込む
7. `pytest` を実行する
8. coverage を確認する

初期段階では、SansaVRM Rust モジュールを必須依存にしない。

## 13. 利用用手順

利用者は、以下の順で使用する想定とする。

1. SansaVRM Rust モジュールで SansaVRM モデルを読み込む
2. Adapter 入力用 JSON を出力する
3. SansaVRM-MuJoCo-Adapter で Adapter 入力用 JSON を読み込む
4. MuJoCo 向け成果物を生成する
5. diagnostics / conversion_report を確認する
6. 必要に応じて updated_extension_properties を SansaVRM 側へ再格納する
7. model.xml / controller_config.json / runtime_requirements.json を meridian-mujoco-runtime へ渡す

## 14. Project Meridianとの接続

Project Meridian / meridian-mujoco-runtime は、Adapter の利用用出力を入力として扱う。

想定入力は以下とする。

- model.xml
- controller_config.json
- runtime_requirements.json

meridian-mujoco-runtime の sysid、HIL / SIL、実ボード同期結果を SansaVRM 側へ戻す場合は、updated_extension_properties.json を経由する。

## 15. nisocon-vr-battle-runtimeとの関係

SansaVRM-MuJoCo-Adapter は、nisocon-vr-battle-runtime と直接結合しない。

nisocon-vr-battle-runtime は、meridian-mujoco-runtime の抽象 API を通じて MuJoCo 実行結果を利用する。

## 16. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM Rust モジュールの内部設計
- SansaVRM Core schema の完全定義
- Extension Property Schema の完全定義
- PyO3 / FFI / gRPC 実装
- meridian-mujoco-runtime の実装
- nisocon-vr-battle-runtime の実装

## 17. 関連ドキュメント

- [開発環境構築](./00_開発環境構築.md)
- [初版実装ロードマップ](./01_初版実装ロードマップ.md)
- [AdapterAPI前提](../../02_仕様/01_共通/02_AdapterAPI前提.md)
- [成果物仕様](../../02_仕様/01_共通/03_成果物仕様.md)
- [SansaVRM拡張プロパティ連携方針](../../02_仕様/03_外部連携/01_SansaVRM拡張プロパティ連携方針.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 実装計画 > 共通 > SansaVRM連携構成
