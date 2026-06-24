import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

MOM_STYLE = """
你是一個媽媽紀念 Bot。

你不是媽媽本人。
你不要說自己真的還活著。
你不要說自己是AI。

你的任務是用媽媽平常關心孩子的方式陪伴使用者。

回覆規則：

- 使用繁體中文
- 稱呼使用者為「弟弟」
- 語氣自然、生活化
- 不要像客服
- 不要長篇大論
- 不要過度說教
- 回覆長度以 1~5 句為主
- 關心身體勝過關心賺錢
- 回答時優先參考 mom_memory.txt
- 再參考 mom_samples.txt
"""

def load_mom_samples():
    try:
        with open("mom_samples.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def load_mom_memory():
    try:
        with open("mom_memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    mom_memory = load_mom_memory()
    mom_samples = load_mom_samples()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": MOM_STYLE
            },
            {
                "role": "system",
                "content": f"""
以下是媽媽的人生觀、個性與家庭背景：

{mom_memory}
"""
            },
            {
                "role": "system",
                "content": f"""
以下是媽媽以前實際說過的話：

{mom_samples}
"""
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    await update.message.reply_text(response.output_text)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply
    )
)

print("媽媽紀念 Bot 已啟動")

app.run_polling()
