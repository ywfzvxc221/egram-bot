import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7671969883:AAFTIg9zcYr9upvul77Zi715H_U9a_fNT4I'
FaucetPay_wallet = 'EQD14kgmngE0fNYVs7_9dw78V3rPhNt7_Ee-7X3ykDORQvMp'
Telegram_Channel = 'https://t.me/qqwweerrttqqyyyy'

bot = telebot.TeleBot(TOKEN)

admin_user_id = 5475256932  # معرفك

# سؤال واحد فقط للتجربة
question = {
    "text": "ما هو لون السماء في النهار؟",
    "options": ["أزرق", "أحمر", "أخضر"],
    "answer": "أزرق"
}

# قائمة المستخدمين
users = {}

# دالة فحص إذا المستخدم أدمن
def is_admin(user_id):
    return user_id == admin_user_id

# دالة فحص الاشتراك بالقناة
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(chat_id="@qqwweerrttqqyyyy", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(e)
        return False

# القائمة الرئيسية
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ابدأ الاختبار"))
    markup.add(KeyboardButton("رصيدي"), KeyboardButton("مساعدة"))
    markup.add(KeyboardButton("دعوة الأصدقاء"), KeyboardButton("سحب الأرباح"))
    markup.add(KeyboardButton("نشر إعلان"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="اشترك في القناة", url=Telegram_Channel)
        markup.add(btn)
        bot.send_message(message.chat.id, "❌ يجب عليك الاشتراك أولاً في القناة.", reply_markup=markup)
        return

    bot.send_message(message.chat.id, "مرحباً بك في بوت الاختبار!", reply_markup=main_menu())
    users.setdefault(user_id, {"points": 0})

@bot.message_handler(func=lambda m: m.text == "ابدأ الاختبار")
def ask_question(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="اشترك في القناة", url=Telegram_Channel)
        markup.add(btn)
        bot.send_message(message.chat.id, "❌ يجب عليك الاشتراك أولاً.", reply_markup=markup)
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in question["options"]:
        markup.add(KeyboardButton(option))
    bot.send_message(message.chat.id, question["text"], reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in question["options"])
def handle_answer(message):
    user_id = message.from_user.id
    if message.text == question["answer"]:
        users[user_id]["points"] += 1
        bot.send_message(message.chat.id, "✅ إجابة صحيحة! حصلت على 0.00002000 TON.")
    else:
        bot.send_message(message.chat.id, "❌ إجابة خاطئة.")

@bot.message_handler(func=lambda m: m.text == "رصيدي")
def my_balance(message):
    user_id = message.from_user.id
    points = users.get(user_id, {}).get("points", 0)
    bot.send_message(message.chat.id, f"رصيدك: {points} نقطة.")

@bot.message_handler(func=lambda m: m.text == "مساعدة")
def help_command(message):
    bot.send_message(message.chat.id, "اضغط 'ابدأ الاختبار' للإجابة على الأسئلة وكسب مكافآت!")

@bot.message_handler(func=lambda m: m.text == "دعوة الأصدقاء")
def invite_friends(message):
    user_id = message.from_user.id
    invite_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.send_message(message.chat.id, f"✅ شارك رابط الدعوة الخاص بك:\n{invite_link}\nكل صديق يسجل عبر رابطك قد تحصل على مكافأة!")

@bot.message_handler(func=lambda m: m.text == "سحب الأرباح")
def withdraw_earnings(message):
    bot.send_message(message.chat.id, "✅ لسحب أرباحك، أرسل عنوان محفظتك على FaucetPay مع المبلغ المطلوب وسيتم المراجعة.")

@bot.message_handler(func=lambda m: m.text == "نشر إعلان")
def publish_ad(message):
    bot.send_message(message.chat.id, "✅ لنشر إعلانك، تواصل مع إدارة البوت، أو أرسل تفاصيل إعلانك هنا ليتم التواصل معك.")

bot.infinity_polling()
