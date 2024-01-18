'''
VERSION TO BE USED FOR TESTING ONLY
VERSION TO BE USED FOR TESTING ONLY
VERSION TO BE USED FOR TESTING ONLY
'''


import time as t
import discord
import logging
import Regex as Re
import database as db
import smtplib, ssl, aiosmtplib
import EmailContent as EC

# Handler
handler = logging.FileHandler(filename='Verification Bot.log', encoding='utf-8', mode ='w', )
client = discord.Client(intents=discord.Intents.all())

# Shows the bot has connected to the API and WebSocket.
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await client.change_presence(activity=discord.Game(name='Keeping out trolls~x'))


# Called whenever a user joins the sever. Puts them in the database and gives them a code.
# Function built already ignores duplicate insertions.
# Note: Due to the nature of Discord usernames, function does not account for 2 people having the exact same name
# as that's impossible (uses username not display name).

#@client.event
#async def on_member_join(member):
    #print(member.name)
    #if db.initial_step(member.name, Re.generate_key()):
        #await member.send("## **Hewwoo!** Welcome to the KCL Anime and Manga discord!\n"
                          #"In order to access the rest of the server, you need to verify that "
                           #"you're a student.\nPlease type your **university** email address! "
                         # )

@client.event
async def on_message(message):
    if message.author == client.user or message.guild != None:
        return
    username = message.author.name
    if db.initial_step(username, Re.generate_key()):
        await message.author.send("## **Hewwoo!** Welcome to the KCL Anime and Manga discord!\n"
                          "In order to access the rest of the server, you need to verify that "
                          "you're a student.\nPlease type your **university** email address! "
                          )
    try:
        current_step = db.get_step(username)
    except:
        return
    if Re.checkMessage('reset',message.content):
        db.clear_user(username)
        db.initial_step(username, Re.generate_key())
        await message.author.send("# Reset!\n"
                                  "## **Hewwoo!** Welcome to the KCL Anime and Manga discord!\n"
                                  "In order to access the rest of the server, you need to verify that "
                                  "you're a student.\nPlease type your **university** email address!"
                                  )
        return
    if Re.checkMessage('help',message.content):
        await message.author.send("Oki! Getting some help!")
        await client.get_user(328907829694038017).send(f"{username} needs some help!")
        return
    if current_step == 1:
        if Re.check_email(message.content):
            user_email = Re.check_email(message.content)
            pass
        else:
            await message.author.send("Ohnowo~~ That email doesn't appear to come from a London "
                                          "University. Please type a valid London university email! "
                                          "If you need to reset type 'reset' and if you need help "
                                          "type 'help'!")
            return

        email = aiosmtplib.SMTP("smtp.gmail.com", 587, start_tls=True)
        await email.connect()
        await email.login("doelaritykclanisoc@gmail.com", 'kwxj vhip vhhu xhvo')
        await email.sendmail("doelaritykclanisoc@gmail.com", str(user_email),
                                EC.create_email("doelaritykclanisoc@gmail.com", str(user_email), db.get_key(message.author.name))
                                )
        await email.quit()
        await message.author.send(f"**Oki!** You should have received an email with your code!\nIf you haven't, "
                                  f" double check your spam folder! Oh and make sure you've typed your email "
                                  f"correctly! {str(user_email)} was what I read~ x ")
        db.update_step(message.author.name,2)
        return
    elif current_step == 2:
        try:
            if str(message.content) == db.get_key(username):
                await client.get_guild(434495241098231818).get_member(message.author.id).\
                    add_roles(client.get_guild(434495241098231818).get_role(1010563130423779378))
                db.clear_user(username)
                await message.author.send("Donesies! Have fun~ xox")
            else:
                await message.author.send("oops~~ That code doesn't match your unique one. "
                                          "If you need to reset type 'reset' and if you need help "
                                          "type 'help'!")
                return
        except:
            return


client.run('MTE1NTQ1OTg2ODA5MDcxNjE3MA.Gq15KE._EdW_Nb2KJjmqy_c6Upojd74XCIXTgfDZnCRRE',
           log_handler=handler, log_level=logging.INFO
           )
