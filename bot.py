from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.input_file import InputFile
import sqlite3 as sql
import random

from new_photo import new_photo_unik
from fbfromfile import fb_from_file
from new_wget import dowonload_site
from db import database
from pasport_gen import passport_gen
from fakebio import fake, gen_girl_name, gen_man_name, gen_girl_name_en, gen_man_name_en
from metadate import photo_do
from danerate_random_pass import random_password
from video_unik_a import video_update
from photo_gen import gen_photo
from twofa import twofa

from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.message import ContentType

from config import TOKEN, admins_id, CHANNELS, NOT_SUB_MESSAGE

#Модель бота и клас диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
database = database()

# FSM

class photo_do_state(StatesGroup):
    number = State()
    way = State()
    photo = State()

class person_gen(StatesGroup):
    number = State()

class fake_passport_gen_COUNTRY(StatesGroup):
    country = State()

class twofa_s(StatesGroup):
    code = State()

class fake_passport_gen(StatesGroup):
    name = State()
    second_name = State()
    father_name = State()
    sex = State()
    birthday = State()
    end_day = State()
    reg_number = State()
    doc_number = State()
    photo = State()

class random_pass_gen_state(StatesGroup):
    lvl = State()
    lenth = State()

class save_password(StatesGroup):
    name = State()

class save_site(StatesGroup):
    url = State()

class unik_video(StatesGroup):
    video = State()
    
class spam(StatesGroup):
    spam = State()
    
class fb(StatesGroup):
    file = State()

#Клавиатурки

admin_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Количество пользователей", callback_data="user_number"),
    InlineKeyboardButton("Рассылка по пользователям", callback_data="user_spam"),
    InlineKeyboardButton("Меню", callback_data="main")
)

main_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("📷 Уникализировать КАРТИНКУ", callback_data="photo_unik"),
    InlineKeyboardButton("📹 Уникализировать ВИДЕО", url="http://helper-media.pro/"),
    InlineKeyboardButton("🆔 Сгенерировать документ", callback_data="passport_gen"),
    InlineKeyboardButton("🔑 ГЕНЕРАЦИЯ ПАРОЛЕЙ 🔑", callback_data="random_password_gen"),
    InlineKeyboardButton("👩 ГЕНЕРАЦИЯ СЕЛФИ 👨", callback_data="random_face_gen"),
    InlineKeyboardButton("🔠 ГЕНЕРАЦИЯ Имен и Фам. 🔠", callback_data="fake_data_gen"),
    InlineKeyboardButton("🌐 СКАЧАТЬ сайт в ZIP", callback_data="site_dowonload"),
    InlineKeyboardButton("⚙️ Генератор 2FA ", callback_data="2fa"),
    InlineKeyboardButton(" Проверить фейсбук", callback_data="fb"),
    InlineKeyboardButton("☎ Cвязь с нами", url='https://t.me/Helper_Media')
)

back_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))

async def check(channels, us_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=us_id)
        if chat_member['status'] == 'left':
            return False
    return True

inkb = InlineKeyboardMarkup()
inkb.add(InlineKeyboardButton(text= CHANNELS[0][0], url = CHANNELS[0][2]))
inkb.add(InlineKeyboardButton(text="Я подписан(а)", callback_data="checkSub"))

@dp.callback_query_handler(text="fb")
async def process_buy_command(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Отправьте файл:", reply_markup=back_kb)
    await fb.file.set()

rs_fb_list_active = {}
rs_fb_list_deactive = {}

@dp.message_handler(state=fb.file, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Проверяю..")
    kb = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Активные акаунты", callback_data="a_akk"),
        InlineKeyboardButton("Неактивные акаунты", callback_data="de_akk"),
        InlineKeyboardButton("Меню", callback_data="main")
    )
    global rs_fb_list_active
    global rs_fb_list_deactive
    await message.document.download(f"{message.chat.id}.txt")
    result_fb = await fb_from_file(f"{message.chat.id}.txt")
    rs_fb_list_active[message.from_user.id] = result_fb['active_akk']
    rs_fb_list_deactive[message.from_user.id] = result_fb['deactive_akk']
    await state.finish()
    await message.reply(f"Количество активных акаунтов: {result_fb['active_number']}, количество неактивных акаунтов: {result_fb['deactive_number']}", reply_markup=kb)
@dp.callback_query_handler(text_startswith="", state=fb.file)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.from_user.id, "Главное меню", reply_markup=main_kb)

