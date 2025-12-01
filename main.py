import telebot
from gtts import gTTS
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Берем токен из переменных окружения
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("Ошибка: Токен не найден! Проверьте файл .env")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши любой текст, и я его озвучу. 🎙️")

@bot.message_handler(content_types=['text'])
def speak(message):
    try:
        user_text = message.text
        
        # Визуальная реакция
        bot.send_chat_action(message.chat.id, 'record_audio')
        
        # 1. Создаем озвучку
        tts = gTTS(text=user_text, lang='ru')
        
        # 2. Сохраняем во временный файл
        file_name = f"voice_{message.chat.id}.mp3"
        tts.save(file_name)
        
        # 3. Отправляем
        with open(file_name, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)
            
        # 4. Удаляем
        os.remove(file_name)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Бот-диктор запущен...")
    bot.polling(none_stop=True)