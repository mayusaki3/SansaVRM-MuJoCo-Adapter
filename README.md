# SansaVRM-MuJoCo-Adapter

SansaVRM-MuJoCo-Adapter は、SansaVRM と MuJoCo / MJCF / controller configuration を接続するための Adapter プロジェクトです。

本リポジトリは、MuJoCo 固有の変換、近似、シミュレーション補助、検証処理を SansaVRM 本体から分離して扱うことを目的とします。

## 状態

本リポジトリは、初期設計およびローカル MuJoCo 環境整備の段階です。

現在の主な作業対象は以下です。

- SansaVRM 本体と本 Adapter の責務境界整理
- ローカル MuJoCo 開発環境の整備
- 最小 MJCF モデルの読み込みと step 実行確認
- 多言語対応を前提としたドキュメント構成の整備

## ドキュメント

ドキュメントは `docs/<language-code>/` 配下で管理します。

| 言語 | 目次 |
| --- | --- |
| 日本語 | [docs/ja-JP/目次.md](docs/ja-JP/目次.md) |

## クイックスタート

ローカル MuJoCo 環境構築および動作確認手順は、日本語ドキュメント目次から参照してください。

- [docs/ja-JP/目次.md](docs/ja-JP/目次.md)

## リポジトリの役割

SansaVRM 本体は、共通モデル情報、Adapter 向け API、custom parameter schema を管理する想定です。

本リポジトリは、MuJoCo 固有の処理を担当します。

- MJCF 生成
- MuJoCo actuator 写像
- controller configuration 生成
- MuJoCo 固有 diagnostics / conversion report 生成
- ローカル MuJoCo 検証用サンプル管理

詳細な仕様、手順、テスト方針は README ではなく、ドキュメントツリーに記録します。

## License

This repository is licensed under the MIT License.