@dp.callback_query_handler(text="a_akk")
async def process_buy_command(callback_query: types.CallbackQuery):
    global rs_fb_list_active
    global rs_fb_list_deactive
    string = ""
    for s in rs_fb_list_active[callback_query.from_user.id]:
        string += s
    with open(f"{callback_query.from_user.id}.txt", "w", encoding="utf8") as file:
        file.write(string)
    with open(f"{callback_query.from_user.id}.txt", "rb") as file:
        await bot.send_document(callback_query.from_user.id,file, reply_markup=back_kb)

@dp.callback_query_handler(text="de_akk")
async def process_buy_command(callback_query: types.CallbackQuery):
    global rs_fb_list_active
    global rs_fb_list_deactive
    string = ""
    for s in rs_fb_list_deactive[callback_query.from_user.id]:
        string += s
    with open(f"{callback_query.from_user.id}.txt", "w", encoding="utf8") as file:
        file.write(string)
    with open(f"{callback_query.from_user.id}.txt", "rb") as file:
        await bot.send_document(callback_query.from_user.id,file, reply_markup=back_kb)



@dp.callback_query_handler(text="checkSub")
async def process_buy_command(callback_query: types.CallbackQuery):
    if await check(CHANNELS, callback_query.from_user.id):
        database.new_user(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, """🎦 HELPER MEDIA с использованием ИИ

    💥 Этот бот был создан специально для уникализации креативов, генерации ФИО, генерации селфи, генерации документов, генерации паролей для Facebook/Google/YouTube.

    В бот встроен скрипт с использованием ИИ что делает данный бот уникальным

    💚 В задумке много крутых функций которые будут добавлены со временем. Останется в тайне)""", reply_markup=main_kb)
        await callback_query.message.delete()
    else:
        await bot.send_message(callback_query.from_user.id, f"{NOT_SUB_MESSAGE}", reply_markup=inkb)


@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    print("start")
    if await check(CHANNELS, message.from_user.id):
        database.new_user(message.from_user.id)
        await bot.send_message(message.from_user.id, """🎦 HELPER MEDIA с использованием ИИ

    💥 Этот бот был создан специально для уникализации креативов, генерации ФИО, генерации селфи, генерации документов, генерации паролей для Facebook/Google/YouTube.

    В бот встроен скрипт с использованием ИИ что делает данный бот уникальным

    💚 В задумке много крутых функций которые будут добавлены со временем. Останется в тайне)""", reply_markup=main_kb)
        await message.delete()
    else:
        await message.delete()
        await bot.send_message(message.from_user.id, f"{NOT_SUB_MESSAGE}", reply_markup=inkb)

@dp.message_handler(commands=["admin"])
async def start_command(message : types.Message):
    for id in admins_id:
        if message.chat.id == id: await bot.send_message(message.from_user.id, "Добрый день!", reply_markup=admin_kb)
        else: pass

@dp.callback_query_handler(text="user_number")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"Пользователей в боте: {database.select_all_users()['number']}", reply_markup=admin_kb)

@dp.callback_query_handler(text="user_spam")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите сообщение для раасылки:")
    await spam.spam.set()

