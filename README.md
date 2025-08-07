# GenAI Learning Log
GenAI Learning Logへようこそ！このプロジェクトは、Django 5.2 を使用して、生涯学習講座や大学などでの学習メモの記録と、学習メモをもとにRAGで学習アシスタントを作ることについての開発記録を目的としたWebアプリケーションです。
- 学習メモ
  - 個人の学習メモを記録および共有します。
- AIエージェント構成
  - RAGを含め、作成したAIエージェントの構成情報を記録します。この情報には、RAGにつかった学習メモの情報が含まれることがあります。AIエージェントの構成情報を共有することに役立ちます。
- RAG評価ログ
  - 手動で実施したRAGASによるRAGの評価結果を記録します。
- RAG評価ツール
  - 今後実装予定。今後の拡張用。

# 開発計画
- [ ] 検索機能
- [ ] 各項目へのツールチップ
- [x] 多言語化のための準備（configディレクトリ下のsettings.pyの変更、urls.pyの変更 , 各テンプレートの修正 , base.htmlで、言語切り替え表示を一時的にコメント化。多言語化の作業時に、base.htmlのコメント設定を解除する。）
- [ ] 多言語化
- [ ] 学習メモのCSVエクスポートについて、RAG向けとFT（ファインチューニング）向け、別々にエクスポートする機能
- [ ] 学習メモのCSVエクスポートについて、自分が作ったものだけをエクスポートする機能
- [ ] 学習メモのCSVエクスポートについて、科目ごとにエクスポートする機能
- [ ] チェックした学習メモを使って、RAG構成ログを新規作成する機能

# セットアップ
このアプリケーションは、Docker Compose を使って簡単に開発・運用できます。

## 依存関係のインストール
ローカルPCに以下のソフトウェアがインストールされていることを確認してください。
 - Docker Engine
 - Docker Compose

## プロジェクトのクローン
このリポジトリをローカルにクローンします。
```
git clone https://github.com/kolinz/GenAI-Learning-Log.git
cd GenAI-Learning-Log
```

## 開発環境での起動方法
この手順では、ホットリロード機能を持つDjango開発サーバーとPostgreSQLデータベースをDockerコンテナで起動します。

1. 環境設定ファイル (.env.dev) の準備
開発環境用の環境設定ファイルを作成します。
```
cp .env.dev.example .env.dev
```
SECRET_KEY やデータベース情報など、必要に応じて .env.dev ファイルの内容を編集してください。

2. entrypoint.sh に実行権限を付与
コンテナ内でスクリプトが実行できるように、権限を付与します。
```
cd app
chmod +x entrypoint.sh
cd ..
```

3. コンテナの起動
以下のコマンドを実行して、コンテナをビルドし、起動します。
```
docker compose -f docker-compose.dev.yml up --build
```

4. アプリケーションへのアクセス
ブラウザで http://localhost:8000/memos/ にアクセスすると、アプリケーションを利用できます。

## 本番環境での運用方法
この手順では、Nginxをリバースプロキシとして使用し、GunicornでDjangoアプリケーションを動かします。

1. 動作確認
本番環境で動かす前に、開発環境で十分なテストを行ってください。
  
2. 環境変数ファイル (.env.prod) の準備
本番環境用の環境設定ファイルを作成します。SECRET_KEY は必ず強固なものに変更してください。
```
cp .env.prod.example .env.prod
```
.env.prod ファイルには、本番用の SECRET_KEY や DEBUG=False、そして許可するホスト名 (ALLOWED_HOSTS) を記述します。
また、次の環境変数を適切な値に設定してください。

- DJANGO_SUPERUSER_USERNAME
- DJANGO_SUPERUSER_EMAIL
- DJANGO_SUPERUSER_PASSWORD
- POSTGRES_DB=genai_learning_db
- POSTGRES_USER=genai_user
- POSTGRES_PASSWORD=genai_password

3. 静的ファイルの収集
Nginxが配信する静的ファイルを収集します。
```
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --no-input
```

4. コンテナの起動
以下のコマンドを実行して、Nginx、Django、PostgreSQLの各コンテナをバックグラウンドで起動します。
```
docker compose -f docker-compose.prod.yml up --build -d
```

5. アプリケーションへのアクセス
ブラウザで http://localhost/ にアクセスすると、アプリケーションを利用できます。

6. コンテナの停止と削除
運用を停止する場合は、以下のコマンドでコンテナを停止します。すべてのデータを完全に削除する場合は -v オプションを追加します。
```
docker compose -f docker-compose.prod.yml down -v
```
