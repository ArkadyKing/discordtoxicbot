import discord
import asyncio
import random
from discord.ext import tasks, commands
from datetime import datetime, timedelta

TOKEN = 'здесь был токен'
bot = commands.Bot(command_prefix='/')

def is_bot(msg):
    return msg.author == bot.user

#каждые 24 часа обновляется счетчик дней в статусе бота
@tasks.loop(hours=24)
async def my_loop():
        with open('days.txt', 'r') as dayf:
            read = dayf.readlines()[-1]
            
        last = datetime.strptime(str(read[0:16]), "%d.%m.%Y %H:%M")
        current = datetime.today().strftime("%d.%m.%Y %H:%M")
        tot = datetime.strptime(current, "%d.%m.%Y %H:%M") - last
        emoch = ''
        for ch in str(tot.days):
            emoch += f"{ch}️⃣"          
        if tot.days % 10 == 1 and tot.days % 100 != 11:
            dnyaei = "день"
        elif 2 <= tot.days % 10 <= 4 and (n % 100 < 10 or tot.days % 100 >= 20):
            dnyaei = "дня"
        else:
            dnyaei = "дней"
        
        await bot.change_presence(activity=discord.Streaming(name=f"{emoch} {dnyaei}",url="https://www.twitch.tv/silvername"))
        print(f'{current} date refreshed\n------')

#при старте бот говорит, с каким id и именем он зашел
@bot.event
async def on_ready():
    print(f'Logged in as "{bot.user.name}"\nid: {bot.user.id}\n------')
    my_loop.start()

#при заходе в определенный канал, бот заходит туда же и проигрывает композицию welcome.mp3
@bot.event    
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    
    if not before.channel and after.channel and (after.channel.id==758215230470750242 or after.channel.id==601325824855244810):
        current = datetime.today().strftime("%d.%m.%Y %H:%M")
        print(f'{current} {member.name} joined {after.channel.name}\n------')
        voice = await after.channel.connect()
        await asyncio.sleep(1)
        voice.play(discord.FFmpegPCMAudio('welcome.mp3'))
        await asyncio.sleep(3)
        await voice.disconnect()

#бот отвечает на сообщения/ добавляет рекции к ним
@bot.event    
async def on_message(msg):
    if ("69" in msg.content):
            await msg.add_reaction('🇳')
            await msg.add_reaction('🇮')  
            await msg.add_reaction('🇨')
            await msg.add_reaction('🇪')

    if msg.author == bot.user:  #чтобы не было замыкания в себя  
        return
    else:
        if ("токсик" in msg.content or "toxic" in msg.content):  #то, ради чего создавался бот. Если написать это, то счетчик обнулится, текущая дата запишется в файл и если поставлен рекорд, запишется рекорд     
            rrrr = 0
            with open('days.txt', 'r') as dayf:
                read_date = dayf.readlines()[-1]

            last_date = datetime.strptime(str(read_date[0:16]), "%d.%m.%Y %H:%M")
            current_date = datetime.today().strftime("%d.%m.%Y %H:%M")
            total = datetime.strptime(current_date, "%d.%m.%Y %H:%M") - last_date
            stotal = str(total)[:-3]
            with open('days.txt', 'a') as dayf:
                dayf.write('\n' + current_date)
                      
            await msg.channel.send(f'{stotal} без токсичности')

            with open('record.txt', 'r') as recordf:
                rr = recordf.readline()
            
            await msg.channel.send(f'{rr} - предыдущий рекорд')

            if rr[0:5]=='1 day':
                rrr = datetime.strptime(rr, "%d day, %H:%M")
            elif rr[2]!='d' and rr[3]!='d':
                    rrr = datetime.strptime(rr, "%H:%M")
                    rrrr=1
            else:
                rrr = datetime.strptime(rr, "%d days, %H:%M")
                               
            if rrrr == 1:
                if total > timedelta(hours=rrr.hour, minutes=rrr.minute):
                    with open('record.txt', 'w') as recordf:
                        recordf.write(stotal)
                        await msg.channel.send('Новый рекорд!')
            elif total > timedelta(days = rrr.day, hours=rrr.hour, minutes=rrr.minute):
                    with open('record.txt', 'w') as recordf:
                        recordf.write(stotal)
                        await msg.channel.send('Новый рекорд!')
            my_loop.restart()
                

        if ("nice" in msg.content or "найс" in msg.content): #реакции к сообщению
            await msg.add_reaction('6️⃣')
            await msg.add_reaction('9️⃣')  


        if ("kek" in msg.content or "кек" in msg.content or "<:KEKW:719911656146075688>" in msg.content): #реакции к сообщению
            await msg.add_reaction("<:KEKW:719911656146075688>")

    await bot.process_commands(msg)
    
    
@bot.command() #команда проверки работы команд
async def test(ctx, arg):
    await ctx.channel.send(arg)

@bot.command() #команда с настраивамым рандомом
async def roll(ctx, *arg):
    if not arg:
            response = str(random.randint(1, 100))
    elif len(arg) == 1:
        try:
            rollx = int(arg[0])
            response = str(random.randint(1, rollx))
        except ValueError:
            response = f"{ctx.author.display_name}, неправильный ввод"
    elif len(arg) == 2:
        try:
            rollx = int(arg[0])
            rolly = int(arg[1])
            response = str(random.randint(rollx, rolly))
        except ValueError:
            response = f"{ctx.author.display_name}, неправильный ввод"
    else: 
        response = f"{ctx.author.display_name}, неправильный ввод"
   
    await ctx.channel.send(response)

@bot.command() #команда монетки
async def flip(ctx):
    response = random.choices(["орёл", "решка", "ребро"], weights=[40, 40, 1])
    await ctx.channel.send(*response)
  

@bot.command() #команда удаления сообщений
async def clear(ctx):
    try:
        deleted = await ctx.channel.purge(limit=10, check=is_bot)
        await ctx.channel.send(f'Deleted {len(deleted)} message(s)')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=is_bot)
    except:
        await ctx.channel.send('Нет прав!')
       
bot.run(TOKEN) #запуск бота