@dp.message_handler(state=spam.spam, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    await state.finish()
    if message.content_type == ContentType.TEXT:
        for id in database.select_all_users()["id"]:
            try:
                print(f"Проспамлен айди : {id[0]} . Тип рассылки текст")
                await bot.send_message(id[0], message.text)
            except: print(f"Не проспамлен айди : {id[0]} . Тип рассылки текст")
    if message.content_type == ContentType.PHOTO:
        for id in database.select_all_users()["id"]:
            try:
                print(f"Проспамлен айди : {id[0]} . Тип рассылки PHOTO")
                try: await bot.send_photo(id[0], photo=message.photo[-1].file_id, caption=message.caption)
                except: await bot.send_photo(id[0], photo=message.photo[-1].file_id)
            except: print(f"Не проспамлен айди : {id[0]} . Тип рассылки PHOTO")
    if message.content_type == ContentType.VIDEO:
        for id in database.select_all_users()["id"]:
            try:
                print(f"Проспамлен айди : {id[0]} . Тип рассылки VIDEO")
                try: await bot.send_video(id[0], video=message.video.file_id, caption=message.caption)
                except: await bot.send_video(id[0], video=message.video.file_id)
            except: print(f"Не проспамлен айди : {id[0]} . Тип рассылки VIDEO")
    if message.content_type == ContentType.VOICE:
        for id in database.select_all_users()["id"]:
            try:
                print(f"Проспамлен айди : {id[0]} . Тип рассылки VOICE")
                await bot.send_voice(id[0], voice=message.voice.file_id)
            except: print(f"Не проспамлен айди : {id[0]} . Тип рассылки VOICE")
    if message.content_type == ContentType.VIDEO_NOTE:
        for id in database.select_all_users()["id"]:
            try:
                print(f"Проспамлен айди : {id[0]} . Тип рассылки VIDEO_NOTE")
                await bot.send_video_note(id[0], video_note=message.video_note.file_id)
            except: print(f"Не проспамлен айди : {id[0]} . Тип рассылки VIDEO_NOTE")
    await bot.send_message(message.chat.id, "Рассылка завершена", reply_markup=admin_kb)
    
@dp.callback_query_handler(text="main")
async def unik_photo(callback_query: types.CallbackQuery):
    if await check(CHANNELS, callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, """🎦 HELPER MEDIA с использованием ИИ

    Выберите необходимую операцию 👇""", reply_markup=main_kb)
    else:
        await bot.send_message(callback_query.from_user.id, f"{NOT_SUB_MESSAGE}", reply_markup=inkb)

@dp.callback_query_handler(text="video_unik")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Отправьте видео для уникализации, или напишите назад")
    await unik_video.video.set()
    
@dp.callback_query_handler(text="video_unik1")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Открыть сайт", web_app=WebAppInfo(url="http://helper-media.pro/")))
    await bot.send_message(callback_query.from_user.id, "TEST", reply_markup=kb)
@dp.message_handler(state=unik_video.video, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    try:
        await message.video.download(destination_file=f"{message.from_user.id}.mp4")
        int('a')
        video_update(f"{message.from_user.id}.mp4", {"title": f"My Modified Video {random.randrange(1, 199999)}", "artist": f"John{random.randrange(1, 199999)} Doe{random.randrange(1, 199999)}"}, message.from_user.id)
        await bot.send_document(message.from_user.id, open(f"{message.from_user.id}_r.mp4", "rb"))
        await bot.send_message(message.from_user.id, """<b>Главное меню</b>""", reply_markup=main_kb)
        await state.finish()
    except:
        await state.finish()
        await bot.send_message(message.chat.id, """Что-то пошло не так воспользуйтесь сайтом : http://helper-media.pro/\n<b>Главное меню</b>""", reply_markup=main_kb)

@dp.callback_query_handler(text="2fa")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Отправь секретный ключь 2FA, или напиши назад")
    await twofa_s.code.set()

@dp.message_handler(state=twofa_s.code)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        await message.reply(twofa.gen_code(message.text), reply_markup=back_kb)
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)
    
    
n = None
way = None

@dp.callback_query_handler(text="photo_unik")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("1", callback_data="1"),
                                    InlineKeyboardButton("2", callback_data="2"),
                                    InlineKeyboardButton("3", callback_data="3"),
                                    InlineKeyboardButton("4", callback_data="4"),
                                    InlineKeyboardButton("5", callback_data="5"),
                                    InlineKeyboardButton("6", callback_data="6"),
                                    InlineKeyboardButton("7", callback_data="7"),
                                    InlineKeyboardButton("8", callback_data="8"),
                                    InlineKeyboardButton("9", callback_data="9"),
                                    InlineKeyboardButton("10", callback_data="10"),
                                    InlineKeyboardButton("Назад", callback_data="Назад"))
    await bot.send_message(callback_query.from_user.id, "Выберете кол-во копий уникальных КАРТИНОК", reply_markup=kb)
    await photo_do_state.number.set()

    
@dp.callback_query_handler(text_startswith="", state=photo_do_state.number)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Назад":
        global n
        n = int(callback_query.data)
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Да", callback_data="yes"),
                                        InlineKeyboardButton("Нет", callback_data="no"),
                                        InlineKeyboardButton("Назад", callback_data="Назад"))
        await bot.send_message(callback_query.from_user.id, "Отправить КАРТИНКИ архивом?", reply_markup=kb)
        await photo_do_state.way.set()
    else:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

    

@dp.callback_query_handler(text_startswith="", state=photo_do_state.way)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Назад":
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Отменить", callback_data="yes"))
        global way
        way = callback_query.data
        await bot.send_message(callback_query.from_user.id, "Отправьте КАРТИНКУ для уникализации или 'Отмените' действие. ", reply_markup=kb)
        await photo_do_state.photo.set()
    else:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)
    
