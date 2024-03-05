# @SHAHM4 & @LGGBG
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button, Message, CallbackQuery
from telebot import types
from funcs import read, write
import random
import time
import os
import threading
import requests
bot_token = "6687297679:AAFASy6GPjoBqe_mblpeVwvd3_SIGPViv3A"
bot = TeleBot(bot_token, parse_mode="Markdown")
db_path = "MillionUsers.json"
db_bests = "Millioners.json"
db_questions = "questions.json"


@bot.message_handler(commands=["start", "million","العب"])
@bot.message_handler(func=lambda message: message.text == "المليون")
def start(message: Message):
    user_id = message.from_user.id
    user = message.from_user.first_name if not message.from_user.last_name else message.from_user.first_name + message.from_user.last_name
    url = f"https://api.telegram.org/bot{bot_token}/getchatmember?chat_id=@bgglg&user_id={user_id}"
    req = requests.get(url)
    if 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        if str(user_id) not in users:
            users[str(user_id)] = {
                "budget": 0,
            }
            write(db_path, users)
        best_list = read(db_bests)
        best_players = "".join(best_list)
        caption = f"""
مرحبا بك عزيزي {user} في لعبة من سيربح المليون

قائمة أفضل لاعبين :\n\n
{best_players}
"""
        markup = Keyboard(
            [  # @SHAHM & @LGGBG
                [
                    Button("- قواعد اللعبة -", callback_data=f"rules-{user_id}"),
                    Button("- إبدأ اللعب -", callback_data=f"play-{user_id}")
                ],
                [
                    Button("- المطور -", "SHAHM4.t.me")
                ]
            ]
        )
        bot.reply_to(
            message,
            caption,
            reply_markup=markup
        )
    else:
        bot.delete_message(message.chat.id, message.message_id)
        f2 = message.from_user.first_name
        t2 = message.from_user.username
        n = bot.get_chat("@bgglg").title
        mar = f"""[{n}](t.me/bgglg)"""
        k = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton(f"{n}", url=f"t.me/lggbg")
        k.add(k1)
        bot.send_message(message.chat.id, """ *عزيزي  - *[{}](t.me/{})  
        لا يمكنك البدء في اللعبة لأنك غير مشترك في قناة المجموعة ؛ ✅
        عليك الاشتراك في قناة : {}""".format(f2, t2, mar), disable_web_page_preview=True, parse_mode="markdown", reply_markup=k)


@bot.callback_query_handler(func= lambda callback: "rules" in callback.data)
def rules(callback: CallbackQuery):
    data = callback.data.split("-")
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id 
    if user_id != int(data[1]):
        bot.answer_callback_query(callback.id, "هو انت منيلك المعلومات حتا تريد تاخذ المليون👀", show_alert=True)
        return
    caption = """
• ليدك 15 سؤالأ يمكنك الإجابه عنهم.

• كل سؤال له وقت محدد للإجابه ( 60 ثانيه ).

• كل سؤال جاوبه صح تحصل فلوس

• اذا قمت بإجابه خاطئه سيتم اقصاءك من اللعبة

• عند الوصول للمليون سيتم اضافتك لقائمة الاشراف
"""
    markup = Keyboard(
        [
            [
                Button("- العوده -", callback_data=f"million_start-{user_id}")
            ]
        ]# SHAHM4 & @BGGlG
    )
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=callback.message.id,
        text=caption,
        reply_markup=markup
    )
    

@bot.callback_query_handler(func= lambda callback: "million_start" in callback.data)
def restart(callback: CallbackQuery):
    data = callback.data.split("-")
    user_id = callback.from_user.id
    user = callback.from_user.first_name if not callback.from_user.last_name else callback.from_user.first_name + callback.from_user.last_name
    if user_id != int(data[1]):
        bot.answer_callback_query(callback.id, "هو انت منيلك معلومات حتا تريد تاخذ المليون 👀", show_alert=True)
        return
    best_list = read(db_bests)
    best_players = "".join(best_list)
    caption = f"""
مرحبا بك عزيزي {user} في لعبة من سيربح المليون

قائمة أفضل لاعبين :\n\n
{best_players}
"""
    markup = Keyboard(
        [ 
            [
                Button("- قواعد اللعبه -", callback_data=f"rules-{user_id}"),
                Button("- إبدأ اللعب -", callback_data=f"play-{user_id}")
            ],
            [
                Button("- المطور -", "SHAHM4.t.me")
            ]
        ]
    )
    bot.edit_message_text(
        message_id=callback.message.id, 
        chat_id=callback.message.chat.id,
        text=caption,
        reply_markup=markup
    )# @SHAHM4 & @BGGlG


@bot.callback_query_handler(func= lambda callback: "play" in callback.data)
def play(callback: CallbackQuery):
    data = callback.data.split("-")
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    user = callback.from_user.first_name if not callback.from_user.last_name else callback.from_user.first_name + callback.from_user.last_name
    if user_id != int(data[1]):
        bot.answer_callback_query(callback.id, "هو انت منيلك معلومات حتا تريد تاخذ المليون 👀", show_alert=True)
        return
    random.shuffle(questions)
    card = random.choice(questions)
    question = card["question"]
    options = card["options"]
    answer = card["correct_option"]
    random.shuffle(options)
    markup = []
    for index in range(0, len(options), 2):
        markup.append([
            Button(options[index], callback_data=f"answer_{'True-' + answer if options[index] == answer else False}-{user_id}"),
            Button(options[index+1], callback_data=f"answer_{'True-' + answer if options[index+1] == answer else False}-{user_id}")
        ])# @SHAHM4 & @BGGlG
    caption = f"""
- اللاعب {user}
- فلوسك : {users[str(user_id)]["budget"]}

- السؤال :
{question}
"""
    thread_id = str(random.randint(2872, 38636299))
    markup.append([Button("60 sec", callback_data=thread_id)])
    sent_message = bot.edit_message_text(
        message_id=callback.message.id, 
        chat_id=chat_id,
        text=caption, 
        reply_markup=Keyboard(markup),
    )
    threads[str(thread_id)] = True
    thread = threading.Thread(
        target=loop, 
        args=(sent_message, thread_id,),
    )
    thread.start()
