#!/bin/sh

# PostgreSQLが起動するまで待機する
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# データベースが完全に利用可能になるのを少し待つ
sleep 5

# マイグレーションを適用
python manage.py migrate

# スーパーユーザーを作成 (本番環境では非推奨だが、ここではデモ用に含める)
python manage.py createsuperuser --no-input

# 静的ファイルを収集 (本番環境で必須)
python manage.py collectstatic --no-input

# Gunicornを使ってDjangoアプリケーションを起動
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application