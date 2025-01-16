import os
import sys
import io
import requests
import PyPDF2
from argparse import ArgumentParser
import json
from flask import Flask, request, abort
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FileMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)

with open('white_list.json', 'r') as f:
    white_list = json.load(f)
white_list_user = white_list.get('white_list_user', {})
while_list_group = white_list.get('white_list_group', {})

if not channel_secret:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if not channel_access_token:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if not OPENAI_API_KEY:
    print('Specify OPENAI_API_KEY as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

@app.route("/test")
def test():
    return "test"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event: MessageEvent):
    if event.message.text.lower() in ["使用者資訊", "info"]:
        with ApiClient(configuration) as api_client:
            source = json.loads(event.source.json())
            user_id = source.get("user_id")
            group_id = source.get("group_id")

            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"使用者ID: {user_id}\n群組ID: {group_id}")]
                )
            )

@handler.add(MessageEvent, message=FileMessageContent)
def message_file(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        if event.message.file_name.endswith(".pdf"):    
            source = json.loads(event.source.json())
            user_id = source.get("user_id")
            group_id = source.get("group_id")
            
            if user_id in white_list_user.keys() or group_id in while_list_group.keys():
                pdf_content = read_pdf_from_url(f"https://api-data.line.me/v2/bot/message/{event.message.id}/content")
                summary = summarize_with_requests(pdf_content)
                # summary = f"test"

                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"{event.message.file_name}\n\n{summary}")]
                    )
                )
                app.logger.info("="*10)
                app.logger.info(f"group_id: {group_id}")
                app.logger.info(f"user_id: {user_id}")
                app.logger.info(f"user_name: {line_bot_api.get_profile(user_id).display_name}")
                app.logger.info(f"file_name: {event.message.file_name}")
                app.logger.info("="*10)
            else:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"你不是白名單使用者或群組，無法使用此功能")]
                    )
                )

def read_pdf_from_url(pdf_url: str) -> str:
    """
    由指定 URL 下載 PDF 檔案，並將其內容以文字方式回傳。
    """
    # 第一步：抓取 PDF 的位元組資料
    response = requests.get(pdf_url, headers={"Authorization": f"Bearer {channel_access_token}"})
    
    # 檢查回應碼是否成功（status_code == 200）
    if response.status_code != 200:
        raise Exception(f"無法下載 PDF。HTTP 狀態碼：{response.status_code}")
    
    # 將位元組資料轉成可被 PyPDF2 讀取的 BytesIO 物件
    pdf_bytes = response.content
    pdf_stream = io.BytesIO(pdf_bytes)
    
    # 第二步：使用 PyPDF2 解析 PDF
    reader = PyPDF2.PdfReader(pdf_stream)
    
    # 第三步：將所有頁面的文字合併
    all_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)
    
    return "\n".join(all_text)

def summarize_with_requests(content: str) -> str:
    """
    使用 requests 對 OpenAI ChatCompletion API 發送請求，
    將 content 作為用戶訊息，請求 GPT 生成摘要。
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    # 可以依需求調整 model、temperature、max_tokens 等參數
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "你是一個專業的摘要產生助手，請務必包含所有關鍵細節與背景資訊。"},
            {"role": "user", "content": f"請用繁體中文幫我總結以下內容，並提供詳細的背景、例子和重點資訊，若無法總結，請回傳『此檔案無法處理，PDF必須為純文字格式』：\n{content}"}
        ],
        "temperature": 0.0,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # 從回應 JSON 中取出摘要文字
    # 依照 OpenAI 回應格式，通常位於 data['choices'][0]['message']['content']
    try:
        summary = data['choices'][0]['message']['content']
        return summary.strip()
    except (KeyError, IndexError):
        return "摘要失敗，請檢查 API 回應。"

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    # arg_parser.add_argument('-h', '--host', default='0.0.0.0', help='host')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port, host="0.0.0.0")