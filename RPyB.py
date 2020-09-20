import discord
from discord.ext import commands
import time
import gtts
from datetime import datetime
import owotrans
import random
import asyncio
import requests
import os
import numpy as np
from zalgo_text import zalgo
from foaas import fuck
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

bot = commands.Bot(command_prefix = 'uc ', help_command=None)
TOKEN = os.environ.get('TOKEN')
ownerid = '435750383491481602'

CHROMEDRIVER_PATH = '/app/.wdm/drivers/chromedriver/linux64/85.0.4183.87'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1024x1400")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd(),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

driver.get("https://benisland.neocities.org/petpet/")
assert "petpet".lower() in driver.title.lower()

async def patpat(filename, picture):
    input_file = driver.find_element_by_xpath("//input[@type='file' and @id='uploadFile']")
    input_file.send_keys(os.getcwd() + picture)

    await asyncio.sleep(5)

    exportgif = driver.find_element_by_id("export")
    exportgif.click()

    await asyncio.sleep(5)

    output = driver.find_element_by_id('result')
    output = output.get_attribute('outerHTML').split('"')
    output = output[1]

    print(output)
    driver.execute_script(open("download.js").read(), output, filename)
    await asyncio.sleep(5)
    
    driver.close()

def get_all_variations(word):
    if len(word) == 1:
        #a single character has two variations. e.g. a -> [a, A]
        return [word, word.upper()]
    else:
        #otherwise, call recursively using the left and the right half, and merge results.
        word_mid_point = len(word) // 2
        left_vars = get_all_variations(word[:word_mid_point])
        right_vars = get_all_variations(word[word_mid_point:])
        variations = []
        for left_var in left_vars:
            for right_var in right_vars:
                variations.append(left_var + right_var)
        return variations


def donothing():
    return 

def selection_sort(x):
    for i in range(len(x)):
        swap = i + np.argmin(x[i:])
        (x[i], x[swap]) = (x[swap], x[i])
    return x


@bot.event
async def on_ready():
    with open('launchlogs.txt', 'a') as ll:
        now = datetime.now()
        ll.write(now.strftime("%d/%m/%Y %H:%M:%S") + '\n')
    print('Launched.')

@bot.command()
async def help(ctx):
    await ctx.send(f'{ctx.author.mention}: https://randpybot.neocities.org/help/')
    
@bot.command()
async def say(ctx, *, string):
    await ctx.send(string)

@bot.command()
async def tts(ctx, *, string):
    message = await ctx.send('Generating, please wait...')
    if len(string) > 500:
        await message.edit('An error occurred! Your string is longer than **500** characters. Maybe try using the commands by chunks?')
        return 
    tts = gtts.gTTS(string)
    ttsfilename = f'generatedtts{ctx.message.id}.mp3'
    tts.save(ttsfilename)
    await message.delete()
    await ctx.send(file = discord.File(ttsfilename))
    
@bot.command()
async def pingme(ctx):
    await ctx.send(ctx.author.mention)

@bot.command()
async def dmme(ctx):
    await ctx.author.send('⠀')
    
@bot.command()
async def owoify(ctx, *, string: str):
        await ctx.send(owotrans.owo(string))
        
@bot.command()
async def getpastebin(ctx, link):
    if link.startswith('http://pastebin.com/'):
        link = link.split('/')
        rawlink = link[0] + '//' + link[2] + '/raw/' + link[3]
    elif link.startswith('pastebin.com'):
        link = link.split('/')
        rawlink = 'http://' + link[0] + '/raw/' + link[1]
    else:
        sneakysneaky = await ctx.send("You thought you can get data from other websites? Nah fam, it doesn't work that way.")
        await asyncio.sleep(10)
        await sneakysneaky.delete()
        await ctx.message.delete()
    try:
        data = requests.get(rawlink).text
    except Exception as inst:
        errormsg = await ctx.send(f'Oops! An error occured. Error: `{inst}`')
        await asyncio.sleep(30)
        await errormsg.delete()
        return 
    await ctx.send(f'```{data}```')
    
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.default)
async def sayinconsole(ctx, *, message):
    with open('messages.txt', 'a') as file:
        file.write(f'{ctx.author.name}#{ctx.author.discriminator} says: {message}\n')
        file.close()

@bot.command()
async def findemote(ctx, *, searchstr):
    for fname in os.listdir('./emojis/'):
        if searchstr in fname:
            await ctx.send(file=discord.File('emojis/' + fname))
            return 
    await ctx.send('No emotes with that name found in the list. You can recommend one tho!')
    
@bot.command()
async def MEOOOW(ctx):
    await ctx.send(file=discord.File('theclickmeow.mp4'))
    
@bot.command()
async def react(ctx, emoji: discord.Emoji):
    users_id = ctx.author.id
    oldestMessage = None
    await ctx.message.delete()
    for channel in ctx.guild.text_channels:
        fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
        if fetchMessage is None:
            continue


        if oldestMessage is None:
            oldestMessage = fetchMessage
        else:
            if fetchMessage.created_at > oldestMessage.created_at:
                oldestMessage = fetchMessage

    await oldestMessage.add_reaction(emoji)
    
@bot.command()
async def zalgoify(ctx, *, text):
    await ctx.send(zalgo.zalgo().zalgofy(text))
    
@bot.command()
async def foaas(ctx):
    await ctx.send(fuck.random(name=ctx.author.name, from_=bot.get_user(ownerid)).text)
    
@bot.command()
async def brainf(ctx, *, code: str):
    bfc = brainfuck.to_function(f"""{code}""")
    await ctx.send(bfc())
    
@bot.command()
async def tobrainf(ctx, *, string: str):
    await ctx.send(print("".join("+"*ord(i)+".[-]"for i in string)))
    
@bot.command()
async def fish(ctx, value, *, code: str):
    ffn = f'fish{ctx.message.id}.fish'
    with open(ffn, 'a') as file:
        file.write(code)
        file.close()
    os.system(f'fish.py {ffn} -v {value}')
    
@bot.command()
async def tofish(ctx, *, string: str):
    code = f"""
    !v"{string}"r!
    o>l?!;
    """
    await ctx.send(code)

@bot.command()
async def getallvariations(ctx, *, string):
    await ctx.send(get_all_variations(string))
    
@bot.command()
async def patpat(ctx, advanced = 0):
    if advanced == 1:
        #code with position changing
        await ctx.send('Work in progress...')
    elif advanced == 0:
        pic = requests.get(ctx.message.attachments[0].url, allow_redirects=True)
        open(f"pic{ctx.message.id}.png", "wb").write(pic.content)
        input_file = driver.find_element_by_xpath("//input[@type='file' and @id='uploadFile']")
        input_file.send_keys(os.getcwd() + f"\\pic{ctx.message.id}.png")

        await asyncio.sleep(5)

        exportgif = driver.find_element_by_id("export")
        exportgif.click()

        await asyncio.sleep(5)

        output = driver.find_element_by_id('result')
        output = output.get_attribute('outerHTML').split('"')
        output = output[1]

        print(output)
        driver.execute_script(open("download.js").read(), output, f"gif{ctx.message.id}.gif")
        await asyncio.sleep(5)
        await ctx.send(driver.find_element_by_id('info').get_attribute('innerHTML'), file=discord.File(f"gif{ctx.message.id}.gif"))
bot.run(TOKEN)
