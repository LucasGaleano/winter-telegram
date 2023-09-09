import logging
import time
from telegram import Update, BotCommand, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ExtBot, CallbackContext
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
    level=logging.WARNING
)

story =  Narrative()
game = Game(Community(), story)
repo = Repo('winter','mongodb://localhost')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    context.job_queue.run_repeating(check_tasks, interval=5, chat_id=update.effective_chat.id)
   
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Start game")


async def barricade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    repo.add_task(owner=get_owner(update), type=Task.BUILD_BARRICADE.value)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{get_owner(update)} is {Task.BUILD_BARRICADE.value.description}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = game.get_status_community()
    message = f"Community:\nDefense: {status['defense']}\nFood: {status['food']}"
    message += "\n\n"
    for survivor in game.survivors:
        if survivor.location:
            message += f"{survivor.name} at the {survivor.location.name}"
    message += "\n\n"
    message += f"Tasks:\n"
    tasks = repo.get_all_progress_task()
    messageTasks = '\n'.join([f"{task.owner} is {task.type.description} [{task.time_remaind()}]" for task in tasks])
    if messageTasks:
        message += messageTasks
    else:
        message += "No one is working"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def travelhostipal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    repo.add_task(owner=get_owner(update), type=Task.TRAVELHOSPITAL.value)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=story.travelling('Hospital', get_owner(update)))


async def check_tasks(context: ContextTypes.DEFAULT_TYPE):
    print('tasks checked')
    currentTasks = repo.get_all_progress_task()
    gameChangesMessage = ''
    for currentTask in currentTasks:
        if currentTask.is_finish():
            currentTask.complete()
            repo.update_task(currentTask)
            gameChangesMessage = game.event_happen(currentTask)           
    for s in game.survivors:
        if s.name not in [task.owner for task in currentTasks] and s.location != None:
            repo.add_task(owner=s.name, type=Task.SEARCH.value)

    if gameChangesMessage:
        await context.bot.send_message(chat_id=context._chat_id, text=gameChangesMessage)

async def check_new_survivor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    survivorName = get_owner(update)
    if game.is_new_survivor(survivorName):
        game.add_survivor(Survivor(survivorName))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=story.new_arrived(survivorName))

def get_owner(update:Update):
    return update.message.from_user.first_name


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('winter.conf')
    application = ApplicationBuilder().token(config['auth']['token']).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('barricade', barricade))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('travelhostipal', travelhostipal))
    application.add_handler(CommandHandler('travelhostipal', travelhostipal))

    application.run_polling()

    print(application.updater.bot.first_name )

'''
start - start new game
barricade - build a barricade
status - check the community status
travelhostipal - travel to hospital
'''


'''
     Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Lucas', id=197827455, last_name='Galeano', type=<ChatType.PRIVATE>, username='lucasgaleano'), date=datetime.datetime(2023, 9, 1, 13, 53, 37, tzinfo=<UTC>), delete_chat_photo=False, entities=(MessageEntity(length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),), from_user=User(first_name='Lucas', id=197827455, is_bot=False, language_code='es', last_name='Galeano', username='lucasgaleano'), group_chat_created=False, message_id=9, supergroup_chat_created=False, text='/start'), update_id=196617858)  
'''