# @SHAHM4 & @BGGlG

@bot.callback_query_handler(func= lambda callback: "answer" in callback.data)
def get_answer(callback: CallbackQuery):
    try:
        thread_id = callback.message.reply_markup.keyboard[-1][0].callback_data
        threads[thread_id] = False
    except IndexError:
        pass
    data = callback.data.split("-")
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    user = callback.from_user.first_name if not callback.from_user.last_name else callback.from_user.first_name + callback.from_user.last_name
    if user_id != int(data[-1]):
        bot.answer_callback_query(callback.id, "هو انت منيلك معلومات حتا تريد تاخذ المليون 👀", show_alert=True)
        return
    budget = users[str(user_id)]["budget"]
    new_markup = Keyboard(
            [
                [
                    Button("- قواعد اللعبه -", callback_data=f"rules-{user_id}"),
                    Button("- إلعب من جديد -", callback_data=f"play-{user_id}")
                ],
                [
                    Button("- المطور -", "SHAHM4.t.me")
                ]
            ]
        )
    if "False" in data[0]:
        users[str(user_id)]["budget"] = 0
        write(db_path, users)
        caption = f"""
- اللاعب {user}
- آجابه خاطئه
- تم اقصاءك من اللعبة
"""
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.id, 
            text=caption, 
            reply_markup=new_markup
        )
        return
    if budget in (0 ,200):
      budget += 100
    elif budget not in (64000, 300):
        budget = budget * 2
    elif budget == 300:
        budget += 200
    elif budget == 64000:
        budget += 61000
        # @SHAHM4 & @BGGlG
    if budget == 1000_000:
        users[str(user_id)]["budget"] = budget
        write(db_path, users)
        bests[f"- {user_id}"] = budget
        write(db_bests, bests)
        caption =f"""
- اللاعب {user}
-الف مبروك لقد ربحت المليلون
- اصبحت فلوسك :  {users[str(user_id)]["budget"]}
- تمت إضافك إلى قائمة أفضل اللاعبين.
- سيظهر الأيدي الخاص بك عندما تضغط /start
"""
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.id, 
            text=caption,
            reply_markup=new_markup
        )
        return
        # @SHAHM4 & @BGGlG
    users[str(user_id)]["budget"] = budget
    write(db_path, users)
    random.shuffle(questions)
    card = random.choice(questions)
    question = card["question"]
    options = card["options"]
    answer = card["correct_option"]
    random.shuffle(options)
    markup = []
    for index in range(0, len(options), 2):
        markup.append([
            Button(options[index], callback_data=f"answer_{'True ' + answer if options[index] == answer else False}-{user_id}"),
            Button(options[index+1], callback_data=f"answer_{'True ' + answer if options[index+1] == answer else False}-{user_id}")
        ])
    caption = f"""
- اللاعب {user}
- إجابه صحيحه.
- فلوسك : {users[str(user_id)]["budget"]}

- السؤال :
{question}
"""
    thread_id = str(random.randint(2872, 38636299))
    markup.append([Button("60 sec", callback_data=thread_id)])
    sent_message = bot.edit_message_text(
        message_id=callback.message.id, 
        chat_id=chat_id,
        text=caption, 
        reply_markup=Keyboard(markup),
    )
    threads[str(thread_id)] = True
    thread = threading.Thread(
        target=loop, 
        args=(sent_message, thread_id,),
    )
    thread.start()
# @SHAHM4 & @BGGlG

def loop(message: Message, thread_id):
    message_id = message.id
    chat = message.chat.id
    timer = 60
    timed = threads.get(thread_id)
    markup = message.reply_markup.keyboard
    user_id = markup[0][0].callback_data.split("-")[-1]
    if timed:
        while True:
            if not threads.get(thread_id):
                break
            if timer != 0:
                time.sleep(1)
                timer -= 1
                sec = timer
                markup[-1][0].text = f" {sec} sec"
                markup[-1][0].callback_data = thread_id
                # @SHAHM4 & @BGGlG
                if not threads.get(thread_id):
                    break
                bot.edit_message_reply_markup(
                    chat_id= chat,
                    message_id = message_id,
                    reply_markup = Keyboard(markup),
                )
                continue
            threads[thread_id] = False
            user = message.from_user.first_name if not message.from_user.last_name else message.from_user.first_name + message.from_user.last_name
            caption = f"""
- اللاعب {user}
- آجابه خاطئه
- تم اقصاءك من اللعبة
"""
            bot.edit_message_text(
                chat_id= chat,
                message_id = message_id,
                text=caption,
                reply_markup=Keyboard(
                    [
                        [
                            Button("- قواعد اللعبه -", callback_data=f"rules-{user_id}"),
                            Button("- إلعب من جديد -", callback_data=f"play-{user_id}")
                        ],
                        [
                            Button("- المطور -", "SHAHM4.t.me")
                        ]
                    ]
                ))
            return
    return


def dbs_checker(dbs):
    for db in dbs:
        if not os.path.exists(db):
            write(db, {})


dbs_checker([db_path, db_bests])
users = read(db_path)
questions = read(db_questions)
bests = read(db_bests)
threads = {}
A='تم تشغيل البوت'
G='مطور البوت https://t.me/SHAHM4'
print(A,'',G)
bot.infinity_polling()
