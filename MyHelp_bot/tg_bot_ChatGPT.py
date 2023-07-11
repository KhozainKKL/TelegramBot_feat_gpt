import os
import cv2
import openai
import telebot
import datetime
import requests
import subprocess
import pytesseract
from gtts import gTTS
from dotenv import load_dotenv
import speech_recognition as sr
# from parsing.parsing_vdd36 import get_data

NUMBERS_ROWS = 7

load_dotenv()

openai.api_key = os.getenv('SITE_API_KEY', None)
bot = telebot.TeleBot(os.getenv('TG_API_KEY', None))

token = os.getenv('TG_API_KEY', None)

logfile = str(datetime.date.today()) + '.log'

if not os.path.exists("users"):
    os.mkdir("users")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Привет! Я бот, который может создавать изображения, транскрибировать и переводить аудио текст.\n"
                          "Помимо этого ты можешь просто со мной пообщаться...\n"
                          " Чтобы узнать, как со мной работать, отправьте команду /help")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    help_text = "Я поддерживаю следующие команды:\n\n" \
                "/create_image - создать изображение\n " \
                "/transcribe - из голоса в текст\n" \
                "/translate - перевести аудио на англ. текст\n" \
                "/photo_to_text - из картинки в текст\n" \
                "/text_to_voice - из текста в голос"

    bot.send_message(chat_id=message.chat.id, text=help_text)


@bot.message_handler(commands=['create_image'])
def create_image(message):
    def tmp_2(message):
        try:
            send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
            response = openai.Image.create(
                prompt=message.text,
                n=5,
                size="1024x1024",
                response_format="url"
            )
            bot.send_media_group(chat_id=message.chat.id,
                                 media=[telebot.types.InputMediaPhoto(response['data'][0]['url']),
                                        telebot.types.InputMediaPhoto(response['data'][1]['url']),
                                        telebot.types.InputMediaPhoto(response['data'][2]['url']),
                                        telebot.types.InputMediaPhoto(response['data'][3]['url']),
                                        telebot.types.InputMediaPhoto(response['data'][4]['url'])])
        except telebot.apihelper.ApiTelegramException:
            bot.edit_message_text(text=format('Что-то с Вашим запросов пошло не так...\n'
                                              'Попробуйте позже.'),
                                  chat_id=message.chat.id, message_id=send_message.message_id)

    send_news = bot.reply_to(message, 'Подробно опишите изображение для создания.')
    bot.register_next_step_handler(send_news, tmp_2)


