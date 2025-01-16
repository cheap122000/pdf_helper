# 執行步驟
### 設定環境變數
- 使用 `bash setup_env.sh` 設定環境變數
- .env 自行填寫以下資訊
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
    - OPENAI_API_KEY
- white_list.json 編輯白名單避免誤用
    - 編輯完成後使用 `docker restart pdf-helper` 重新啟動容器即可讀取

### 執行指令
```
docker compose up -d
```
