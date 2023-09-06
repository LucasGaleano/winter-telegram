import logging
import time
from telegram import Update, BotCommand, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ExtBot
from threading import Thread
from repo import Repo, CurrentTask, Task
from narrative import Narrative
import asyncio
from game import Game
from community import Community
from survivor import Survivor
import configparser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

story =  Narrative()
game = Game(Community(), story)
repo = Repo('winter','mongodb://localhost')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_my_commands([BotCommand("statustasks","check what everyone is doing"),
                                       BotCommand("statuscommunity","check the community status"),
                                       BotCommand("barricade","build a barricade"),
                                       BotCommand("travelhostipal","travel to hospital")])
    
    Thread(target=monitor_events, args=[5, context.bot, update.effective_chat.id]).start()
    print(update)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Start game")


async def barricade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    repo.add_task(owner=get_owner(update), type=Task.BUILD_BARRICADE.value)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{get_owner(update)} is {Task.BUILD_BARRICADE.value.description}")

async def statustasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    tasks = repo.get_all_progress_task()
    message = '\n'.join([f"{task.owner} is {task.type.description} [{task.time_remaind()}]" for task in tasks])
    if not message:
        message = "No one is working"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def statusCommunity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = game.get_status_community()
    message = f"Defense: {status['defense']}\nFood: {status['food']}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def travelhostipal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)


    await context.bot.send_message(chat_id=update.effective_chat.id, text=story.travelling('Hospital', get_owner(update)))


def monitor_events(checking_time:int, bot:ExtBot, chat_id:int):
    asyncio.run(check_tasks(checking_time, bot, chat_id))

async def check_tasks(checking_time:int, bot:ExtBot, chat_id:int):
    while True:
        print('tasks checked')
        currentTasks = repo.get_all_progress_task()
        for currentTask in currentTasks:
            if currentTask.is_finish():
                currentTask.complete()
                repo.update_task(currentTask)
                gameChangesMessage = game.event_happen(currentTask)                
                await bot.send_message(chat_id=chat_id, text=gameChangesMessage)
                
        time.sleep(checking_time)

# async def mention_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = f"[{update.message.from_user.username}](https://t.me/{update.message.from_user.username})"
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def check_new_survivor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if game.is_new_survivor(update.message.chat.first_name):
        game.add_survivor(Survivor(update.message.chat.first_name))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=story.new_arrived(update.message.chat.first_name))

def get_owner(update:Update):
    return update.message.from_user.first_name


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('winter.conf')
    application = ApplicationBuilder().token(config['auth']['token']).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('barricade', barricade))
    application.add_handler(CommandHandler('statustasks', statustasks))
    application.add_handler(CommandHandler('statuscommunity', statusCommunity))
    application.add_handler(CommandHandler('travelhostipal', travelhostipal))
    # application.add_handler(CommandHandler('mention_user', mention_user))

    application.run_polling()

    print(application.updater.bot.first_name )

'''
     Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Lucas', id=197827455, last_name='Galeano', type=<ChatType.PRIVATE>, username='lucasgaleano'), date=datetime.datetime(2023, 9, 1, 13, 53, 37, tzinfo=<UTC>), delete_chat_photo=False, entities=(MessageEntity(length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),), from_user=User(first_name='Lucas', id=197827455, is_bot=False, language_code='es', last_name='Galeano', username='lucasgaleano'), group_chat_created=False, message_id=9, supergroup_chat_created=False, text='/start'), update_id=196617858)  
'''