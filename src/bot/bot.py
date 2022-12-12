import os
import warnings

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.meta import db, MODELS, DEFAULT_MODEL
from src.structs import ItemType

warnings.filterwarnings("ignore")


bot = Bot(token=os.getenv('BOT_TOKEN'))
bot.GLOBAL_MODEL_CONFIG = DEFAULT_MODEL
dp = Dispatcher(bot)  # create as usual


@dp.message_handler(commands=['get_book_by_id'])
async def get_book_by_id(message: types.Message):
    book_id = int(message.text.split()[-1])
    item = db.get_item_by_id(book_id, ItemType.BOOK)
    ans = ''
    for k, v in item.items():
        ans += f'{k}: {v}\n\n'
    await message.reply(ans)

@dp.message_handler(commands=['get_film_by_id'])
async def get_film_by_id(message: types.Message):
    film_id = int(message.text.split()[-1])
    item = db.get_item_by_id(film_id, ItemType.FILM)
    ans = ''
    for k, v in item.items():
        ans += f'{k}: {v}\n\n'
    await message.reply(ans)

@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('model'))
async def process_callback_model(callback_query: types.CallbackQuery):
    model_name = callback_query.data.split('_')[-1]
    bot.GLOBAL_MODEL_CONFIG = model_name
    if model_name in MODELS:
        await bot.send_message(callback_query.from_user.id, f'{model_name} установлена.')
    else:
        await bot.send_message(callback_query.from_user.id, f'Ошибка установки {model_name}.')

@dp.message_handler(commands=['switch_model'])
async def switch_model(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=50)
    for model_name in MODELS.keys():
        inline_kb_full.add(InlineKeyboardButton(f'{model_name}', callback_data=f'model_{model_name}'))

    await message.reply("Выберите модель:", reply_markup=inline_kb_full)

@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data.split('_')[-1]
    book_id = bot.add_global_info[int(code)]
    recs = MODELS[bot.GLOBAL_MODEL_CONFIG].recommend(book_id)
    if not len(recs):
        await bot.send_message(callback_query.from_user.id, 'Нечего порекомендовать :(')
    for i, rec in enumerate(recs):
        item = db.get_item_by_id(rec, ItemType.FILM)
        await bot.send_message(callback_query.from_user.id, f'({i+1}) - {item["title"]}, {item["year"]:.0f}, {", ".join(item["lemmas_inter"])}\n\n{item["description"][:300]}...')

@dp.message_handler(commands=['get_reco'])
async def process_reco(message: types.Message):
    titles = db.find_matches_by_title(message.text, ItemType.BOOK)
    inline_kb_full = InlineKeyboardMarkup(row_width=200)
    bot.add_global_info = {}
    for i, title in enumerate(titles):
        bot.add_global_info[i] = db.find_id_by_title(title, ItemType.BOOK)
        inline_kb_full.add(InlineKeyboardButton(f'{i+1} - {title}', callback_data=f'btn_{i}'))

    await message.reply("Найдены следующие книги:", reply_markup=inline_kb_full)

@dp.message_handler(commands=['get_reco_by_id'])
async def process_reco_by_id(message: types.Message):
    book_id = int(message.text.split()[-1])
    recs = db.recommend(book_id)
    if not len(recs):
        await message.reply('Нечего порекомендовать :(')
    recs_text = ''
    for i, rec in enumerate(recs):
        item = db.get_item_by_id(rec, ItemType.FILM)
        recs_text += f'({i+1}) - {item["title"]}, {item["year"]:.0f}, {", ".join(item["lemmas_inter"])}\n\n{item["description"][:300]}...\n\n'
    await message.reply(recs_text)

@dp.message_handler(commands=['start', 'help'])
async def start(message):
    intruction = "/get_reco 'название книги для рекомендации'.\nПример: /get_reco преступление и наказание достоевский\n\n"
    intruction += "/get_reco_by_id 'id книгии для рекомендации'.\nПример /get_reco_by_id 1\n\n"
    intruction += "/get_film_by_id 'id фильма для получения информации'.\nПример /get_film_by_id 1\n\n"
    intruction += "/get_book_by_id 'id книги для получения информции'.\nПример /get_book_by_id 1\n\n"
    intruction += "/switch_model - смена установленной модели\n\n"
    await message.reply(intruction)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
