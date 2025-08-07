# Dockerfile

# Pythonの公式イメージをベースとして使用
FROM python:3.12-slim

# アップデートとnetcatのインストール
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# 環境変数を設定（環境変数は.envファイルで設定されるため、ここではデフォルト値や説明を記載）
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリをコンテナ内に設定
WORKDIR /app

# プロジェクトの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトのコードを作業ディレクトリにコピー
COPY . .

# ホストから公開するポートを指定
EXPOSE 8000

# コンテナ起動時に実行するコマンド
# DBが起動するまで待機するため、Djangoのコマンドを直接実行するのではなく、スクリプトを使用
CMD ["/app/entrypoint.sh"]