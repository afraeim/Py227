import os
import webbrowser 
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN: Final = "tgBotAPI"
b_UN: Final = "@pcgotshutdown_bot"
brave = webbrowser.Chromium('C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
#Commands
async def start_command(update:Update,context: ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text('Hello Professor, this is your personal assistant here! Your system is up and running')

async def help_command(update:Update,context: ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text('''This is your personal assistant here!\nThese command words should work for you\nstdwn_now\nstdwn\nabort\nopentg\nopenyt\nshutdown [value]\nurl[value]\nwget [value]''')

async def custom_command(update:Update,context: ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text('custom command here')

#Responses

def handle_response(text:str) -> str:
    proc: str = text.lower()

    if len(proc)<=9:
        if 'hello' in proc:
            return 'hi, A7raeim'
        elif proc == 'stdwn':
            return os.system('shutdown /s /t 1200'), 'System will be shutdown in 20 minutes'
        elif proc=='abort':
            return os.system('shutdown -a')
        elif proc=='opentg':
            brave.open('https://web.telegram.org/k/')
            return 'Telegram Opened'
        elif proc=='openyt':
            brave.open('https://www.youtube.com/')
            return 'Youtube Opened'
        else:
            return "Not Understood"
    elif len(proc)>9:
        z=proc.split()
        if z[0]=='shutdown' and z[1].isdecimal()==True:
            return os.system(f'shutdown /s /t {z[1]}'), f'System will be shutdown in {z[1]} minutes'
        elif z[0] == 'url':
            brave.open(str(z[1]))
            return 'Site opened'
        elif z[0] =='wget':
            os.system(f'wget {z[1]}')
            return 'Your file download started'
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'group':
        if b_UN in text:
            new_text: str = text.replace(b_UN, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)

async def error(updae: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {updae} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
    