# GenAI Learning Log
GenAI Learning Logへようこそ！このプロジェクトは、Django 5.2 を使用して、生涯学習講座や大学などでの学習メモの記録と、学習メモをもとにRAGで学習アシスタントを作ることについての開発記録を目的としたWebアプリケーションです。
- 学習メモ
  - 個人の学習メモを記録します。また、学習メモのCSVエクスポートや、作成済みの学習メモから、関連するToDoを作成することができます。
- ToDo管理
  - 個人の学習メモに関連するToDoを作成します。宿題や今後の予定、AIエージェント作成の忘れ防止に役立ちます。
- AIエージェント構成
  - RAGを含め、作成したAIエージェントの構成情報を記録します。この情報には、RAGにつかった学習メモの情報が含まれることがあります。AIエージェントの構成情報を共有することに役立ちます。
- RAG評価ログ
  - 手動で実施したRAGASによるRAGの評価結果を記録します。
- RAG評価ツール
  - 今後実装予定。今後の拡張用。

# 主な使い方
このアプリケーションが既に稼働しているとして.....

## 一般ユーザーが使う前に、管理者が準備しておくこと
1. DifyやLangflowなどでAIエージェントをつくりましょう。一般ユーザー（学生などの学習者）が、学習に使えるものがベストです。（参考資料：[生成AIアプリ開発入門：環境構築とチャットボット作成](https://mydocument.atlassian.net/wiki/spaces/support4textbook/pages/1860403430)）
2. AIエージェントのワークフローをエクスポートします。いわゆる定義ファイルと言われるもの。
2. 管理画面（/admin）にアクセスし、一般ユーザーを登録する。管理画面でグループを作成し、CSVインポート機能で複数人分のアカウントをまとめて作成する。
3. 管理者はログインし、「AIエージェント構成」で、サンプルとなるAIエージェントの定義ファイル（「２」のファイル）をアップロードする。
4. AIエージェント構成の画面に、サンプルとなるAIエージェント構成が掲載されていることを確認する。

## 一般ユーザー
1. 管理者が用意したアカウントでログインします。
2. 「学習メモ」の画面で、日々の学習について、各単元のまとめ（要約）をつくります。項目はすべて入力しましょう。「ToDo管理」もつかうと効果的です。
3. 蓄積した「学習メモ」をCSVエクスポートで、ダウンロードします。RAG利用の場合は、「科目」や「単元」、「記録内容」が必要です。ファインチューニングが目的の場合は、RAG利用向けの項目に加えて、「想定される質問例」や「質問への回答例」をCSVエクスポートに含めましょう。
3. 「AIエージェント構成」で、一覧画面に表示されているAIエージェント構成情報にアクセスし、表示されている内容をもとに、自分の学習アシスタントになるAIエージェントを作成します。ダウンロードしたCSVファイルをチャンクデータとして活用しましょう。ファインチューニングによるモデルカスタマイズを実施しても良いでしょう。
4. 作成したAIエージェントをいつでも再現できるように、ワークフローのバックアップを取得します。
5. 「AIエージェント構成」画面で、新規作成し、取得したファイルを含めたAIエージェント構成の情報を保存します。学習に取り組むなかで、様々なAIエージェントをつくるでしょうから、都度「AIエージェント構成」に登録し、AIエージェント構成の情報を保存します。保存した「AIエージェント構成」の情報は、他のユーザーから表示し、再利用することができます。

# ドキュメント
詳しくは、[wiki](https://github.com/kolinz/GenAI-Learning-Log/wiki)をご覧ください。

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

3. Python仮想環境をセットアップします。

以下のコマンドを実行します。
```
python3 -m venv venv
source venv/bin/activate
```

4. 依存関係をインストールします。

以下のコマンドを実行します。
```
pip install -r requirements.txt
```

5. コンテナの起動

以下のコマンドを実行して、コンテナをビルドし、起動します。
```
docker compose -f docker-compose.dev.yml up --build
```

6. アプリケーションへのアクセス

ブラウザで http://localhost:8000/memos/ にアクセスすると、アプリケーションを利用できます。

7. コンテナを終了する場合
以下のコマンドを実行して、コンテナを終了します。
```
docker compose -f docker-compose.dev.yml down -v
```
実行結果
```
✔ Container genai-learning-log-web-1       Removed                                                                0.0s
✔ Container genai-learning-log-db-1        Removed                                                                0.0s
✔ Volume genai-learning-log_postgres_data  Removed                                                                0.1s
✔ Network genai-learning-log_default       Removed  
```

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

3. entrypoint.prod.sh に実行権限を付与

コンテナ内でスクリプトが実行できるように、権限を付与します。
```
chmod +x entrypoint.prod.sh
```

4. 静的ファイルの収集

Nginxが配信する静的ファイルを収集します。
```
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --no-input
```

5. コンテナの起動

以下のコマンドを実行して、Nginx、Django、PostgreSQLの各コンテナをバックグラウンドで起動します。
```
docker compose -f docker-compose.prod.yml up --build -d
```

6. アプリケーションへのアクセス

ブラウザで http://localhost/ にアクセスすると、アプリケーションを利用できます。

7. コンテナの停止と削除

運用を停止する場合は、以下のコマンドでコンテナを停止します。すべてのデータを完全に削除する場合は -v オプションを追加します。
```
docker compose -f docker-compose.prod.yml down -v
```

# 開発計画
- [x] 検索機能の実装。
- [x] 学習メモについて、学習メモとAI対話記録の２つの種別項目を設ける。
- [x] 学習メモのCSVエクスポートについて、種別ごとに、学習メモとAI対話記録を別々にエクスポートする機能の実装。
- [x] 学習メモのCSVエクスポートについて、選択した学習メモだけをエクスポートする機能の実装。
- [x] ToDo管理アプリの基本機能を追加の実装。
- [x] 学習メモの詳細画面内に、関連するToDoを表示する機能を設ける。
- [x] 増えた機能をハンバーガーメニューにまとめる。
- [x] 学習メモからのエクスポート時に、ユーザーが自由に選択できるフォームを実装する。
- [x] 開発環境向けに、[maildev](https://github.com/maildev/maildev)を使えるようにする。
- [x] メールを使ったパスワードリセット機能を実装する。
- [x] 多言語化のための準備（configディレクトリ下のsettings.pyの変更、urls.pyの変更 , 各テンプレートの修正 , base.htmlで、言語切り替え表示を一時的にコメント化。多言語化の作業時に、base.htmlのコメント設定を解除する）。
- [x] 多言語化（日本語と英語）（機械翻訳を使って手短に実施した。今後の運用で必要に応じてアップデート。英語以外の言語の追加を検討。）
- [ ] 手動でRAGAS実行による評価結果を登録する手順書の作成と表示。
