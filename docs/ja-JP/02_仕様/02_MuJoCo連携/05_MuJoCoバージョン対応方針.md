<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260508-000016Z-SVMJ
lang: ja-JP
canonical_title: MuJoCoバージョン対応方針
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > MuJoCoバージョン対応方針

# MuJoCoバージョン対応方針

## 1. 本ドキュメントの目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter における MuJoCo バージョン対応方針を定義する。

MuJoCo の要素、属性、既定値、推奨設定、Python API、viewer、runtime 挙動はバージョンにより変化する可能性がある。

本仕様は、MuJoCo バージョン差分に対して、Adapter がどのように対応可否を判定し、diagnostics、conversion_report、custom parameter mapping に反映するかを定義する。

## 2. 基本方針

Adapter は、対象 MuJoCo バージョンを明示的に扱う。

Adapter は、MuJoCo バージョンに依存する mapping、schema、fallback、diagnostics を実装側の推測で処理してはならない。

MuJoCo バージョン依存の判定は、custom parameter schema、adapter capability、または明示的な version policy に基づいて行う。

## 3. 対象バージョン

初期段階では、PyPI package `mujoco` により導入される MuJoCo を対象とする。

初期の最小対応方針は以下とする。

- Python package `mujoco` を使用する
- local validation では installed version を取得する
- target MuJoCo version が未指定の場合は installed version を使用する
- schema に required version がある場合は installed version と照合する

## 4. バージョン取得

Adapter は、可能な場合、実行環境の MuJoCo バージョンを取得する。

Python binding を使用する場合、以下のような取得を想定する。

```python
import mujoco

print(mujoco.__version__)
```

取得したバージョンは、conversion_report または diagnostics に記録できる。

## 5. target MuJoCo version

Adapter は、変換対象の MuJoCo バージョンを target MuJoCo version として扱う。

target MuJoCo version は、以下のいずれかで指定できることを想定する。

- Adapter 実行オプション
- controller_config
- custom parameter schema
- local validation 設定
- installed MuJoCo version

指定が競合する場合は、明示的に指定された target MuJoCo version を優先する。

## 6. custom parameter schemaとの関係

custom parameter schema は、MuJoCo バージョンに関する情報を保持できる。

初期候補は以下とする。

- mujoco_version
- supported_since
- deprecated_since
- required_mujoco_version

Adapter は、対象 parameter が target MuJoCo version で使用可能かを schema に基づいて判定する。

## 7. required_mujoco_version

`required_mujoco_version` は、特定の mapping を使用できる MuJoCo バージョン範囲を定義する。

例：

```json
{
  "required_mujoco_version": {
    "min": "2.3.0",
    "max": null
  }
}
```

Adapter は、target MuJoCo version がこの範囲を満たさない場合、その mapping を使用してはならない。

## 8. supported_since

`supported_since` は、parameter または mapping が対応開始した MuJoCo バージョンを示す。

対象バージョンが `supported_since` より古い場合、Adapter は diagnostics に記録する。

必要に応じて fallback 方針に従う。

## 9. deprecated_since

`deprecated_since` は、parameter または mapping が非推奨となった MuJoCo バージョンを示す。

対象バージョンが `deprecated_since` 以降の場合、Adapter は warning として diagnostics に記録する。

非推奨項目でも変換可能な場合は、conversion_report に記録したうえで出力してよい。

ただし、schema または version policy で `error` とされている場合は、変換を失敗扱いにする。

## 10. mapping選択方針

同一 parameter に対して、MuJoCo バージョン別に複数の mapping が存在する場合、Adapter は target MuJoCo version に一致する mapping を選択する。

選択順は以下とする。

1. target MuJoCo version に明示一致する mapping
2. target MuJoCo version を含む範囲 mapping
3. default mapping
4. fallback

対応する mapping が存在しない場合は diagnostics に記録する。

## 11. fallback方針

MuJoCo バージョンにより mapping が利用できない場合、fallback 方針に従う。

fallback 方針は以下を想定する。

- `use_default`
- `preserve_only`
- `warn`
- `error`
- `ignore`

fallback を適用した場合は、diagnostics または conversion_report に記録する。

## 12. diagnostics記録対象

MuJoCo バージョン対応では、以下を diagnostics に記録する。

- target MuJoCo version が未指定である
- installed MuJoCo version を target として使用した
- required_mujoco_version を満たさない
- supported_since より古い MuJoCo version が指定された
- deprecated_since 以降の MuJoCo version が指定された
- 対象バージョン用の mapping が存在しない
- fallback を適用した
- version policy と custom parameter schema が矛盾している

## 13. conversion_report記録対象

conversion_report には、以下を記録する。

- target MuJoCo version
- installed MuJoCo version
- 使用した mapping set
- version fallback 適用数
- deprecated parameter 使用数
- unsupported parameter 数
- version warning 数
- version error 数

## 14. controller_configとの関係

controller_config は、MuJoCo runtime または Adapter runtime のバージョン依存情報を持つことができる。

初期候補は以下とする。

- target MuJoCo version
- required Adapter version
- controller runtime version
- runtime feature flags

ただし、controller_config は MJCF の代替ではない。

MJCF へ出力すべき情報を controller_config へ退避する場合は、custom parameter schema の `io_scope` と `adapter_artifact` に基づく必要がある。

## 15. Python package versionとの関係

Python package `mujoco` の version と、MuJoCo library の機能差分は密接に関係する。

Adapter は、初期段階では Python package `mujoco.__version__` を installed MuJoCo version として扱う。

将来、Python package version と library version を分離して取得できる必要が生じた場合は、version policy を拡張する。

## 16. viewer対応方針

MuJoCo viewer は、OS、GPU、OpenGL、リモート実行環境の影響を受ける。

viewer の起動成功は、初期ローカル検証の必須条件に含めない。

headless の MJCF 読み込みと `mj_step` 実行を初期完了条件とする。

viewer 関連の問題は diagnostics または local validation log に記録してよい。

## 17. schema更新方針

MuJoCo バージョンアップにより新しい parameter、element、attribute が追加された場合、以下の順に対応する。

1. custom parameter schema の更新
2. mapping の追加
3. diagnostics code の追加
4. テスト仕様の追加
5. 実装の追加
6. conversion_report 記録項目の更新

## 18. 後方互換方針

Adapter は、可能な範囲で過去の MuJoCo バージョンに対する mapping を保持する。

ただし、保守困難または MuJoCo 側で廃止された機能については、deprecated または unsupported として扱う。

非対応化する場合は、diagnostics に明確に記録する。

## 19. 非スコープ

本ドキュメントでは、以下を非スコープとする。

- MuJoCo 全バージョン差分の網羅
- MuJoCo runtime の内部仕様定義
- Python package 管理方針の完全定義
- viewer 実装の詳細
- OS / GPU / OpenGL 互換性マトリクスの完全定義

## 20. 関連ドキュメント

- [MJCF変換方針](./01_MJCF変換方針.md)
- [custom parameter mapping](./03_custom_parameter_mapping.md)
- [controller_config仕様](./04_controller_config仕様.md)
- [diagnostics仕様](../01_共通/04_diagnostics仕様.md)
- [ローカルMuJoCo環境構築](../../04_実装計画/02_MuJoCo連携/01_ローカルMuJoCo環境構築.md)

---

[目次](../../目次.md) > SansaVRM-MuJoCo-Adapter > 仕様 > MuJoCo連携 > MuJoCoバージョン対応方針
