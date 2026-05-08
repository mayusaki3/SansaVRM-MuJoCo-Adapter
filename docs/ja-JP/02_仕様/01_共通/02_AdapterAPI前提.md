<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000009Z-SVMJ
lang: ja-JP
canonical_title: AdapterAPI前提
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 共通 > AdapterAPI前提

# AdapterAPI前提

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter が SansaVRM 本体と連携する際に前提とする Adapter API の考え方を定義する。

本仕様では、具体的な SansaVRM Core API の実装詳細ではなく、SansaVRM-MuJoCo-Adapter 側が必要とする入出力境界、取得対象、記録対象、検証対象を定義する。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、SansaVRM 本体の内部データ構造へ直接依存してはならない。

Adapter は、SansaVRM 本体が提供する安定した公開 API または同等の抽象化層を経由して情報を取得する。

SansaVRM 本体 API の名称、引数、戻り値の詳細は SansaVRM 本体仕様に従う。

## 3. 読み取り対象

Adapter は、SansaVRM 本体 API から以下の情報を取得できることを前提とする。

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

## 4. 書き込み対象

Adapter は、変換または検証の結果として、以下の情報を SansaVRM 本体側へ返却または記録できることを前提とする。

- diagnostics
- conversion report
- fallback result
- unsupported parameter information
- non-reversible conversion information
- generated artifact metadata

## 5. 検証対象

Adapter は、SansaVRM 本体または共通検証層により、以下の検証を実行できることを前提とする。

- 共通物理情報の妥当性検証
- Adapter 固有パラメータの妥当性検証
- custom parameter schema の妥当性検証
- 必須パラメータの存在検証
- 対象 MuJoCo バージョンに対する対応可否検証
- MJCF 入出力可否の検証
- Adapter 側補助成果物への分離可否検証

## 6. Adapter API境界

Adapter API 境界は、SansaVRM 本体と SansaVRM-MuJoCo-Adapter の責務境界である。

SansaVRM 本体は、共通モデル情報と schema を保持する。

SansaVRM-MuJoCo-Adapter は、API から取得した情報をもとに、MuJoCo 固有の変換、近似、補助成果物生成、検証を行う。

## 7. MJCF出力対象の判定

MJCF へ直接出力できる情報は、custom parameter schema に定義された `io_scope` と `mjcf_mapping` に基づいて判定する。

Adapter は、MJCF へ直接出力できるかどうかを実装側の推測で判定してはならない。

`io_scope = mjcf` または `io_scope = both` の情報は、`mjcf_mapping` に従って MJCF へ出力する。

## 8. Adapter補助成果物対象の判定

MJCF へ直接出力しない情報は、custom parameter schema に定義された `io_scope` と `adapter_artifact` に基づいて判定する。

`io_scope = adapter_artifact` または `io_scope = both` の情報は、`adapter_artifact` に従って controller_config などの Adapter 側補助成果物へ出力する。

## 9. diagnostics連携

Adapter は、以下の事象を diagnostics として記録する。

- 必須情報の不足
- schema 不整合
- MuJoCo バージョン非対応
- MJCF へ出力できない情報
- Adapter 側補助成果物へ分離した情報
- fallback を適用した情報
- 非可逆変換となった情報

## 10. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- SansaVRM Core API の詳細な関数シグネチャ
- SansaVRM 本体の内部データ構造
- MuJoCo runtime の実装
- MJCF XML 生成アルゴリズムの詳細
- controller_config の具体的 schema

## 11. 関連ドキュメント

- `01_要件定義/01_基本要件/03_責務境界.md`
- `02_仕様/01_共通/01_仕様概要.md`

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 共通 > AdapterAPI前提
