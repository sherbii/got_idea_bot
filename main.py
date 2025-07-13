
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd

API_TOKEN = "8070778295:AAFfnC-o627YmsQ3KohF-aOPUExiXnsx5sM"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Загружаем таблицы
categories = pd.read_excel("data/категории.xlsx")
examples = pd.read_excel("data/примеры.xlsx")

# Начало
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я помогу выбрать, чем заняться.\nНапиши /idea, чтобы начать!")

# Обработка /idea
@dp.message_handler(commands=['idea'])
async def idea_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i, row in categories.iterrows():
        button_text = row['category_name']
        callback_data = f"cat_{row['id']}"
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    await message.answer("Вот что тебе может подойти 👇", reply_markup=keyboard)

# Выбор категории
@dp.callback_query_handler(lambda c: c.data.startswith("cat_"))
async def show_examples(callback_query: types.CallbackQuery):
    cat_id = int(callback_query.data.split("_")[1])
    matched = examples[examples["parent_category_id"] == cat_id]
    if matched.empty:
        await bot.send_message(callback_query.from_user.id, "Отличный способ провести время 👍\n\n🔁 Вернуться к другим вариантам")
    else:
        for _, row in matched.iterrows():
            text = f"🎯 {row['title']}"
            if pd.notna(row['address']):
                text += f"\n📍 {row['address']}"
            if pd.notna(row['link']):
                text += f"\n🔗 {row['link']}"
            if pd.notna(row['extra_info']):
                text += f"\n💬 {row['extra_info']}"
            await bot.send_message(callback_query.from_user.id, text)
        await bot.send_message(callback_query.from_user.id, "🔁 Вернуться к другим вариантам — /idea")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
