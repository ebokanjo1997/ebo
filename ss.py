import logging
import requests
from user_agent import generate_user_agent
import os
from bs4 import BeautifulSoup
import yt_dlp
import re
import instaloader
import json
import sqlite3
from datetime import datetime
import asyncio
import urllib.parse
import time
from typing import Optional, Dict, Any, List
from io import BytesIO
import sys
import signal

TOKEN = "7353125557:AAGfxiWv1TaBfOW38mOujwzpyJKfnpXX978"
CHANNEL_USERNAME = "@e_1bo2"
CHANNEL_USERNAME2 = "@e_1bo2"  
DEVELOPER_IDS = [868526133]


TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


TIKTOK_API_URL = "https://tiksave.io/api/ajaxSearch"
TIKTOK_HEADERS = {
    'authority': 'tiksave.io',
    'accept': '*/*',
    'accept-language': "ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://tiksave.io',
    'referer': 'https://tiksave.io/ar',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': "?1",
  'sec-ch-ua-platform': "\"Android\"",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "no-cors",
  'sec-fetch-dest': "image",
    'user-agent': generate_user_agent(),
    'x-requested-with': 'XMLHttpRequest',
}
TIKTOK_COOKIES = {
    '__gads': 'ID=845d6f69a383b47d:T=1753115039:RT=1753777189:S=ALNI_MZ5mo4zUsj-FGlikaQuoQ4_swmsAw',
    '__gpi': 'UID=000010f3a3509093:T=1753115039:RT=1753777189:S=ALNI_MYygG_4blpkyQSIgGe4X14XjLOv_A',
    '__eoi': 'ID=f988b7216243e3f9:T=1753115039:RT=1753777189:S=AA-AfjaaFPzIIsO8HLZKRQPpo5H_',
    'FCNEC': '%5B%5B%22AKsRol_DFZW-z9Bos6qXwGfO8Q5J58PDhfHvyYmhEhiH_YoMOq4xyT_w_UAqYzh9EZDicGKtVO2YdT96aKCyE-6wO0HnG4tshKgcaw846Q46khC5rq-e0BMBYFBSXcTwPuhBnMw16CGjkEBIuJA9kx7kb17k5UHIZQ%3D%3D%22%5D%5D',
}

PINTEREST_IMG_API = "https://api.pinterestdl.io/api/image"
PINTEREST_API_URL = "https://everyweb.net/wp-json/aio-dl/video-data/"
PINTEREST_TOKEN = "0d8a45597e998fd21242b74089fac11b70dd1499a2ba25ad3b6100238811eafd"
PINTEREST_HASH = "aHR0cHM6Ly9waW4uaXQvNmp0RVZPRkdz1024YWlvLWRs"
PINTEREST_HEADERS = {
    'authority': 'everyweb.net',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://everyweb.net',
    'referer': 'https://everyweb.net/pinterest/',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
}
PINTEREST_COOKIES = {
    '_lscache_vary': 'cd11052a02ea53c97b30994ffef5a4b1',
    '_ga_7P1TVF9P7M': 'GS2.1.s1753736522$o1$g0$t1753736522$j60$l0$h0',
    '_ga': 'GA1.1.30758253.1753736522',
    'pll_language': 'ar',
    '__gads': 'ID=e510112a91dffb7c:T=1753736524:RT=1753736524:S=ALNI_MZ3sbceLB32rKNPnoWCLYi6ccl2Xg',
    '__gpi': 'UID=0000111a4db6b81c:T=1753736524:RT=1753736524:S=ALNI_Ma6vm88YHiW8LcyOlTWXlmafYoqTw',
    '__eoi': 'ID=c2055eef46b6fba0:T=1753736524:RT=1753736524:S=AA-Afjatkw_ngmHHvPIurkUp7l9N',
    'FCNEC': '%5B%5B%22AKsRol9AtNttuHht9OxvvFO9Ok96J2IaZLpQu-5py1E6tFSwu2yhdbdoM53f1SzURfR4XU24wRX_AdkxfZ_gu117p4Yr0dxw9EhKPsSc6C3ZPVOaVqfs4Gfe0yUGxrj0brm30K13UfO86KxL-lCngteOv-aGd8p9SA%3D%3D%22%5D%5D',
}

