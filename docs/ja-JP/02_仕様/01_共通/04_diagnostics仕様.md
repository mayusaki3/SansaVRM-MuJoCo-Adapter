<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000011Z-SVMJ
lang: ja-JP
canonical_title: diagnostics仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 共通 > diagnostics仕様

# diagnostics仕様

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter が生成する diagnostics の目的、記録対象、分類、出力方針を定義する。

diagnostics は、変換、検証、実行前確認で検出した警告・エラー・補足情報を記録し、SansaVRM 本体または利用者が変換結果を判断できるようにするための成果物である。

## 2. 基本方針

SansaVRM-MuJoCo-Adapter は、以下の事象を diagnostics として記録する。

- 必須情報の不足
- schema 不整合
- MuJoCo バージョン非対応
- MJCF へ直接出力できない情報
- Adapter 側補助成果物へ分離した情報
- fallback を適用した情報
- 非可逆変換となった情報
- 未対応パラメータ
- 変換対象外と判断した情報

## 3. diagnosticsの役割

diagnostics は、以下の役割を持つ。

- 変換処理の警告・エラーを記録する
- 変換時の判断理由を記録する
- MJCF に入らなかった情報の扱いを記録する
- controller_config などの補助成果物へ分離した情報を記録する
- fallback 適用の有無を記録する
- 非可逆変換情報を記録する
- SansaVRM 本体へ返却する診断情報の基礎とする

## 4. 出力形式

初期段階では、diagnostics は JSON 形式で出力する。

標準的な出力名は以下とする。

```text
diagnostics.json
```

ローカル専用の diagnostics は以下の名称を使用できる。

```text
diagnostics.local.json
```

`diagnostics.local.json` は Git 管理対象外とする。

## 5. 記録単位

diagnostics は、診断項目単位で記録する。

1つの診断項目は、少なくとも以下の情報を持つ。

- diagnostic_id
- severity
- category
- code
- message
- target_type
- target_id
- source
- detail

## 6. severity

severity は、診断項目の重大度を表す。

severity は以下のいずれかとする。

- `info`
- `warning`
- `error`
- `fatal`

### 6.1 info

`info` は、処理上の補足情報を示す。

例：

- Adapter 側補助成果物へ情報を分離した
- fallback を使用せず既定変換を行った

### 6.2 warning

`warning` は、変換結果は生成できるが注意が必要な状態を示す。

例：

- 一部の情報が MJCF へ直接出力されず controller_config へ分離された
- 非可逆変換が発生した
- fallback が適用された

### 6.3 error

`error` は、対象項目の変換または検証に失敗した状態を示す。

例：

- 必須パラメータが不足している
- custom parameter schema と値が一致しない
- 対象 MuJoCo バージョンで未対応のパラメータが使用されている

### 6.4 fatal

`fatal` は、変換処理全体を継続できない状態を示す。

例：

- 入力モデルを読み込めない
- Adapter が必要とする API 応答を取得できない
- 出力先へ成果物を書き込めない

## 7. category

category は、診断項目の分類を表す。

category は以下のいずれかを初期候補とする。

- `input`
- `schema`
- `mapping`
- `mjcf`
- `adapter_artifact`
- `version`
- `fallback`
- `non_reversible`
- `unsupported`
- `output`
- `runtime`

## 8. code

code は、診断項目を機械的に識別するためのコードである。

code は、以下の形式を基本とする。

```text
D-<CATEGORY>-<NUMBER>
```

例：

```text
D-SCHEMA-001
D-MJCF-001
D-FALLBACK-001
D-UNSUPPORTED-001
```

## 9. target_type

target_type は、診断対象の種類を表す。

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
- custom_parameter
- custom_parameter_schema
- artifact

## 10. target_id

target_id は、診断対象を識別する ID である。

対象 ID が存在しない場合、またはモデル全体に関する診断である場合は `null` を許容する。

## 11. source

source は、診断項目の発生元を表す。

初期候補は以下とする。

- sansavrm_api
- adapter
- mjcf_writer
- controller_config_writer
- conversion_report_writer
- diagnostics_writer
- mujoco_loader
- local_validation

## 12. detail

detail は、診断項目の補足情報を保持する。

detail の内容は診断項目により異なる。

例：

```json
{
  "expected": "number",
  "actual": "string",
  "parameter": "torque_limit_nm"
}
```

## 13. 出力例

```json
{
  "diagnostics": [
    {
      "diagnostic_id": "diag-000001",
      "severity": "warning",
      "category": "adapter_artifact",
      "code": "D-ADAPTER-001",
      "message": "command_delay_ms は MJCF に直接出力せず controller_config へ分離しました。",
      "target_type": "actuator",
      "target_id": "left_knee_servo",
      "source": "controller_config_writer",
      "detail": {
        "parameter": "command_delay_ms",
        "artifact": "controller_config.json"
      }
    }
  ]
}
```

## 14. conversion_reportとの関係

conversion_report は変換結果の概要を記録する。

diagnostics は個別の警告・エラー・補足情報を記録する。

同一の事象について、conversion_report には集計情報を記録し、diagnostics には詳細情報を記録してよい。

## 15. SansaVRM本体への返却

Adapter は、diagnostics を SansaVRM 本体側へ返却または記録できる。

SansaVRM 本体側で diagnostics を保持する場合、Adapter 側 diagnostics の内容を失ってはならない。

ただし、表示用の要約や severity によるフィルタリングは許容する。

## 16. Git管理方針

以下は Git 管理対象とする。

- diagnostics schema
- diagnostics 仕様ドキュメント
- 小規模なテスト用 diagnostics サンプル

以下は Git 管理対象外とする。

- ローカル実行で生成された `diagnostics.local.json`
- ローカルログ
- 大量の検証結果

## 17. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- diagnostics schema の完全定義
- UI 表示仕様
- SansaVRM 本体側 diagnostics 表示仕様
- MuJoCo runtime のエラー体系全体の再定義

## 18. 関連ドキュメント

- `02_仕様/01_共通/01_仕様概要.md`
- `02_仕様/01_共通/02_AdapterAPI前提.md`
- `02_仕様/01_共通/03_成果物仕様.md`

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > 共通 > diagnostics仕様
