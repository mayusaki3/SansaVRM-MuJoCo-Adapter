[目次](../../README.md) > docs > ja-JP > ローカルMuJoCo環境構築

# ローカルMuJoCo環境構築

## 1. 目的

本ドキュメントは、SansaVRM-MuJoCo-Adapter のローカル開発環境に MuJoCo Python 環境を作成し、最小 MJCF モデルの読み込み確認まで行う手順を定義する。

本手順の目的は以下とする。

- MuJoCo Python binding をローカル環境に導入する
- リポジトリ直下で仮想環境を作成する
- Git 管理対象外とするローカル成果物を明確化する
- 最小 MJCF モデルを読み込み、MuJoCo が動作することを確認する
- 将来の MJCF 生成・controller_config 生成・diagnostics 生成の土台を作る

## 2. 前提

### 2.1 対象OS

初期手順では、以下を対象とする。

- Windows 10 / Windows 11
- PowerShell
- Python 3.10 以上

Linux / macOS については、別途検証後に追記する。

### 2.2 MuJoCo導入方針

MuJoCo は Python package の `mujoco` を使用する。

MuJoCo Python binding は PyPI の `mujoco` package として配布され、MuJoCo library 本体も package に含まれるため、通常は MuJoCo 本体を別途手動インストールしない。

ただし、GUI viewer や OpenGL 関連の動作は OS / GPU / ドライバ / リモート環境の影響を受けるため、初期確認では headless の読み込み・step 実行を優先する。

## 3. ディレクトリ方針

リポジトリ直下に以下を作成する。

```text
SansaVRM-MuJoCo-Adapter/
├─ .venv/                         # Git対象外
├─ requirements-dev.txt            # Git対象
├─ examples/                       # Git対象
│  └─ minimal_body/
│     └─ model.xml                 # Git対象
├─ output/                         # Git対象外
└─ docs/
   └─ ja-JP/
      └─ 07_ローカルMuJoCo環境構築.md
```

## 4. 仮想環境作成

PowerShell でリポジトリ直下へ移動する。

```powershell
cd C:\WORKPLACE\Makes\GitHub\SansaVRM-MuJoCo-Adapter
```

仮想環境を作成する。

```powershell
py -3 -m venv .venv
```

仮想環境を有効化する。

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell の実行ポリシーにより有効化できない場合は、現在ユーザーの実行ポリシーを変更する。

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

変更後、再度仮想環境を有効化する。

## 5. pip更新

```powershell
python -m pip install --upgrade pip
```

## 6. 依存関係インストール

```powershell
pip install -r requirements-dev.txt
```

初期依存関係は以下とする。

```text
mujoco>=3.3.0
numpy>=1.26
pytest>=8.0
```

## 7. MuJoCo import確認

```powershell
python -c "import mujoco; print(mujoco.__version__)"
```

期待結果：

- エラーなく `mujoco` を import できる
- MuJoCo の version が表示される

## 8. 最小MJCF読み込み確認

`examples/minimal_body/model.xml` を使用して、MuJoCo が MJCF を読み込めることを確認する。

```powershell
python - <<'PY'
import mujoco

model = mujoco.MjModel.from_xml_path('examples/minimal_body/model.xml')
data = mujoco.MjData(model)

for _ in range(10):
    mujoco.mj_step(model, data)

print('MuJoCo load and step succeeded')
print('nbody:', model.nbody)
print('njnt:', model.njnt)
print('ngeom:', model.ngeom)
PY
```

PowerShell で here-document が扱いにくい場合は、以下の一行確認を使用する。

```powershell
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('examples/minimal_body/model.xml'); d=mujoco.MjData(m); mujoco.mj_step(m,d); print('ok', m.nbody, m.njnt, m.ngeom)"
```

## 9. GUI viewer確認

GUI viewer は必須ではない。

GUI 表示が可能な環境では、以下で viewer を起動できる。

```powershell
python -m mujoco.viewer --mjcf=examples/minimal_body/model.xml
```

GUI viewer が失敗しても、headless の `MjModel.from_xml_path` と `mj_step` が成功していれば、初期ローカル検証は成立とする。

## 10. Git対象外とするもの

以下は Git 管理対象外とする。

- `.venv/`
- `.env`
- `.env.*`
- `output/`
- `outputs/`
- `artifacts/`
- `logs/`
- `*.log`
- `*.mjb`
- `*.mjcf.compiled.xml`
- `controller_config.local.json`
- `conversion_report.local.json`
- `diagnostics.local.json`
- `local/`
- `tmp/`
- `temp/`
- `sandbox/`
- `assets/local/`
- `models/local/`

## 11. Git対象とするもの

以下は Git 管理対象とする。

- `README.md`
- `requirements-dev.txt`
- `.gitignore`
- `docs/`
- `examples/`
- `schemas/`
- `src/`
- `tests/`

ただし、`examples/` 配下でも巨大なバイナリ、外部から取得したモデル、個別環境依存の成果物は Git 管理対象外とする。

## 12. 初期完了条件

初期ローカル環境の完了条件は以下とする。

- `.venv` を作成できる
- `pip install -r requirements-dev.txt` が成功する
- `import mujoco` が成功する
- `examples/minimal_body/model.xml` を読み込める
- `mujoco.mj_step()` を実行できる
- Git 管理対象外のローカル生成物が `.gitignore` で除外されている

## 13. 次工程

初期環境構築後、以下へ進む。

1. `examples/minimal_body/model.xml` の追加
2. headless 動作確認用 test の追加
3. position actuator サンプルの追加
4. controller_config schema の追加
5. diagnostics schema の追加
6. SansaVRM API 連携前提の adapter skeleton 作成

---

[目次](../../README.md) > docs > ja-JP > ローカルMuJoCo環境構築
