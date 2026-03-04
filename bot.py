<<<<<<< HEAD
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User
from dotenv import load_dotenv

load_dotenv()

# Переменные из .env
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
admin_id = int(os.getenv('ADMIN_ID'))
keywords = [k.strip().lower() for k in os.getenv('KEYWORDS').split(',')]

# ВАЖНО: Используем уже сохранённую сессию
session_string = os.getenv('SESSION_STRING', '')
if not session_string:
    print('❌ ОШИБКА: SESSION_STRING не найдена в переменных Railway!')
    print('Добавь SESSION_STRING в Variables на Railway!')
    exit(1)

client = TelegramClient(StringSession(session_string), api_id, api_hash)

notified_messages = set()


@client.on(events.NewMessage())
async def handler(event):
    try:
        message_text = (event.message.text or '').lower()

        if not message_text:
            return

        chat_id = event.chat_id
        message_id = event.message.id
        unique_key = f"{chat_id}_{message_id}"

        if unique_key in notified_messages:
            return

        # Проверяем ключевые слова
        found_keyword = None
        for keyword in keywords:
            if keyword in message_text:
                found_keyword = keyword
                break

        if found_keyword:
            try:
                sender = await event.get_sender()
                sender_name = sender.first_name or 'Пользователь'
                if sender.last_name:
                    sender_name += ' ' + sender.last_name

                username = f"@{sender.username}" if sender.username else "нет username"

                chat = await event.get_chat()

                # Правильно определяем имя чата
                if isinstance(chat, User):
                    chat_title = chat.first_name or 'Приватный чат'
                else:
                    chat_title = chat.title or chat.name or 'Чат'

                message_link = f"https://t.me/c/{abs(chat_id)}/{message_id}"

                notification = f"""
🔔 <b>НАЙДЕН НОВЫЙ КЛИЕНТ!</b>

👤 <b>Клиент:</b> {sender_name}
🆔 <b>Контакт:</b> {username}
💬 <b>Канал/Чат:</b> {chat_title}
🎯 <b>Ключевое слово:</b> <code>{found_keyword}</code>

📝 <b>Сообщение:</b>
<code>{message_text[:300]}{"..." if len(message_text) > 300 else ""}</code>

<a href="{message_link}">👉 Открыть сообщение</a>
                """

                await client.send_message(admin_id, notification, parse_mode='html')

                notified_messages.add(unique_key)
                print(f"✅ Уведомление отправлено: {sender_name} в {chat_title}")

            except Exception as e:
                print(f"❌ Ошибка обработки: {e}")

    except Exception as e:
        print(f"❌ Ошибка обработчика: {e}")


async def main():
    print('🔐 Подключение к Telegram...\n')

    try:
        await client.connect()
        print('✅ Успешно подключено к Telegram!\n')
        print('🚀 Бот запущен и слушает сообщения...')
        print('⏹️  Для остановки нажми Ctrl+C\n')

        await client.run_until_disconnected()

    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')


if __name__ == '__main__':
    asyncio.run(main())
=======
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User
from dotenv import load_dotenv

load_dotenv()

# Переменные из .env
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
admin_id = int(os.getenv('ADMIN_ID'))
keywords = [k.strip().lower() for k in os.getenv('KEYWORDS').split(',')]

# Создаём клиент с сохранением сессии
session_string = os.getenv('SESSION_STRING', '')
client = TelegramClient(StringSession(session_string), api_id, api_hash)

notified_messages = set()


def save_session_to_env(session_str):
    """Сохраняет сессию в .env файл"""
    env_path = '.env'
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'SESSION_STRING=' in content:
        content = content.split('SESSION_STRING=')[0] + f'SESSION_STRING={session_str}\n'
    else:
        content += f'\nSESSION_STRING={session_str}'

    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('✅ SESSION_STRING сохранена в .env')


@client.on(events.NewMessage())
async def handler(event):
    try:
        message_text = (event.message.text or '').lower()

        if not message_text:
            return

        chat_id = event.chat_id
        message_id = event.message.id
        unique_key = f"{chat_id}_{message_id}"

        if unique_key in notified_messages:
            return

        # Проверяем ключевые слова
        found_keyword = None
        for keyword in keywords:
            if keyword in message_text:
                found_keyword = keyword
                break

        if found_keyword:
            try:
                sender = await event.get_sender()
                sender_name = sender.first_name or 'Пользователь'
                if sender.last_name:
                    sender_name += ' ' + sender.last_name

                username = f"@{sender.username}" if sender.username else "нет username"

                chat = await event.get_chat()

                # Правильно определяем имя чата
                if isinstance(chat, User):
                    chat_title = chat.first_name or 'Приватный чат'
                else:
                    chat_title = chat.title or chat.name or 'Чат'

                message_link = f"https://t.me/c/{abs(chat_id)}/{message_id}"

                notification = f"""
🔔 <b>НАЙДЕН НОВЫЙ КЛИЕНТ!</b>

👤 <b>Клиент:</b> {sender_name}
🆔 <b>Контакт:</b> {username}
💬 <b>Канал/Чат:</b> {chat_title}
🎯 <b>Ключевое слово:</b> <code>{found_keyword}</code>

📝 <b>Сообщение:</b>
<code>{message_text[:300]}{"..." if len(message_text) > 300 else ""}</code>

<a href="{message_link}">👉 Открыть сообщение</a>
                """

                await client.send_message(admin_id, notification, parse_mode='html')

                notified_messages.add(unique_key)
                print(f"✅ Уведомление отправлено: {sender_name} в {chat_title}")

            except Exception as e:
                print(f"❌ Ошибка обработки: {e}")

    except Exception as e:
        print(f"❌ Ошибка обработчика: {e}")


async def main():
    print('🔐 Подключение к Telegram...\n')

    try:
        await client.start(phone=phone_number)
        print('✅ Успешно подключено к Telegram!\n')

        # Сохраняем сессию
        session_str = client.session.save()
        save_session_to_env(session_str)

        print('🚀 Бот запущен и слушает сообщения...')
        print('⏹️  Для остановки нажми Ctrl+C\n')

        await client.run_until_disconnected()

    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')


if __name__ == '__main__':
    asyncio.run(main())
>>>>>>> 3507133e0f4ac3d53b2df7eb02164a4add6f9c1b
