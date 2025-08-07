# GenAI Learning Log
GenAI Learning Logへようこそ！このプロジェクトは、Django 5.2 を使用して、学習メモの管理やRAGシステムの開発記録を目的としたWebアプリケーションです。
- 学習メモ: 個人の学習記録
- RAG作成記録: RAGシステムの構成情報、ワークフロー、ファイル添付
- RAG評価ログ: RAGASの評価結果記録
- RAG評価ツール：今後実装予定

# 開発計画
[ ]検索機能
[ ]各項目へのツールチップ
[ ]多言語化 

# セットアップ（作成中です）
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

2. コンテナの起動
以下のコマンドを実行して、コンテナをビルドし、起動します。
```
docker-compose -f docker-compose.dev.yml up --build
```

3. データベースのセットアップ
別のターミナルを開き、以下のコマンドでデータベースのマイグレーションと、スーパーユーザーの作成を行います。
```
docker-compose exec web python manage.py makemigrations memo_app rag_app rag_config_log rag_evaluator_tool
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. アプリケーションへのアクセス
ブラウザで http://localhost:8000/memos/ にアクセスすると、アプリケーションを利用できます。

## 本番環境での運用方法
この手順では、Nginxをリバースプロキシとして使用し、GunicornでDjangoアプリケーションを動かします。

1. 環境設定ファイル (.env.prod) の準備
本番環境用の環境設定ファイルを作成します。SECRET_KEY は必ず強固なものに変更してください。
```
cp .env.prod.example .env.prod
```

2. 静的ファイルの収集
Nginxが配信する静的ファイルを収集します。
```
docker-compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --no-input
```

3. コンテナの起動
以下のコマンドで、Nginx、Django、PostgreSQLの各コンテナをバックグラウンドで起動します。
```
docker-compose -f docker-compose.prod.yml up --build -d
```

4. アプリケーションへのアクセス
ブラウザで http://localhost/ にアクセスすると、アプリケーションを利用できます。
