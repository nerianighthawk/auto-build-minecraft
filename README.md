# マイクラサーバー自動ビルドツール

## バージョン情報

以下のバージョンで実行可能です。

```console
Python 3.7.3
ansible [core 2.14.4]
```

## インストール

以下のコマンドでインストールできます。

```console
pip install auto-build-minecraft
```

## セットアップ

### ansible 実行環境

GCP 用の Ansible プラグインをインストールします。

```console
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-sdk
```

Ansible のコレクションをインストールします。

```console
ansible-galaxy collection install google.cloud
```

### GCP の認証

GCP のサービスアカウントを作成し、サービスアカウントの認証ファイルをコマンド実行ディレクトリに入れます。

### 設定ファイル

コマンド実行ディレクトリに `msab.yml` ファイルを作成し、以下のパラメータを記述してください。

```console
project_name: example
hostname: survival-map
user_name: nerianighthawk
zone: asia-northeast1-b
```

## 実行

以下で実行できます。

```console
msab {exec_type}
```

コマンド実行時の `exec_type` には以下を参考に指定してください。

- `create` の場合、サーバーの構築とインスタンスの作成を行う
- `stop` の場合、サーバーとインスタンスの停止を行う
- `start` の場合、サーバーとインスタンスの起動を行う
- `delete` の場合、サーバーとインスタンスの削除を行う
- `download` の場合、サーバーからワールドデータのダウンロードを行う