FB_API_URL = "https://fbdownloader.to/api/ajaxSearch"
FB_HEADERS = {
    'authority': 'fbdownloader.to',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://fbdownloader.to',
    'referer': 'https://fbdownloader.to/ar',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
FB_COOKIES = {
    'fpestid': 'TQyMQylz-gvL1kHeSpoed1DZBd_-Y4YBDU4rVgQYEKy2H3fz6rzKpilTTsGNsyjM8XNppw',
}

SNAP_SMART_API_URL = "https://samrt-loader.com/kydwon/api/addfile"
SNAP_SMART_COOKIES = {
    'myCookieConsent': 'true',
    'PHPSESSID': 'lruvkc8ljl99ks5imuc3fsca9u',
}
SNAP_SMART_HEADERS = {
    'authority': 'samrt-loader.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://samrt-loader.com',
    'referer': 'https://samrt-loader.com/ar/snapchat',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
}

SNAPCHAT_API_URL = "https://snapinsta.app/action.php"
SNAPCHAT_HEADERS = {
    'authority': 'snapinsta.app',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://snapinsta.app',
    'referer': 'https://snapinsta.app/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

YOUTUBE_API_URL = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"
YOUTUBE_HEADERS = {
    "x-rapidapi-host": "ytstream-download-youtube-videos.p.rapidapi.com",
    "x-rapidapi-key": "ccbf5c7fb7mshe66aa640fe34327p188362jsn8c8ef10771d3"
}

INSTALOADER = instaloader.Instaloader()

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  date_added TEXT,
                  first_time INTEGER DEFAULT 1,
                  banned INTEGER DEFAULT 0)''') 
    conn.commit()
    conn.close()

def add_user(user):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT first_time FROM users WHERE user_id = ?", (user['id'],))
        existing_user = c.fetchone()
        
        if existing_user:
            c.execute('''UPDATE users SET 
                        username = ?, 
                        first_name = ?, 
                        last_name = ?
                        WHERE user_id = ?''',
                     (user.get('username'), user.get('first_name'), 
                      user.get('last_name'), user['id']))
            
            first_time = existing_user[0]
        else:
            c.execute('''INSERT INTO users 
                        (user_id, username, first_name, last_name, date_added, first_time) 
                        VALUES (?, ?, ?, ?, ?, 1)''',
                     (user['id'], user.get('username'), user.get('first_name'), 
                      user.get('last_name'), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            first_time = 1
        
        conn.commit()
        return first_time
    except Exception as e:
        logger.error(f"Error adding user to DB: {e}")
        return 0
    finally:
        conn.close()

def mark_user_as_old(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET first_time = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Error updating user status: {e}")
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT user_id FROM users WHERE banned = 0")
        return [row[0] for row in c.fetchall()]
    except Exception as e:
        logger.error(f"Error getting users from DB: {e}")
        return []
    finally:
        conn.close()

def get_user_count():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM users WHERE banned = 0")
        return c.fetchone()[0]
    except Exception as e:
        logger.error(f"Error getting user count: {e}")
        return 0
    finally:
        conn.close()

def get_banned_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT user_id FROM users WHERE banned = 1")
        return [row[0] for row in c.fetchall()]
    except Exception as e:
        logger.error(f"Error getting banned users: {e}")
        return []
    finally:
        conn.close()

def ban_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        return False
    finally:
        conn.close()

def unban_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET banned = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error unbanning user: {e}")
        return False
    finally:
        conn.close()

def is_user_banned(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT banned FROM users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] == 1 if result else False
    except Exception as e:
        logger.error(f"Error checking ban status: {e}")
        return False
    finally:
        conn.close()

def get_user_stats():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM users WHERE banned = 0")
        active_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE banned = 1")
        banned_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE date(date_added) = date('now')")
        new_today = c.fetchone()[0]
        
        c.execute("SELECT date_added FROM users ORDER BY date_added LIMIT 1")
        first_user_date = c.fetchone()
        first_user_date = first_user_date[0] if first_user_date else "غير معروف"
        
        return {
            'active_users': active_users,
            'banned_users': banned_users,
            'total_users': active_users + banned_users,
            'new_today': new_today,
            'first_user_date': first_user_date
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return None
    finally:
        conn.close()

init_db()

def safe_filename_from_url(url: str, default: str) -> str:
    try:
        tail = urllib.parse.urlparse(url).path.split('/')[-1]
        if not tail:
            return default
        if '.' not in tail:
            return f"{tail}.bin"
        return tail
    except:
        return default

def download_bytes(url: str, timeout: int = 20) -> bytes:
    r = requests.get(url, stream=True, timeout=timeout)
    r.raise_for_status()
    return r.content

def extract_youtube_id(url: str) -> Optional[str]:
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu.be\/([0-9A-Za-z_-]{11})',
        r'embed\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def send_message(chat_id, text, parse_mode=None, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
    return response.json()

async def send_video(chat_id, video, caption=None, supports_streaming=True, width=None, height=None, duration=None):
    if isinstance(video, str):
        payload = {
            'chat_id': chat_id,
            'video': video,
            'supports_streaming': supports_streaming
        }
        if caption:
            payload['caption'] = caption
        if width:
            payload['width'] = width
        if height:
            payload['height'] = height
        if duration:
            payload['duration'] = duration
        
        response = requests.post(f"{TELEGRAM_API_URL}/sendVideo", json=payload)
    else:
        files = {'video': video}
        data = {
            'chat_id': chat_id,
            'supports_streaming': 'true'
        }
        if caption:
            data['caption'] = caption
        if width:
            data['width'] = str(width)
        if height:
            data['height'] = str(height)
        if duration:
            data['duration'] = str(duration)
        
        response = requests.post(f"{TELEGRAM_API_URL}/sendVideo", files=files, data=data)
    return response.json()

async def send_document(chat_id, document, caption=None, filename=None):
    if isinstance(document, bytes):
        files = {'document': (filename or 'file.bin', BytesIO(document))}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        
        response = requests.post(f"{TELEGRAM_API_URL}/sendDocument", files=files, data=data)
    else:
        files = {'document': document}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        
        response = requests.post(f"{TELEGRAM_API_URL}/sendDocument", files=files, data=data)
    return response.json()

async def delete_message(chat_id, message_id):
    payload = {
        'chat_id': chat_id,
        'message_id': message_id
    }
    response = requests.post(f"{TELEGRAM_API_URL}/deleteMessage", json=payload)
    return response.json()

async def edit_message_text(chat_id, message_id, text, parse_mode=None, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text
    }
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(f"{TELEGRAM_API_URL}/editMessageText", json=payload)
    return response.json()

async def get_chat_member(chat_id, user_id):
    payload = {
        'chat_id': chat_id,
        'user_id': user_id
    }
    response = requests.post(f"{TELEGRAM_API_URL}/getChatMember", json=payload)
    return response.json()

async def answer_callback_query(callback_query_id, text=None, show_alert=False):
    payload = {
        'callback_query_id': callback_query_id
    }
    if text:
        payload['text'] = text
    if show_alert:
        payload['show_alert'] = show_alert
    
    response = requests.post(f"{TELEGRAM_API_URL}/answerCallbackQuery", json=payload)
    return response.json()

async def check_subscription(user_id):
    try:
        result1 = await get_chat_member(CHANNEL_USERNAME, user_id)
        if not result1.get('ok'):
            return False
        
        status1 = result1['result']['status']
        if status1 not in ['member', 'administrator', 'creator']:
            return False
        
        result2 = await get_chat_member(CHANNEL_USERNAME2, user_id)
        if not result2.get('ok'):
            return False
        
        status2 = result2['result']['status']
        if status2 not in ['member', 'administrator', 'creator']:
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        return False

async def send_subscription_message(chat_id):
    subscription_message = (
        "- يجب عليك الاشتراك في قناتي البوت\n"
        f"- اضغط للاشتراك = {CHANNEL_USERNAME}\n"
        f"- ا ضغط للاشتراك = {CHANNEL_USERNAME2}\n"
        "- بعد الاشتراك اضغط /start لتفعيل البوت"
    )
    await send_message(chat_id, subscription_message)

async def send_new_user_info_to_admin(user):
    user_count = get_user_count()
    
    user_info = (
        "مستخدم جديد\n"
        f"الايدي: {user['id']}\n"
        f"الاسم: {user.get('first_name', 'غير معروف')} {user.get('last_name', '')}\n"
        f"اليوزر: @{user.get('username', 'لا يوجد')}\n"
        f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"عدد الاعضاء الكلي: {user_count}"
    )
    
    for developer_id in DEVELOPER_IDS:
        try:
            await send_message(developer_id, user_info)
        except Exception as e:
            logger.error(f"Failed to send user info to developer {developer_id}: {e}")

def create_main_keyboard():
    keyboard = {
        'inline_keyboard': [
            [
                {'text': 'تحميل من اليوتيوب', 'callback_data': 'download_youtube'},
                {'text': 'تحميل من الفيسبوك', 'callback_data': 'download_facebook'}
            ],
            [
                {'text': 'تحميل من الانستا', 'callback_data': 'download_instagram'},
                {'text': 'تحميل من بنترست', 'callback_data': 'download_pinterest'}
            ],
            [
                {'text': 'تحميل من تيك توك', 'callback_data': 'download_tiktok'},
                {'text': 'تحميل من سناب شات', 'callback_data': 'download_snapchat'}
            ],
            [
                {'text': 'المطور', 'url': 'https://t.me/e_1bo'},
                {'text': 'قناة المطور', 'url': 'https://t.me/e_1bo2'}
            ],
            [
                {'text': 'لوحة الادمن', 'callback_data': 'admin_panel'} if DEVELOPER_IDS else None
            ]
        ]
    }
    keyboard['inline_keyboard'] = [row for row in keyboard['inline_keyboard'] if any(btn is not None for btn in row)]
    return keyboard

def create_broadcast_keyboard(message):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'نعم', 'callback_data': f'broadcast_yes_{message}'}],
            [{'text': 'لا', 'callback_data': 'broadcast_no'}]
        ]
    }
    return keyboard

def create_admin_keyboard():
    keyboard = {
        'inline_keyboard': [
            [
                {'text': 'احصائيات البوت', 'callback_data': 'admin_stats'},
                {'text': 'بث للجميع', 'callback_data': 'admin_broadcast'}
            ],
            [
                {'text': 'حظر مستخدم', 'callback_data': 'admin_ban'},
                {'text': 'فك حظر مستخدم', 'callback_data': 'admin_unban'}
            ],
            [
                {'text': 'المستخدمين المحظورين', 'callback_data': 'admin_banned_list'},
                {'text': 'الغاء', 'callback_data': 'admin_cancel'}
            ]
        ]
    }
    return keyboard

def create_platform_selection_keyboard():
    keyboard = {
        'inline_keyboard': [
            [
                {'text': 'يوتيوب', 'callback_data': 'platform_youtube'},
                {'text': 'فيسبوك', 'callback_data': 'platform_facebook'}
            ],
            [
                {'text': 'انستجرام', 'callback_data': 'platform_instagram'},
                {'text': 'بينتيريست', 'callback_data': 'platform_pinterest'}
            ],
            [
                {'text': 'تيك توك', 'callback_data': 'platform_tiktok'},
                {'text': 'سناب شات', 'callback_data': 'platform_snapchat'}
            ],
            [
                {'text': 'رجوع', 'callback_data': 'back_to_main'}
            ]
        ]
    }
    return keyboard

async def handle_start(user, chat_id):
    if is_user_banned(user['id']):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(user['id']):
        await send_subscription_message(chat_id)
        return
    is_new_user = add_user(user)
    if is_new_user == 1:
        await send_new_user_info_to_admin(user)
        mark_user_as_old(user['id'])
    
    welcome_message = (
            "مرحبا بك بوت KANJO لتحميل من جميع مواقع التواصل\n"
            "تحميل بدون حقوق او علامة مائية\n"
            "اختر المنصة التي تريد التحميل منها:"
    )
    
    keyboard = create_main_keyboard()
    await send_message(chat_id, welcome_message, reply_markup=keyboard)

async def handle_send(user, chat_id, args):
    if user['id'] not in DEVELOPER_IDS:
        await send_message(chat_id, "هذا الأمر للمطور فقط")
        return
    
    if not args:
        await send_message(chat_id, "يرجى كتابة الرسالة بعد الأمر /send")
        return
    
    message = ' '.join(args)
    keyboard = create_broadcast_keyboard(message)
    
    await send_message(chat_id, f"هل تريد إرسال هذه الرسالة لجميع المستخدمين؟\n\n{message}", reply_markup=keyboard)

async def handle_admin_panel(chat_id, user_id):
    if user_id not in DEVELOPER_IDS:
        await send_message(chat_id, "هذا الأمر للمطورين فقط")
        return
    
    keyboard = create_admin_keyboard()
    await send_message(chat_id, "لوحة تحكم الادمن", reply_markup=keyboard)

async def handle_admin_stats(chat_id, user_id):
    if user_id not in DEVELOPER_IDS:
        return
    
    stats = get_user_stats()
    if stats:
        stats_text = (
            f"احصائيات البوت:\n"
            f"المستخدمين النشطين: {stats['active_users']}\n"
            f"المستخدمين المحظورين: {stats['banned_users']}\n"
            f"إجمالي المستخدمين: {stats['total_users']}\n"
            f"المستخدمين الجدد اليوم: {stats['new_today']}\n"
            f"تاريخ أول مستخدم: {stats['first_user_date']}"
        )
        await send_message(chat_id, stats_text)
    else:
        await send_message(chat_id, "حدث خطأ في جلب الاحصائيات")

async def handle_admin_ban(chat_id, user_id):
    if user_id not in DEVELOPER_IDS:
        return
    
    await send_message(chat_id, "ارسل ايدي المستخدم الذي تريد حظره\n(يمكنك الحصول على ايدي المستخدم عن طريق @userinfobot)")

async def handle_admin_unban(chat_id, user_id):
    if user_id not in DEVELOPER_IDS:
        return
    
    await send_message(chat_id, "ارسل ايدي المستخدم الذي تريد فك حظره")

async def handle_admin_banned_list(chat_id, user_id):
    if user_id not in DEVELOPER_IDS:
        return
    
    banned_users = get_banned_users()
    if banned_users:
        banned_list = "\n".join([str(uid) for uid in banned_users[:50]])
        message = f"المستخدمين المحظورين:\n{banned_list}"
        if len(banned_users) > 50:
            message += f"\n\nو {len(banned_users) - 50} مستخدم آخر"
        await send_message(chat_id, message)
    else:
        await send_message(chat_id, "لا يوجد مستخدمين محظورين")

async def handle_ban_user(chat_id, admin_id, target_id_str):
    if admin_id not in DEVELOPER_IDS:
        return
    
    try:
        target_id = int(target_id_str)
        if target_id in DEVELOPER_IDS:
            await send_message(chat_id, "لا يمكن حظر المطورين")
            return
        
        if ban_user(target_id):
            await send_message(chat_id, f"تم حظر المستخدم {target_id}")
        else:
            await send_message(chat_id, "حدث خطأ في حظر المستخدم")
    except ValueError:
        await send_message(chat_id, "رقم ايدي غير صالح")

async def handle_unban_user(chat_id, admin_id, target_id_str):
    if admin_id not in DEVELOPER_IDS:
        return
    
    try:
        target_id = int(target_id_str)
        if unban_user(target_id):
            await send_message(chat_id, f"تم فك حظر المستخدم {target_id}")
        else:
            await send_message(chat_id, "حدث خطأ في فك حظر المستخدم")
    except ValueError:
        await send_message(chat_id, "رقم ايدي غير صالح")

async def handle_broadcast_confirmation(callback_query, data):
    await answer_callback_query(callback_query['id'])
    
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    
    if data == 'broadcast_no':
        await edit_message_text(chat_id, message_id, "تم إلغاء الإرسال الشامل")
        return
    
    if data.startswith('broadcast_yes_'):
        message = data[13:]
        users = get_all_users()
        total_users = len(users)
        success_count = 0
        fail_count = 0
        
        await edit_message_text(chat_id, message_id, "جاري الإرسال...")
        
        for user_id in users:
            try:
                await send_message(user_id, message)
                success_count += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                fail_count += 1
                logger.error(f"Failed to send to user {user_id}: {e}")
        
        result_text = (
            f"تم الانتهاء من الإرسال الشامل\n\n"
            f"عدد المستخدمين الكلي: {total_users}\n"
            f"تم الإرسال بنجاح: {success_count}\n"
            f"فشل في الإرسال: {fail_count}"
        )
        await edit_message_text(chat_id, message_id, result_text)

async def handle_platform_selection(callback_query, platform):
    await answer_callback_query(callback_query['id'])
    
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    
    platform_messages = {
        'youtube': "يرجى إرسال رابط يوتيوب للتحميل",
        'facebook': "يرجى إرسال رابط فيسبوك للتحميل",
        'instagram': "يرجى إرسال رابط انستجرام للتحميل",
        'pinterest': "يرجى إرسال رابط بينتيريست للتحميل",
        'tiktok': "يرجى إرسال رابط تيك توك للتحميل",
        'snapchat': "يرجى إرسال رابط سناب شات للتحميل"
    }
    
    if platform in platform_messages:
        await edit_message_text(chat_id, message_id, platform_messages[platform])

async def handle_main_button_click(callback_query, button_data):
    await answer_callback_query(callback_query['id'])
    
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    
    if button_data == 'admin_panel':
        await handle_admin_panel(chat_id, callback_query['from']['id'])
        return
    
    if button_data.startswith('download_'):
        platform = button_data.replace('download_', '')
        
        platform_messages = {
            'youtube': "يرجى إرسال رابط يوتيوب للتحميل",
            'facebook': "يرجى إرسال رابط فيسبوك للتحميل",
            'instagram': "يرجى إرسال رابط انستجرام للتحميل",
            'pinterest': "يرجى إرسال رابط بينتيريست للتحميل",
            'tiktok': "يرجى إرسال رابط تيك توك للتحميل",
            'snapchat': "يرجى إرسال رابط سناب شات للتحميل"
        }
        
        if platform in platform_messages:
            await edit_message_text(chat_id, message_id, platform_messages[platform])
    
    elif button_data == 'back_to_main':
        welcome_message = (
            "مرحبا بك بوت KANJO لتحميل من جميع مواقع التواصل\n"
            "تحميل بدون حقوق او علامة مائية\n"
            "اختر المنصة التي تريد التحميل منها:"
        )
        keyboard = create_main_keyboard()
        await edit_message_text(chat_id, message_id, welcome_message, reply_markup=keyboard)

async def handle_admin_button_click(callback_query, button_data):
    await answer_callback_query(callback_query['id'])
    
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    user_id = callback_query['from']['id']
    
    if button_data == 'admin_stats':
        await handle_admin_stats(chat_id, user_id)
    elif button_data == 'admin_broadcast':
        await send_message(chat_id, "ارسل الرسالة التي تريد بثها لجميع المستخدمين")
    elif button_data == 'admin_ban':
        await handle_admin_ban(chat_id, user_id)
    elif button_data == 'admin_unban':
        await handle_admin_unban(chat_id, user_id)
    elif button_data == 'admin_banned_list':
        await handle_admin_banned_list(chat_id, user_id)
    elif button_data == 'admin_cancel':
        await delete_message(chat_id, message_id)

async def handle_tiktok(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None

    try:
        data = {'q': url, 'lang': 'ar'}
        response = requests.post(
            TIKTOK_API_URL,
            cookies=TIKTOK_COOKIES,
            headers=TIKTOK_HEADERS,
            data=data,
            timeout=20
        )
        response.raise_for_status()
        
        json_data = response.json()
        html_content = json_data.get("data")
        if not html_content:
            raise ValueError("No data in TikTok response")

        soup = BeautifulSoup(html_content, 'html.parser')
        video_tag = soup.find('video')
        video_url = video_tag.get('data-src') if video_tag else None

        if video_url:
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
        else:
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            await send_message(chat_id, "تعذر تحميل الفيديو من تيكتوك")
            
    except Exception as e:
        logger.error(f"TikTok error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_pinterest(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None
    
    try:
        headers_img = {
            'authority': 'api.pinterestdl.io',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
            'origin': 'https://pinterestdl.io',
            'referer': 'https://pinterestdl.io/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        resp = requests.get(PINTEREST_IMG_API, params={'url': url}, headers=headers_img, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            image_url = data.get('imageUrl')
            if image_url:
                content = download_bytes(image_url, timeout=25)
                filename = safe_filename_from_url(image_url, "pinterest.jpg")
                if loading_msg_id:
                    await delete_message(chat_id, loading_msg_id)
                await send_document(chat_id, content, caption="تم التحميل باعلى دقة", filename=filename)
                return

        data_form = {'url': url, 'token': PINTEREST_TOKEN, 'hash': PINTEREST_HASH}
        video_response = requests.post(
            PINTEREST_API_URL,
            cookies=PINTEREST_COOKIES,
            headers=PINTEREST_HEADERS,
            data=data_form,
            timeout=20
        )
        if video_response.status_code == 200:
            jd = video_response.json()
            medias = jd.get('medias') or []
            if medias:
                candidate = None
                for m in medias:
                    if m.get('quality') in ('hd', '720', '1080', '4k'):
                        candidate = m
                        break
                if not candidate:
                    candidate = medias[0]
                video_url = candidate.get('url')
                if video_url:
                    if loading_msg_id:
                        await delete_message(chat_id, loading_msg_id)
                    await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
                    return

        if loading_msg_id:
            await delete_message(chat_id, loading_msg_id)
        await send_message(chat_id, "تعذر تحميل المحتوى من بينتيريست")
    except Exception as e:
        logger.error(f"Pinterest error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_facebook(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None

    try:
        data = {
            'k_exp': '1753825936',
            'k_token': '2ba09b483e6bd112275af34aa9fa4c2a9d53df34a934389b8086bcbffce0a515',
            'p': 'home',
            'q': url,
            'lang': 'ar',
            'v': 'v2',
            'w': '',
        }

        response = requests.post(
            FB_API_URL,
            cookies=FB_COOKIES,
            headers=FB_HEADERS,
            data=data,
            timeout=20
        )
        response.raise_for_status()
        json_data = response.json()
        if json_data.get('status') != 'ok':
            raise ValueError("Facebook API returned non-ok status")
        
        soup = BeautifulSoup(json_data['data'], 'html.parser')
        video_url = None
        
        for quality in ['720p (HD)', '360p (SD)']:
            link = soup.find('a', {'title': f'Download {quality}'})
            if link and 'href' in link.attrs:
                video_url = link['href']
                break
        
        if not video_url:
            video_tag = soup.find('video')
            if video_tag and 'src' in video_tag.attrs:
                video_url = video_tag['src']
        
        if video_url:
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
        else:
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            await send_message(chat_id, "تعذر تحميل الفيديو من فيسبوك")
            
    except Exception as e:
        logger.error(f"Facebook error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_instagram(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'outtmpl': 'instagram_%(id)s.%(ext)s',
            'socket_timeout': 15,
            'no_check_certificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            
            if info.get('duration', 0) > 0:
                ydl.download([url])
                filename = ydl.prepare_filename(info)
                if loading_msg_id:
                    await delete_message(chat_id, loading_msg_id)
                with open(filename, 'rb') as video_file:
                    await send_video(
                        chat_id, 
                        video_file, 
                        caption="تم التحميل باعلى دقة",
                        width=info.get('width'),
                        height=info.get('height'),
                        duration=info.get('duration')
                    )
                try:
                    os.remove(filename)
                except: pass
            else:
                if loading_msg_id:
                    await delete_message(chat_id, loading_msg_id)
                img_url = info['url']
                content = download_bytes(img_url, timeout=25)
                filename = safe_filename_from_url(img_url, "instagram.jpg")
                await send_document(chat_id, content, caption="تم التحميل باعلى دقة", filename=filename)
                
    except yt_dlp.DownloadError as e:
        logger.error(f"Instagram ytdlp error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass
        
        try:
            shortcode = re.search(r'/p/([^/]+)', url) or re.search(r'/reel/([^/]+)', url)
            if shortcode:
                post = instaloader.Post.from_shortcode(INSTALOADER.context, shortcode.group(1))
                if post.is_video:
                    await send_video(chat_id, post.video_url, caption="تم التحميل باعلى دقة")
                else:
                    content = download_bytes(post.url, timeout=25)
                    filename = safe_filename_from_url(post.url, "instagram.jpg")
                    await send_document(chat_id, content, caption="تم التحميل باعلى دقة", filename=filename)
        except Exception as ee:
            logger.error(f"Instagram fallback error: {ee}")
    except Exception as e:
        logger.error(f"Instagram error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_snapchat(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None

    try:
        payload = {'file_name': url}
        try:
            r = requests.post(
                SNAP_SMART_API_URL,
                cookies=SNAP_SMART_COOKIES,
                headers=SNAP_SMART_HEADERS,
                json=payload,
                timeout=20
            )
            jd = r.json()
            if jd.get('success') and 'files' in jd:
                video_url = None
                
                for f in jd['files']:
                    if f.get('resolution_type') == 'mp4/hd' and f.get('file'):
                        video_url = f['file']
                        break
                
                if not video_url:
                    for f in jd['files']:
                        if f.get('file'):
                            video_url = f['file']
                            break
                if video_url:
                    if loading_msg_id:
                        await delete_message(chat_id, loading_msg_id)
                    await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
                    return
        except Exception as e:
            logger.warning(f"Snapchat smart-loader failed: {e}")

        data = {'url': url, 'action': 'post'}
        response = requests.post(
            SNAPCHAT_API_URL,
            headers=SNAPCHAT_HEADERS,
            data=data,
            timeout=20
        )
        response.raise_for_status()
        json_data = response.json()
        if json_data.get('status') == 'success' and 'url' in json_data:
            video_url = json_data['url']
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
            return

        if loading_msg_id:
            await delete_message(chat_id, loading_msg_id)
        await send_message(chat_id, "تعذر تحميل المحتوى من سناب شات")
    except Exception as e:
        logger.error(f"Snapchat error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_youtube(chat_id, url, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    if not await check_subscription(chat_id):
        await send_subscription_message(chat_id)
        return
    
    loading_msg = await send_message(chat_id, "انتظر جارِ التحميل")
    loading_msg_id = loading_msg.get('result', {}).get('message_id') if loading_msg.get('ok') else None

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'outtmpl': 'youtube_%(id)s.%(ext)s',
            'socket_timeout': 15,
            'no_check_certificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            filename = ydl.prepare_filename(info)
            if loading_msg_id:
                await delete_message(chat_id, loading_msg_id)
            with open(filename, 'rb') as video_file:
                await send_video(
                    chat_id, 
                    video_file, 
                    caption="تم التحميل باعلى دقة",
                    width=info.get('width'),
                    height=info.get('height'),
                    duration=info.get('duration')
                )
            try:
                os.remove(filename)
            except: pass
            
    except yt_dlp.DownloadError as e:
        logger.error(f"YouTube ytdlp error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass
        
        try:
            video_id = extract_youtube_id(url)
            if video_id:
                api_url = f"{YOUTUBE_API_URL}?id={video_id}"
                response = requests.get(api_url, headers=YOUTUBE_HEADERS, timeout=20)
                response.raise_for_status()
                data = response.json()
                if data.get('status') != 'fail' and 'formats' in data and len(data['formats']) > 0:
                    video_url = data['formats'][0]['url']
                    await send_video(chat_id, video_url, caption="تم التحميل باعلى دقة")
        except Exception as e2:
            logger.error(f"YouTube fallback error: {e2}")
    except Exception as e:
        logger.error(f"Unexpected YouTube error: {e}")
        if loading_msg_id:
            try:
                await delete_message(chat_id, loading_msg_id)
            except: pass

async def handle_message(user, chat_id, text, message_id=None):
    if is_user_banned(chat_id):
        await send_message(chat_id, "تم حظرك من استخدام البوت")
        return
    
    add_user(user)
    
    if not text.startswith(('http://', 'https://')):
        if user['id'] in DEVELOPER_IDS and text.isdigit():
            return
        
        return
    
    try:
        low = text.lower()
        if "tiktok.com" in low:
            await handle_tiktok(chat_id, text, message_id)
        elif "pin.it" in low or "pinterest.com" in low:
            await handle_pinterest(chat_id, text, message_id)
        elif "facebook.com" in low:
            await handle_facebook(chat_id, text, message_id)
        elif "instagram.com" in low:
            await handle_instagram(chat_id, text, message_id)
        elif "snapchat.com" in low:
            await handle_snapchat(chat_id, text, message_id)
        elif "youtube.com" in low or "youtu.be" in low:
            await handle_youtube(chat_id, text, message_id)
        else:
            await send_message(
                chat_id,
                "الرابط غير مدعوم. الروابط المدعومة:\n"
                "TikTok, Instagram, Facebook, YouTube, Pinterest, Snapchat"
            )
    except Exception as e:
        logger.error(f"Router error (user {user['id']}): {e}")

admin_actions = {}


async def process_update(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        user = message.get('from', {})
        
        if 'text' in message:
            text = message['text'].strip()
            message_id = message.get('message_id')
            
            if user['id'] in DEVELOPER_IDS and text.isdigit():
                if chat_id in admin_actions:
                    action = admin_actions[chat_id]
                    if action == 'ban':
                        await handle_ban_user(chat_id, user['id'], text)
                        del admin_actions[chat_id]
                        return
                    elif action == 'unban':
                        await handle_unban_user(chat_id, user['id'], text)
                        del admin_actions[chat_id]
                        return
            
            if text.startswith('/start'):
                await handle_start(user, chat_id)
            elif text.startswith('/send'):
                args = text.split()[1:]
                await handle_send(user, chat_id, args)
            elif text.startswith('/admin'):
                await handle_admin_panel(chat_id, user['id'])
            else:
                await handle_message(user, chat_id, text, message_id)
    
    elif 'callback_query' in update:
        callback_query = update['callback_query']
        data = callback_query.get('data')
        
        if data:
            if data.startswith('broadcast_'):
                await handle_broadcast_confirmation(callback_query, data)
            elif data.startswith('download_') or data == 'back_to_main' or data == 'admin_panel':
                await handle_main_button_click(callback_query, data)
            elif data.startswith('platform_'):
                platform = data.replace('platform_', '')
                await handle_platform_selection(callback_query, platform)
            elif data.startswith('admin_'):
                await handle_admin_button_click(callback_query, data)
                if data == 'admin_ban':
                    admin_actions[callback_query['message']['chat']['id']] = 'ban'
                elif data == 'admin_unban':
                    admin_actions[callback_query['message']['chat']['id']] = 'unban'
                elif data == 'admin_cancel':
                    if callback_query['message']['chat']['id'] in admin_actions:
                        del admin_actions[callback_query['message']['chat']['id']]

async def get_updates(offset=None):
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params)
        data = response.json()
        if data.get('ok'):
            return data['result']
        return []
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return []

async def main():
    logger.info("Bot started...")
    offset = None
    
    while True:
        try:
            updates = await get_updates(offset)
            for update in updates:
                offset = update['update_id'] + 1
                await process_update(update)
        
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
