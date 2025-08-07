#!/bin/sh

# PostgreSQLが起動するまで待機する
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# データベースが完全に利用可能になるのを少し待つ
sleep 5

# マイグレーションを実行
python manage.py makemigrations memo_app rag_app rag_config_log rag_evaluator_tool
python manage.py migrate

# スーパーユーザーを作成
python manage.py createsuperuser --no-input

# Djangoアプリケーションを起動
exec python manage.py runserver 0.0.0.0:8000