# Обработчик команды /transcribe
@bot.message_handler(commands=['transcribe'])
def transcribe(message):
    def tmp_1(message):
        def audio_to_text(dest_name: str):
            r = sr.Recognizer()
            message = sr.AudioFile(dest_name)
            with message as source:
                audio = r.record(source)
            result = r.recognize_google(audio, language="ru_RU")
            return result

        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        if message.voice:
            try:
                file_info = bot.get_file(message.voice.file_id)
                path = file_info.file_path
                fname = os.path.basename(path)
                doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
                with open(fname + '.oga', 'wb') as f:
                    f.write(doc.content)
                process = subprocess.run(['ffmpeg', '-i', fname + '.oga',
                                          fname + '.wav'])
                result = audio_to_text(fname + '.wav')
                bot.edit_message_text(text=format(f'Результат обработки:\n{result}'),
                                      chat_id=message.chat.id, message_id=send_message.message_id)
            except sr.UnknownValueError as e:
                bot.edit_message_text(text='Прошу прощения, но я не разобрал сообщение, или оно пустое...',
                                      chat_id=message.chat.id,
                                      message_id=send_message.message_id)
                with open(logfile, 'a', encoding='utf-8') as f:
                    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(
                        message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(
                        message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(
                        message.from_user.language_code) + ':Message is empty.\n')
            except Exception as e:
                with open(logfile, 'a', encoding='utf-8') as f:
                    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(
                        message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(
                        message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(
                        message.from_user.language_code) + ':' + str(e) + '\n')
            finally:
                os.remove(fname + '.wav')
                os.remove(fname + '.oga')

    send_news = bot.reply_to(message, 'Отправьте аудиофайл для транскрибирования.')
    bot.register_next_step_handler(send_news, tmp_1)


# Обработчик команды /translate
@bot.message_handler(commands=['translate'])
def translate(message):
    def tmp_4(message):
        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        if message.voice:
            try:
                file_info = bot.get_file(message.voice.file_id)
                path = file_info.file_path
                fname = os.path.basename(path)
                doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
                with open(fname + '.oga', 'wb') as f:
                    f.write(doc.content)
                process = subprocess.run(['ffmpeg', '-i', fname + '.oga',
                                          fname + '.wav'])
                result = open(fname + '.wav', "rb")
                transcript = openai.Audio.translate("whisper-1", result)
                bot.edit_message_text(text=format(f'Результат обработки:\n{transcript.text}'),
                                      chat_id=message.chat.id, message_id=send_message.message_id)
            except sr.UnknownValueError as e:
                bot.edit_message_text(text='Прошу прощения, но я не разобрал сообщение, или оно пустое...',
                                      chat_id=message.chat.id,
                                      message_id=send_message.message_id)
                with open(logfile, 'a', encoding='utf-8') as f:
                    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(
                        message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(
                        message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(
                        message.from_user.language_code) + ':Message is empty.\n')
            except Exception as e:
                with open(logfile, 'a', encoding='utf-8') as f:
                    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(
                        message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(
                        message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(
                        message.from_user.language_code) + ':' + str(e) + '\n')
            finally:
                os.remove(fname + '.wav')
                os.remove(fname + '.oga')

    send_news = bot.reply_to(message, 'Отправьте аудиофайл для перевода.')
    bot.register_next_step_handler(send_news, tmp_4)


@bot.message_handler(commands=['photo_to_text'])
def handle_pdf(message):
    def tmp_4(message):
        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        if message.photo:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            src = file_info.file_path
            try:
                downloaded_file = bot.download_file(file_info.file_path)
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                image = cv2.imread(src)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
                cv2.imwrite(src, thresh1)
                string = pytesseract.image_to_string(thresh1, lang='rus+eng')
                bot.edit_message_text(text=format(string), chat_id=message.chat.id, message_id=send_message.message_id)
            finally:
                os.remove(src)
        else:
            bot.edit_message_text(text=format('Не корректный файл...'), chat_id=message.chat.id,
                                  message_id=send_message.message_id)

    send_news = bot.reply_to(message, 'Отправьте изображение для транскрибации.')
    bot.register_next_step_handler(send_news, tmp_4)


@bot.message_handler(commands=['text_to_voice'])
def handle_youtube(message):
    def tmp_4(message):
        bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        obj = gTTS(text=message.text, lang='ru')
        downoladed_file = obj.save('voices/audio.mp3')
        audio = open('voices/audio.mp3', 'rb')
        bot.send_audio(chat_id=message.chat.id, audio=audio)

    send_news = bot.reply_to(message, 'Отправьте текст.')
    bot.register_next_step_handler(send_news, tmp_4)


# @bot.message_handler(commands=['parsing'])
# def parsing_site(message):
#     def tmp(message):
#         bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
#         tmp = get_data(message.text)
#         bot.send_document(message.chat.id, tmp)
#
#     send_news = bot.reply_to(message, 'Отправьте текст.')
#     bot.register_next_step_handler(send_news, tmp)


@bot.message_handler(content_types=['text'])
def msg(message):
    if f"{message.chat.id}.txt" not in os.listdir('users'):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write('')

    with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
        oldmes = file.read()

    if message.text == '/clear':
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='История очищена!')

    try:
        send_message = bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "user", "content": oldmes},
                      {"role": "user", "content": f'Предыдущие сообщения: {oldmes}; Запрос: {message.text}'}],
            presence_penalty=0.6)

        bot.edit_message_text(text=completion.choices[0].message["content"], chat_id=message.chat.id,
                              message_id=send_message.message_id)

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(
                message.text.replace('\n', ' ') + '\n' + completion.choices[0].message["content"].replace('\n',
                                                                                                          ' ') +
                '\n')

        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS + 1:
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=e)


bot.infinity_polling()
