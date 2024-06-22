import logging
import time
from telegram import Update, BotCommand, Bot, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ExtBot, CallbackContext
from threading import Thread
from repo import Repo, CurrentTask, Task, TaskType
from narrative import Narrative
import asyncio
from game import Game
from community import Community
from survivor import Survivor
import copy
import configparser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

story =  Narrative('es')
game = Game(Community(), story)
repo = Repo('winter','mongodb://localhost')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    context.job_queue.run_repeating(check_tasks, interval=5, chat_id=update.effective_chat.id)
    await send_message(context, text="Start Game")
    # await add_command(context, 'traveltown','testing command', travel)

    #print(await context.bot.send_dice(chat_id=context._chat_id, emoji=constants.DiceEmoji.DARTS))
    #print(await context.bot.send_poll(chat_id=context._chat_id, question="run?", options=["no","yes"], open_period=20))
    #print(update)🏥🧟

async def barricade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    if has_active_task(get_owner(update)):
        await send_message(context, text=f"You are currently engaged in a task.")
        return None
    await stop_passive_task(update, context)

    add_task(owner=get_owner(update), type=Task.BUILD_BARRICADE.value)
    await send_message(context, text=f"{get_owner(update)} is {Task.BUILD_BARRICADE.value.description}")

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    if has_active_task(get_owner(update)):
        await send_message(context, text=f"You are currently engaged in a task.")
        return None
    await stop_passive_task(update, context)

    add_task(owner=get_owner(update), type=Task.EXPLORE.value)
    await send_message(context, text=f"{get_owner(update)} is {Task.EXPLORE.value.description}")

async def travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    if has_active_task(get_owner(update)):
        await send_message(context, text=f"You are currently engaged in a task.")
        return None    
    await stop_passive_task(update, context)
    #print(update.message.text) # /travellocation
    location = update.message.text.split('/travel')[1]

    taskTypeTravel = copy.copy(Task.TRAVEL.value)
    taskTypeTravel.description = f"travelling to the {location}"
    taskTypeTravel.location = location
    add_task(owner=get_owner(update), type=taskTypeTravel)
    await send_message(context, text=story.travelling(location, get_owner(update)))

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_new_survivor(update, context)
    message = game.show_status_community()
    message += "\n\n"
    for survivor in game.survivors:
        if survivor.location:
            message += survivor.show_location()
            message += '\n'
    message += "\n\n"
    message += f"Tasks:\n"
    tasks = repo.get_all_progress_task()
    messageTasks = '\n'.join([f"{task.type.emoji} {task.owner} is {task.type.description} [{task.time_remaind()}]" for task in tasks if not task.type.passive])
    messageTasks += '\n'.join([f"{task.type.emoji} {task.owner} is {task.type.description}..." for task in tasks if task.type.passive])
    if messageTasks:
        message += messageTasks
    else:
        message += "No one is working"
    await send_message(context, text=message)


async def check_tasks(context: ContextTypes.DEFAULT_TYPE):
    print('tasks checked')
    currentTasks = repo.get_all_progress_task()
    gameChangesMessage = ''
    for currentTask in currentTasks:
        if currentTask.is_finish():
            currentTask.complete()
            repo.update_task(currentTask)
            gameChangesMessage = game.event_happen(currentTask)
            # if gameChangesMessage.startswith("found a"):
            #     newLocation = gameChangesMessage.split()[2]
            #     await add_command(context, f'travel{newLocation}',f'travel to {newLocation}', travel)
    for s in game.survivors:
        if not has_task(s.name) and s.location != None:
            add_task(owner=s.name, type=Task.SEARCH.value)


    if gameChangesMessage:
        await send_message(context, text=gameChangesMessage)

async def check_new_survivor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    survivorName = get_owner(update)
    if game.is_new_survivor(survivorName):
        game.add_survivor(Survivor(survivorName))
        await send_message(context, text=story.new_arrived(survivorName))

async def stop_passive_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.delete_all_passive_task_by_owner(get_owner(update))

def has_task(owner: str):
    return repo.get_all_progress_task_by_owner(owner)

def has_active_task(owner:str):
    return any([not currentTask.type.passive for currentTask in repo.get_all_progress_task_by_owner(owner)])

def get_owner(update:Update):
    return update.message.from_user.first_name

def add_task(owner:str, type=TaskType):
    repo.add_task(owner=owner, type=type)

async def send_message(context: ContextTypes.DEFAULT_TYPE, text: str, update: Update = None, ):
    #escaping characters for markdown.
    text = text.replace('.','\.').replace('[','\[').replace(']','\]').replace('+','\+').replace('-','\-')
    await context.bot.send_message(chat_id=context._chat_id, text=text, parse_mode=constants.ParseMode.MARKDOWN_V2)

async def add_command(context: ContextTypes.DEFAULT_TYPE, command: str, description: str, callback):
    commands = list(await context.bot.getMyCommands())
    commands.append(BotCommand(command,description))
    await context.bot.setMyCommands(commands)
    application.add_handler(CommandHandler(command, callback))
    print(f"new command added {command} - {description}")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('winter.conf')
    application = ApplicationBuilder().token(config['auth']['token']).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('barricade', barricade))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('explore', explore))
    # application.add_handler(CommandHandler('travelhospital', travel))
    print('start')

    application.run_polling()


'''
     Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Lucas', id=197827455, last_name='Galeano', type=<ChatType.PRIVATE>, username='lucasgaleano'), date=datetime.datetime(2023, 9, 1, 13, 53, 37, tzinfo=<UTC>), delete_chat_photo=False, entities=(MessageEntity(length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),), from_user=User(first_name='Lucas', id=197827455, is_bot=False, language_code='es', last_name='Galeano', username='lucasgaleano'), group_chat_created=False, message_id=9, supergroup_chat_created=False, text='/start'), update_id=196617858)  
'''

'''
start - start new game
barricade - build a barricade
status - check the community status
explore - explore for new locations
travelhospital - travel to hospital
'''