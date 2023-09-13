import telebot
from telebot import types
import yadisk

from config import TOKEN_BOT, TOKEN
from func import get_name, create_button, delete, get_files, download, buttons

bot = telebot.TeleBot(TOKEN_BOT)
public_dict = {}
p_d_copy = {}
public_counter = []
mass = []
path = '/02 Literatura'


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global path
    if call.message:
        msg = call.data
        if msg == 'back':
            print(path)
            path = delete(path)
            turn_back = get_name(path)
            public_dict.update(turn_back)
            print(public_dict)
            btn = create_button(turn_back, path)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'{path}', reply_markup=btn)

        elif msg == 'next':
            public_counter.append(1)
            print(public_counter)
            ikb2 = types.InlineKeyboardMarkup(row_width=3)
            btn = buttons(mass)

            for i in btn[len(public_counter)]:
                ikb2.add(i)
            ikb2.add(types.InlineKeyboardButton('>>След.>>', callback_data='next'))
            ikb2.add(types.InlineKeyboardButton('<<Назад<<', callback_data='back1'))
            ikb2.add(types.InlineKeyboardButton(f'{len(public_counter) + 1}/{len(btn)}', callback_data='empty'))
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Файлы для скачивания', reply_markup=ikb2)

        elif msg == 'back1':
            public_counter.pop()
            print(public_counter)
            ikb2 = types.InlineKeyboardMarkup(row_width=3)
            btn = buttons(mass)
            print(btn)
            if len(public_counter) > 0:
                for i in btn[len(public_counter)]:
                    ikb2.add(i)
                ikb2.add(types.InlineKeyboardButton('>>След.>>', callback_data='next'))
                ikb2.add(types.InlineKeyboardButton('<<Назад<<', callback_data='back1'))
                ikb2.add(types.InlineKeyboardButton(f'{len(public_counter) + 1}/{len(btn)}', callback_data='empty'))
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, 'Файлы для скачивания', reply_markup=ikb2)
            else:
                for i in btn[len(public_counter)]:
                    ikb2.add(i)
                ikb2.add(types.InlineKeyboardButton('>>След.>>', callback_data='next'))
                # ikb2.add(types.InlineKeyboardButton('<<Назад<<', callback_data='back1'))
                ikb2.add(types.InlineKeyboardButton(f'{len(public_counter) + 1}/{len(btn)}', callback_data='empty'))
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, 'Файлы для скачивания', reply_markup=ikb2)

        else:
            print('else')
            p_d_copy.clear()
            p_d_copy.update(public_dict)
            if len(public_dict) != 0:
                for i in p_d_copy:
                    print(f'{msg} == {i}')
                    if msg == i:
                        path = path + f'/{public_dict[i]}'
                        print(path)
                        data = get_name(path)
                        public_dict.clear()
                        public_dict.update(data)
                        if len(public_dict) != 0:
                            print(public_dict)
                            btn1 = create_button(data, path)
                            bot.delete_message(call.message.chat.id, call.message.message_id)
                            bot.send_message(call.message.chat.id, f'{path}', reply_markup=btn1)
                            break
                        else:
                            bot.send_message(call.message.chat.id, 'В данной папке находятся только файлы, чтобы их увидеть нажмите на кнопку ниже')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # y = yadisk.YaDisk(token=TOKEN)
    # search_dir = '02 Literatura'
    # y.is_dir('/' + search_dir)
    # for item in y.listdir(search_dir):
    #     print(item)

    all = get_name('/02 Literatura')
    # print('/02 Literatura')
    public_dict.update(all)
    print(public_dict)
    btn = create_button(all, path)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Показать файлы в этой папке"))
    bot.send_message(message.chat.id, text='Если хотите посмотреть содержимое папок, нажмите кнопку ниже', reply_markup=markup)

    bot.send_message(message.chat.id, 'Папка 02 Lteratura', reply_markup=btn)


@bot.message_handler(commands=['dirs'])
def send_welcome(message):

    all = get_name(path)
    print(path)
    public_dict.update(all)
    print(public_dict)
    btn = create_button(all, path)

    bot.send_message(message.chat.id, f'Текущая папка -> {path}', reply_markup=btn)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Показать файлы в этой папке':
        mass.clear()
        bot.send_message(message.chat.id, 'Необходимо немного подождать, файлы загружаются\nLoading…\n█▒▒▒▒▒▒▒▒▒')
        counter = 0
        files = (get_files(path))
        for i in files:
            counter += 1
            dow = path + f'/{i}'
            link = download(dow)
            mass.append(types.InlineKeyboardButton(text=i, url=link))
        ikb1 = types.InlineKeyboardMarkup(row_width=3)
        if len(mass) <= 8:
            for i in mass:
                ikb1.add(i)
            bot.send_message(message.chat.id, 'Файлы для скачивания', reply_markup=ikb1)
        else:
            btn = buttons(mass)
            print(btn)
            print(public_counter)
            for i in btn[len(public_counter)]:
                ikb1.add(i)
            ikb1.add(types.InlineKeyboardButton('>>След.>>', callback_data='next'))
            ikb1.add(types.InlineKeyboardButton(f'{len(public_counter)+1}/{len(btn)}', callback_data='empty'))
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Файлы для скачивания', reply_markup=ikb1)


bot.infinity_polling()
