from asyncio.tasks import sleep
from collections import deque

import discord
from discord.ext.commands.core import command
from dreamWorker import DreamJob, DreamParams, DreamWorker
import os
import logging
import asyncio
import functools
import glob
import typing
import shutil
from datetime import datetime
from discord import User, user
from discord.ext import commands
#from dotenv import load_dotenv

CMD_PREFIX = os.getenv('COMMAND_PREFIX')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


IMAGE_WIDTH = int(os.getenv('IMAGE_WIDTH'))
NUM_LAYERS = int(os.getenv('NUM_LAYERS'))
BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
GRADIENT_ACCUMULATE_EVERY = int(os.getenv('GRADIENT_ACCUMULATE_EVERY'))
EPOCHS = int(os.getenv('EPOCHS'))
ITERATIONS = int(os.getenv('ITERATIONS'))
SAVE_GIF = bool(os.getenv('SAVE_GIF'))
SAVE_EVERY = int(os.getenv('SAVE_EVERY'))

dreamParams = DreamParams(IMAGE_WIDTH, NUM_LAYERS, BATCH_SIZE,
                          GRADIENT_ACCUMULATE_EVERY, EPOCHS, ITERATIONS, SAVE_GIF, SAVE_EVERY)


userQueue = deque()
jobQueue = deque()
userJobs = {}


logging.basicConfig(
    handlers=[logging.FileHandler('dreamBot.log', 'a', 'utf-8')],
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger()


bot = commands.Bot(command_prefix=CMD_PREFIX)

@bot.command(name='dream', help='Adds a dream to the queue.', pass_context=True)
async def addDreamToQueue(ctx:commands.Context, dreamText:str):
    if ctx.author.id in userQueue:
        await(ctx.send("You are already in the queue, please wait."))
        return
    if not dreamText:
        await(ctx.send("No dream text was provided. Nothing was submitted"))
        return
    userQueue.append(ctx.author.id)
    print(userQueue)
    newDreamJob = DreamJob(ctx, dreamText)
    jobQueue.append(newDreamJob)
    userJobs[ctx.author.id] = newDreamJob
    await(ctx.send('Added dream "{}" to queue.'.format(dreamText)))
    return

@bot.command(name='remove', help='Removes the users current dream.', pass_context=True)
async def removeDreamFromQueue(ctx:commands.Context):
    if ctx.author.id not in userQueue:
        await(ctx.send("You are not currently in the queue, removing nothing."))
        return
    userQueue.remove(ctx.author.id)
    print(userQueue)
    oldDreamText = userJobs[ctx.author.id].dreamText
    jobQueue.remove(userJobs[ctx.author.id])
    userJobs[ctx.author.id] = None
    await(ctx.send('Removed dream "{}" from queue.'.format(oldDreamText)))

@bot.command(name='change', help='Changes the users current dream.', pass_context=True)
async def changeDreamFromQueue(ctx:commands.Context, dreamText:str):
    if ctx.author.id not in userQueue:
        await(ctx.send("You are not currently in the queue, changing nothing."))
        return
    if not dreamText:
        await(ctx.send("No dream text was provided. Nothing was submitted"))
        return
    queuePosition = userQueue.index(ctx.author.id)
    oldDreamText = jobQueue[queuePosition].dreamText

    newDreamJob = DreamJob(ctx, dreamText)
    jobQueue[queuePosition] = newDreamJob
    userJobs[ctx.author.id] = newDreamJob
    await(ctx.send('Changed dream in queue from "{}" to "{}".'.format(oldDreamText, dreamText)))

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has connected to Discord!')
    bot.loop.create_task(checkQueue())


async def checkQueue():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if not userQueue:
            logger.info("No requests in queue, sleeping for now")
            await asyncio.sleep(5)
            continue
        await processQueueEntry()


async def processQueueEntry():
    currentJob: DreamJob
    currentJob = jobQueue.popleft()
    currentUser: str
    currentUser = userQueue.popleft()
    userJobs[currentUser] = None
    dreamImage = await createDreamTask(runDream, currentJob)
    await sendImage(dreamImagePath=dreamImage, dreamText=currentJob.dreamText, discordContext=currentJob.discordContext)
    await cleanUpDir(dreamImage=dreamImage, currentUser=currentUser)


async def cleanUpDir(dreamImage: str, currentUser: str):
    if not os.path.exists(f'images/{currentUser}/'):
        os.makedirs(f'images/{currentUser}/')
    now = datetime.now()
    currentDate = now.strftime("%d-%m-%Y_%H-%M-%S")
    destPath = f'images/{currentUser}/{dreamImage}-{currentDate}'
    os.mkdir(destPath)
    # shutil.copy2(f'{dreamImage}.jpg',f'{destPath}/{dreamImage}.jpg')
    for image in glob.glob(f'{dreamImage}*.jpg'):
        shutil.move(image, f'{destPath}/{image}')
    if os.path.exists(f'{dreamImage}.gif'):
        shutil.move(f'{dreamImage}.gif', f'{destPath}/{dreamImage}.gif')
    return

# Solution for running a blocking function in a non-blocking way
# taken from: https://stackoverflow.com/a/65882269


async def createDreamTask(runDream: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(runDream, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)


def runDream(dreamJob: DreamJob):
    dreamText = dreamJob.dreamText
    dreamWorker = DreamWorker(dreamText=dreamText,dreamParams=dreamParams)
    dreamImage = dreamWorker.runDream()
    print(dreamImage)
    return dreamImage


async def sendImage(dreamImagePath: str, dreamText: str, discordContext: commands.Context):
    dreamImage = discord.File(fp=f'{dreamImagePath}.jpg')
    await discordContext.reply(f'"{dreamText}":', file=dreamImage, mention_author=True)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    pass