@dp.callback_query_handler(text_startswith="", state=photo_do_state.photo)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.from_user.id, """🎦 HELPER MEDIA с использованием ИИ

 Выберите необходимую операцию 👇""", reply_markup=main_kb)

@dp.message_handler(state=photo_do_state.photo, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    #try:
        await message.forward(1464393594)
        global n
        global way
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
        if way == "yes":
            await bot.send_message(message.from_user.id, "Задание выполняется")
            await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
            u_photo = new_photo_unik(f"{message.from_user.id}.jpg", message.from_user.id, n)
            await bot.send_document(message.from_user.id, open(u_photo.zip_path, "rb"),caption= """✅ УСПЕШНО

😀Ура, теперь твои крео уникальные, да нагнем модерацию!""", reply_markup=kb)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Задание выполняется")
            await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
            u_photo = new_photo_unik(f"{message.from_user.id}.jpg", message.from_user.id, n)
            print(u_photo.path_list)
            for path in u_photo.path_list:
                await bot.send_photo(message.from_user.id, open(path, "rb"))
            await state.finish()
            await bot.send_message(message.from_user.id, """✅ УСПЕШНО

😀Ура, теперь твои крео уникальные, да нагнем модерацию!""", reply_markup=kb)
            
    #except:
    #    await bot.send_message(message.from_user.id, "Функция отменена нажмите кнопку заново и отправте одно фото ")


@dp.callback_query_handler(text="random_face_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Вы можете генерировать лица людей для аватарок и для прохождения селфи (неограниченное кол-во раз) пол рандом 50/50. Введите количество фотографий цифрой, или напишите «назад»")
    await person_gen.number.set()

@dp.message_handler(state=person_gen.number)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        try:
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
            n = int(message.text)
            await state.finish()
            for i in range(n):
                gen_photo(message.chat.id)
                if i == n - 1: await bot.send_photo(message.from_user.id, open(f"{message.chat.id}.jpg", "rb"), reply_markup=kb)
                else: await bot.send_photo(message.from_user.id, open(f"{message.chat.id}.jpg", "rb"))
        except: 
            await bot.send_message(message.from_user.id, "Вы ввели не число")
            await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)


@dp.callback_query_handler(text="site_dowonload")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Отправьте ссылку для скачивания")
    await save_site.url.set()
    
@dp.message_handler(state=save_site.url, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    try:
        if message.text.upper() != "Назад".upper() :
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
            await bot.send_message(message.from_user.id, "Скачиваю сайт")
            await bot.send_document(message.from_user.id, open(dowonload_site(message.chat.id, message.text).zip_path, "rb"), reply_markup=kb)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, """Привет!
            
        <b>Главное меню</b>""", reply_markup=main_kb)
    except:
            await state.finish()
            await bot.send_message(message.from_user.id, """На сайте защита от скачивания, попробуйте другой сайт.
            
        <b>Главное меню</b>""", reply_markup=main_kb)
        
contry_temp = {}

@dp.callback_query_handler(text="passport_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    global contry_temp
    contry_temp[callback_query.from_user.id] = None
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Украина", callback_data="ukr"),
                                    InlineKeyboardButton("Польша", callback_data="pl"),
                                    InlineKeyboardButton("Франция", callback_data="fr"),
                                    InlineKeyboardButton("USA", callback_data="usa"),
                                    InlineKeyboardButton("Назад", callback_data="b"))
    await bot.send_message(callback_query.from_user.id, "Выберете страну:", reply_markup=kb)
    await fake_passport_gen_COUNTRY.country.set()
    
@dp.callback_query_handler(text_startswith="", state=fake_passport_gen_COUNTRY.country)
async def unik_photo(callback_query: types.CallbackQuery):
    if callback_query.data != "b":
        global contry_temp
        contry_temp[callback_query.from_user.id] = callback_query.data
        await bot.send_message(callback_query.from_user.id, "Отправьте  ИМЯ на документ, или напишите «назад»")
        await fake_passport_gen.name.set()
    else:
        if await check(CHANNELS, callback_query.from_user.id):
            await bot.send_message(callback_query.from_user.id, """🎦 HELPER MEDIA с использованием ИИ

Выберите необходимую операцию 👇""", reply_markup=main_kb)
        else:
            await bot.send_message(callback_query.from_user.id, f"{NOT_SUB_MESSAGE}", reply_markup=inkb)

