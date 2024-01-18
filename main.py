import discord
import logging
import Regex as Re
import database as db
import aiosmtplib
import EmailContent as EC
import messages as mes

# Handler
handler = logging.FileHandler(filename='Verification Bot.log', encoding='utf-8', mode ='w', )
client = discord.Client(intents=discord.Intents.all())

greeting = ("## Welcome!\n"
            f"{client.get_emoji(975421021156958248)}In order to access the rest of the server, you need to verify that "
            f"you're a student.\n{client.get_emoji(975421021156958248)}If you need help, just type 'help'!\n"
            f"{client.get_emoji(975421021156958248)}Please type your **university** email address!")

# Shows the bot has connected to the API and WebSocket.
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await client.change_presence(activity=discord.Game(name='Email Verification'))


# Called whenever a user joins the sever. Puts them in the database and gives them a code.
# Function built already ignores duplicate insertions.
# Note: Due to the nature of Discord usernames, function does not account for 2 people having the exact same name
# as that's impossible (uses username not display name).q


@client.event
async def on_member_join(member):
    print(member.name)
    if db.initial_step(member.name, Re.generate_key()):
        await member.send(greeting)


@client.event
async def on_message(message):
    username = message.author.name
    if message.guild == None:
        print(f'{username}: "{message.content}"   Attachments: {message.attachments}')
    if message.author == client.user or message.guild != None:   # Makes sure it's a DM and the bot doesn't reply to itself
        return
    if message.author == client.get_user(328907829694038017):
        if db.initial_step(message.content, Re.generate_key()):
            await message.author.send(greeting)
        else:
            await client.get_user(328907829694038017).send(
                f"That person's already in the database."
            )
        return
    if Re.checkMessage('start', message.content.lower()):
        if db.initial_step(username, Re.generate_key()):
            await message.author.send(greeting
                                      )
        return
    try:
        current_step = db.get_step(username)  # Checks if they're in the database.
    except:
        return
    if Re.checkMessage('reset',message.content.lower()):  # Resets the bot if any user errors occur.
        db.clear_user(username)
        db.initial_step(username, Re.generate_key())
        await message.author.send(f"# Reset!\n{greeting}"
                                  )
        return
    if Re.checkMessage('help',message.content.lower()): # DMs me to help them out : ).
        await message.author.send("Oki! Getting some help!")
        await client.get_user(328907829694038017).send(f"{username} needs some help!")
        return
    if current_step == 1:
        if Re.check_email(message.content): # Function to verify email is from a London university.
            user_email = Re.check_email(message.content)  # >> Additional Note (1) <<
            pass
        else:
            await message.author.send("Ohnowo~~ That email doesn't appear to come from a "
                                          "University. Please type a valid university email! "
                                          "If you need to reset type 'reset' and if you need help "
                                          "type 'help'!")  # Error message for user if they type an invalid address.
            return
        try:
            email = aiosmtplib.SMTP("smtp.gmail.com", 587, start_tls=True)
            await email.connect()
            await email.login("******************@gmail.com", mes.app_password)
            await email.sendmail("******************@gmail.com", str(user_email),
                                EC.create_email("******************@gmail.com", str(user_email), db.get_key(message.author.name))
                                )
            await email.quit()
            await message.author.send(f"You should have received an email with your code!\nIf you haven't, "
                                  f"double check your spam folder!\nOh and make sure you've typed your email "
                                  f"correctly!\n**{str(user_email)}** was what I read.")
            db.update_step(message.author.name,2)
            return
        except:
            await client.get_user(328907829694038017).send(f"{username} requires assistance.")                                                                                   # Error message for user if they type an invalid address.
            return
    elif current_step == 2: # Email has been sent now we look for the code.
        try:
            if Re.checkMessage(db.get_key(username), message.content):
                await client.get_guild(434495241098231818).get_member(message.author.id).\
                    add_roles(client.get_guild(434495241098231818).get_role(1010563130423779378))  # Adds verified role
                db.clear_user(username)
                await message.author.send("All done! Have fun")
            else:
                await message.author.send("That code doesn't match your unique one. "
                                          "If you need to reset type 'reset' and if you need help "
                                          "type 'help'!")  # Error to user for wrong code.
                return
        except:
            return

# DEBUGGING

@client.event
async def on_error(event):
    print(f'{event} raised.')
# DEBUGGING

client.run(mes.bot_token,
           log_handler=handler, log_level=logging.INFO
           )


# Additional Note (1): There is no way of 100% verifying the user has typed their exact email address as that
# is information I do not have access to. The best I can do is making sure it follows the pattern: name@uni.ac.uk
# using regex. Even if I used GMail's API to verify the email exists, there will always be human error :),
# hence the reset command.
