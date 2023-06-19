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
from save_site import dowobload_site
from db import database
from pasport_gen import passport_gen
from fakebio import fake, gen_girl_name, gen_man_name, gen_girl_name_en, gen_man_name_en
from metadate import photo_do
from danerate_random_pass import random_password
from video_unik_a import video_update
from photo_gen import gen_photo

from aiogram.types.message import ContentType

from config import TOKEN

#Модель бота и клас диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
ds = dowobload_site()
database = database()

# FSM

class photo_do_state(StatesGroup):
    number = State()
    way = State()
    photo = State()

class person_gen(StatesGroup):
    number = State()

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

#Клавиатурки

main_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Уникализация фото", callback_data="photo_unik"),
    InlineKeyboardButton("Генерация паспорта", callback_data="passport_gen"),
    InlineKeyboardButton("Сгенерировать рандомный пароль", callback_data="random_password_gen"),
    InlineKeyboardButton("Уникализация видео", callback_data="video_unik"),
    InlineKeyboardButton("Генерация лиц", callback_data="random_face_gen"),
    InlineKeyboardButton("Скачать сайт", callback_data="site_dowonload"),
    InlineKeyboardButton("Генерация данных", callback_data="fake_data_gen")

)

@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    await bot.send_message(message.from_user.id, """Привет!
    
<b>Главное меню</b>""", reply_markup=main_kb)
    await message.delete()

@dp.callback_query_handler(text="main")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, """Привет!
    
<b>Главное меню</b>""", reply_markup=main_kb)

@dp.callback_query_handler(text="video_unik")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Отправьте видео для уникализации")
    await unik_video.video.set()

@dp.message_handler(state=unik_video.video, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    try:
        await message.video.download(destination_file=f"{message.from_user.id}.mp4")
        video_update(f"{message.from_user.id}.mp4", {"title": f"My Modified Video {random.randrange(1, 199999)}", "artist": f"John{random.randrange(1, 199999)} Doe{random.randrange(1, 199999)}"}, message.from_user.id)
        await bot.send_document(message.from_user.id, open(f"{message.from_user.id}_r.mp4", "rb"))
    except: 
        await message.document.download(destination_file=f"{message.from_user.id}.MOV")
        #video_update(f"{message.from_user.id}.mp4", {"title": f"My Modified Video {random.randrange(1, 199999)}", "artist": f"John{random.randrange(1, 199999)} Doe{random.randrange(1, 199999)}"}, message.from_user.id)
        #await bot.send_document(message.from_user.id, open(f"{message.from_user.id}_r.mp4", "rb"))

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
    await bot.send_message(callback_query.from_user.id, "Выберете количество выходных фото", reply_markup=kb)
    await photo_do_state.number.set()

    
@dp.callback_query_handler(text_startswith="", state=photo_do_state.number)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Назад":
        global n
        n = int(callback_query.data)
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Да", callback_data="yes"),
                                        InlineKeyboardButton("Нет", callback_data="no"),
                                        InlineKeyboardButton("Назад", callback_data="Назад"))
        await bot.send_message(callback_query.from_user.id, "Отправить фото архивом?", reply_markup=kb)
        await photo_do_state.way.set()
    else:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

    

@dp.callback_query_handler(text_startswith="", state=photo_do_state.way)
async def photo_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Назад":
        global way
        way = callback_query.data
        await bot.send_message(callback_query.from_user.id, "Отправьте фото")
        await photo_do_state.photo.set()
    else:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)
    



