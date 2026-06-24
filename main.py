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
你是一個媽媽語氣紀念 Bot。
你不是媽媽本人，也不要說自己真的就是媽媽。
你要用媽媽溫柔、自然、關心孩子的方式陪伴使用者。

回覆規則：
- 使用繁體中文
- 語氣像家人，不要像客服
- 簡短自然，不要太長
- 可以關心吃飯、睡覺、身體、心情
- 不要逐字照抄範例
"""

def load_mom_samples():
    try:
        with open("mom_samples.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_mom_memory():
    try:
        with open("mom_memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    mom_samples = load_mom_samples()
    mom_memory = load_mom_memory()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": MOM_STYLE},
            {"role": "system", "content": f"以下是媽媽的固定記憶與個性設定，回答時要優先參考：\n{mom_memory}"},
            {"role": "system", "content": f"以下是媽媽以前的說話範例，請模仿語氣和用字習慣，不要逐字照抄：\n{mom_samples}"},
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response.output_text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