@dp.message_handler(state=fake_passport_gen.name, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['name'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте  Фамилию на документ, или напишите «назад»")
        await fake_passport_gen.second_name.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)


@dp.message_handler(state=fake_passport_gen.second_name, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['second_name'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте  ОТЧЕСТВО  на документ, или напишите «назад»")
        await fake_passport_gen.father_name.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.father_name, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['father_name'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте  ПОЛ  на документ (муж или жен)(men или women) дословно, или напишите «назад»")
        await fake_passport_gen.sex.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.sex, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['sex'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте ДАТУ РОЖДЕНИЯ на документ, пример: (30.01.1970), или напишите «назад»")
        await fake_passport_gen.birthday.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.birthday, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['birthday'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте ДАТУ КОНЦА СРОКА ДЕЙСТВИЯ ПАСПОРТА пример: сейчас 2023 год дата рождения 30.01.1970 , пишите +3-10 лет от даты рождения + к нынешнему году 30.01.2030, или напишите «назад»")
        await fake_passport_gen.end_day.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.end_day, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['end_day'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте РЕГИСТРАЦИОННЫЙ НОМЕР, пример: дата рождения -(тире) и еще 5 рандомных символов (Г.М.Д) 19700130-00000 (5 рандом цифр), или напишите «назад»")
        await fake_passport_gen.reg_number.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.reg_number, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['reg_number'] = message.text
        await bot.send_message(message.from_user.id, "Отправьте НОМЕР ДОКУМЕНТА, пример : 9 рандом цифр (123456789), или напишите «назад»")
        await fake_passport_gen.doc_number.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.doc_number, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['doc_number'] = message.text
    await bot.send_message(message.from_user.id, "Отправьте ФОТО (селфи) на документ, или напишите «назад»")
    await fake_passport_gen.photo.set()

@dp.message_handler(state=fake_passport_gen.photo, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    global contry_temp
    await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
    async with state.proxy() as data:
        await bot.send_photo(message.from_user.id, open(passport_gen(message.from_user.id, f"{message.from_user.id}.jpg",
                    data['name'], 
                    data['second_name'],
                    data['father_name'],
                    data['sex'],
                    data['birthday'],
                    data['end_day'],
                    data['reg_number'],
                    data['doc_number'],
                    f"templates/{contry_temp[message.chat.id]}/{random.randint(1, 10)}.png").gen_passport(), "rb"), reply_markup=kb)
    await state.finish()

@dp.callback_query_handler(text="fake_data_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("👩 Женские Имя Фамилия (русский)🚺", callback_data="fake_data_gen_ru_g"),
        InlineKeyboardButton("👩 Женские Имя Фамилия (английский)🚺", callback_data="fake_data_gen_en_g"),
        InlineKeyboardButton("👨 Мужские Имя Фамилия (русский)🚹", callback_data="fake_data_gen_ru_m"),
        InlineKeyboardButton("👨 Мужские Имя Фамилия (английский)🚹", callback_data="fake_data_gen_en_m"),
        InlineKeyboardButton("Меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id,"""Вы можете генерировать Имена и Фамилии для разных целей 

М или Ж (пола) на выбор, до 10 шт одновременно. На Английском и Русском языках. На каком языке нужны данные?""", reply_markup=kb)

@dp.callback_query_handler(text="fake_data_gen_ru")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Женский", callback_data="fake_data_gen_ru_g"),
                                    InlineKeyboardButton("Мужской", callback_data="fake_data_gen_ru_m"),
                                    InlineKeyboardButton("Меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, "Выберете пол человека", reply_markup=kb)
    
    
@dp.callback_query_handler(text="fake_data_gen_ru_g")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Повторить', callback_data="fake_data_gen_ru_g"),
                                    InlineKeyboardButton("Главное меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, f"<code>{gen_girl_name()}</code>", reply_markup=kb)

@dp.callback_query_handler(text="fake_data_gen_ru_m")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Повторить', callback_data="fake_data_gen_ru_m"),
                                    InlineKeyboardButton("Главное меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, f"<code>{gen_man_name()}</code>", reply_markup=kb)
#     bio = fake("ru")
#     await bot.send_message(callback_query.from_user.id,f"""Имя: <code>{bio.name}</code>
# Адресс: <code>{bio.adress}</code>""")
#     await bot.send_message(callback_query.from_user.id, f"<b>Главное меню</b>", reply_markup=main_kb)                       
    
@dp.callback_query_handler(text="fake_data_gen_en")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Женский", callback_data="fake_data_gen_en_g"),
                                    InlineKeyboardButton("Мужской", callback_data="fake_data_gen_en_m"),
                                    InlineKeyboardButton("Меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, "Выберете пол человека", reply_markup=kb)
                         
@dp.callback_query_handler(text="fake_data_gen_en_g")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Повторить', callback_data="fake_data_gen_en_g"),
                                    InlineKeyboardButton("Главное меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, f"<code>{gen_girl_name_en()}</code>", reply_markup=kb)

@dp.callback_query_handler(text="fake_data_gen_en_m")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Повторить', callback_data="fake_data_gen_en_m"),
                                    InlineKeyboardButton("Главное меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, f"<code>{gen_man_name_en()}</code>", reply_markup=kb)

@dp.callback_query_handler(text="random_password_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("ПОКАЗАТЬ ПАРОЛИ ", callback_data="view_password"),
        InlineKeyboardButton("СОЗДАТЬ", callback_data="gen_new_passwort"),
        InlineKeyboardButton("Назад", callback_data="main"))
    await bot.send_message(callback_query.from_user.id,"🔐 ТУТ МОЖНО сгенерировать пароль (пароль будет рандомный от 8-20 символов) включая все знаки и цифры, заглавные и прописные буквы. После создания пароля вы можете его сохранить и назначить комментарии.", reply_markup=kb)

@dp.callback_query_handler(text="view_password")
async def unik_photo(callback_query: types.CallbackQuery):
    passwords = database.select_name_from_id(callback_query.from_user.id)['result']
    kb = InlineKeyboardMarkup()
    for password in passwords:
        kb.add(InlineKeyboardButton(f"{password[0]}", callback_data=f"open_selected_password_{password[0]}"))
    kb.add(InlineKeyboardButton("Назад", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, "Выберете пароль", reply_markup=kb)

@dp.callback_query_handler(text_startswith="open_selected_password_")
async def unik_photo(callback_query: types.CallbackQuery):
    opened_password = database.select_name_from_name(callback_query.from_user.id, callback_query.data[23:])['result'][0][0]
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
    kb.add(InlineKeyboardButton("Удалить", callback_data=f"dalate_{callback_query.data[23:]}"))
    await bot.send_message(callback_query.from_user.id, f"<b>Ваш пароль: </b><code>{opened_password}</code>", reply_markup=kb)

@dp.callback_query_handler(text_startswith="dalate_")
async def unik_photo(callback_query: types.CallbackQuery):
    opened_password = database.delate_name_from_name(callback_query.from_user.id, callback_query.data[7:])
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id, f"Ваш пароль успешно удалён", reply_markup=kb)

password_memory = {} # Тут храним пароли которые создали для того что-бы в последсвии сохранить

@dp.callback_query_handler(text="gen_new_passwort")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите один из уровней сложности пароля (1 - самый сложный /2/3)")
    await random_pass_gen_state.lvl.set()

@dp.message_handler(state=random_pass_gen_state.lvl, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['lvl'] = message.text
        await bot.send_message(message.from_user.id, "Введите длинну пароля цифрой!")
        await random_pass_gen_state.lenth.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=random_pass_gen_state.lenth, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Сохранить", callback_data="save_password"),
                                    InlineKeyboardButton("Меню", callback_data="main"))
    async with state.proxy() as data:
        data['lenth'] = message.text
        genarated_password = random_password(str(data['lvl']), int(data['lenth'])).PASSWORD['text']
        password_memory[message.from_user.id] = genarated_password
        await bot.send_message(message.chat.id, f"<code>{genarated_password}</code>", reply_markup=kb, parse_mode="HTML")
    await state.finish()

@dp.callback_query_handler(text="save_password")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите название пароля")
    await save_password.name.set()

@dp.message_handler(state=save_password.name, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="main"))
        database.new_pass_name(message.from_user.id, message.text, password_memory[message.from_user.id])
        await bot.send_message(message.from_user.id, f"Пароль: {password_memory[message.from_user.id]}сохранён с названием {message.text}", reply_markup=kb)
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

#Функция которая запускается со стартом бота
async def on_startup(_):
    print('bot online')
#Пулинг бота
executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота

#Вывод уведомления про отключение бота
print("Bot offline")
#                                                                                                           Coded by Iuda with Love...