@dp.message_handler(state=photo_do_state.photo, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    #try:
        global n
        global way
        if way == "yes":
            await bot.send_message(message.from_user.id, "Обрабатываю")
            await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
            u_photo = new_photo_unik(f"{message.from_user.id}.jpg", message.from_user.id, n)
            await bot.send_document(message.from_user.id, open(u_photo.zip_path, "rb"), "Готво!")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Обрабатываю")
            await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
            u_photo = new_photo_unik(f"{message.from_user.id}.jpg", message.from_user.id, n)
            for i in range(n):
                await bot.send_photo(message.from_user.id, open(f"media/{message.from_user.id}/{message.from_user.id}_{n - 1}.png", "rb"))
            await state.finish()
            await bot.send_message(message.from_user.id, "Готово!")
            
    #except:
    #    await bot.send_message(message.from_user.id, "Функция отменена нажмите кнопку заново и отправте одно фото ")


@dp.callback_query_handler(text="random_face_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите количество фотографий цифрой, или назад")
    await person_gen.number.set()

@dp.message_handler(state=person_gen.number)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        try:
            n = int(message.text)
            await state.finish()
            for i in range(n):
                gen_photo(message.chat.id)
                await bot.send_photo(message.from_user.id, open(f"{message.chat.id}.jpg", "rb"))
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
    if message.text.upper() != "Назад".upper() :
        await bot.send_message(message.from_user.id, "Скачиваю сайт")
        await bot.send_document(message.from_user.id, open(ds.website(message.text, str(message.from_user.id), str(message.from_user.id), str(message.from_user.id)), "rb"))
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.callback_query_handler(text="passport_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите имя, которое будет в паспорте")
    await fake_passport_gen.name.set()

@dp.message_handler(state=fake_passport_gen.name, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    if message.text.upper() != "Назад".upper() :
        async with state.proxy() as data:
            data['name'] = message.text
        await bot.send_message(message.from_user.id, "Введите фамилию, которая будет в паспорте")
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
        await bot.send_message(message.from_user.id, "Введите отчество, которое будет в паспорте")
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
        await bot.send_message(message.from_user.id, "Введите пол человека, который будет в паспорте")
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
        await bot.send_message(message.from_user.id, "Введите день рождения человека, который будет в паспорте")
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
        await bot.send_message(message.from_user.id, "Введите дату окончания паспорта")
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
        await bot.send_message(message.from_user.id, "Введите дату регистрации паспорта")
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
        await bot.send_message(message.from_user.id, "Введите номер паспорта")
        await fake_passport_gen.doc_number.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, """Привет!
        
    <b>Главное меню</b>""", reply_markup=main_kb)

@dp.message_handler(state=fake_passport_gen.doc_number, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['doc_number'] = message.text
    await bot.send_message(message.from_user.id, "Отправьте фото для паспорта")
    await fake_passport_gen.photo.set()

@dp.message_handler(state=fake_passport_gen.photo, content_types=ContentType.ANY)
async def photo_state(message : types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file=f"{message.from_user.id}.jpg")
    async with state.proxy() as data:
        await bot.send_photo(message.from_user.id, open(passport_gen(message.from_user.id, f"{message.from_user.id}.jpg",
                    data['name'], 
                    data['second_name'],
                    data['father_name'],
                    data['sex'],
                    data['birthday'],
                    data['end_day'],
                    data['reg_number'],
                    data['doc_number']).gen_passport(), "rb"))
    await state.finish()


@dp.callback_query_handler(text="fake_data_gen")
async def unik_photo(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Русский", callback_data="fake_data_gen_ru"),
        InlineKeyboardButton("Англиский", callback_data="fake_data_gen_en"),
        InlineKeyboardButton("Меню", callback_data="main"))
    await bot.send_message(callback_query.from_user.id,"На каком языке нужны данные?", reply_markup=kb)

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
        InlineKeyboardButton("Посмотреть пароли", callback_data="view_password"),
        InlineKeyboardButton("Сгенерировать новый", callback_data="gen_new_passwort"),
        InlineKeyboardButton("Назад", callback_data="main"))
    await bot.send_message(callback_query.from_user.id,"Что делаем?", reply_markup=kb)

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
    await bot.send_message(callback_query.from_user.id, f"<b>Ваш пароль: </b><code>{opened_password}</code>")

password_memory = {} # Тут храним пароли которые создали для того что-бы в последсвии сохранить

@dp.callback_query_handler(text="gen_new_passwort")
async def unik_photo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите один из уровней сложности пароля (1/2/3)")
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
        genarated_password = random_password(int(data['lvl']), int(data['lenth'])).PASSWORD['text']
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
        database.new_pass_name(message.from_user.id, message.text, password_memory[message.from_user.id])
        await bot.send_message(message.from_user.id, f"Пароль: {password_memory[message.from_user.id]} сохранён с названием {message.text}")
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