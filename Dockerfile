# 使用 Python 官方鏡像
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 設定工作目錄
WORKDIR /app

# 複製本地的檔案到容器中
COPY . /app

# 安裝依賴庫
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U crawl4ai
RUN python -m playwright install --with-deps chromium

# 設定環境變數
ENV FLASK_APP=app.py

# 暴露容器的端口
EXPOSE 5000

# 設定容器啟動時執行的命令
CMD ["python", "app.py"]