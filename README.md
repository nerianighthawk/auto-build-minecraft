# マイクラサーバー自動ビルドツール

## セットアップ

### Docker 関連

`Docker/resources` にマイクラフォルダに入れたいものを入れる

- eula.txt
- ops.json
- whitelist.json
- server.properties
- world/
- mod/

### ansible 実行環境

GCP 用の Ansible プラグインをインストールする

```console
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-sdk
```

Ansible のコレクションをインストールする

```console
ansible-galaxy collection install google.cloud
```

### GCP の認証

GCP のサービスアカウントを作成し、サービスアカウントの認証ファイルを `env/` ディレクトリに入れる

### 変数設定

`/var` ディレクトリに以下の3つのファイルを入れる

```yml:playbook-vars.yml
exec_type: "create"
```

```yml:create-instance-vars.yml
gcp_project: "sample-00000"
gcp_network: "network"
gcp_cred_file: "env/sample.json"
zone: "asia-northeast1-b"
region: "asia-northeast1"
hostname: "sample"
user_name: "sample-user"
ssh_key_dir: "~/.ssh/"
```

```yml:run-server-vars.yml
resource_file_dest: "/home/sample-user"
image_name: "sample-image"
container_name: "sample-container"
```

## 実行

以下で実行する

```console
ansible-playbook playbook.yml
```

`playbook-vars.yml` に記載されている `exec_type` の値によって、実行時の挙動は以下のように変化する

- `create` の場合、サーバーの構築とインスタンスの作成を行う
- `stop` の場合、サーバーとインスタンスの停止を行う
- `start` の場合、サーバーとインスタンスの起動を行う
- `delete` の場合、サーバーとインスタンスの削除を行う
- `download` の場合、サーバーからワールドデータのダウンロードを行う
