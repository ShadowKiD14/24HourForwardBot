import logging
import time
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#edit token and channel
TOKEN = 'YOUR_BOT_TOKEN_HERE'
FORWARD_TO_CHANNEL = '@CHANNEL_USERNAME_with@'
SLEEP_TIME = 1500 # Sleep for 25 minutes (1500 seconds)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am alive and ready to forward your messages.')

def forward(update: Update, context: CallbackContext) -> None:
    global is_forwarding
    is_forwarding = True
    update.message.reply_text('Please send all the messages that have to be forwarded.')

messages_to_forward = []

def send_to_channel(update: Update, context: CallbackContext) -> None:
    global is_forwarding
    if is_forwarding:
        forwarded_messages = messages_to_forward
        for i in range(0, len(forwarded_messages), 5):   #it will send 5 messages in a batch
            forwarded_batch = forwarded_messages[i:i+5]  #sends 5 messages in next batch
            for message in forwarded_batch:
                context.bot.forward_message(chat_id=FORWARD_TO_CHANNEL, from_chat_id=message.chat_id, message_id=message.message_id)
            time.sleep(SLEEP_TIME)
        update.message.reply_text('All the messages have been forwarded.')
        is_forwarding = False
        messages_to_forward.clear() # Clear the list after all messages are forwarded
    else:
        update.message.reply_text('No messages to forward.')

def message_received(update: Update, context: CallbackContext) -> None:
    global is_forwarding
    if is_forwarding:
        messages_to_forward.append(update.message)
        update.message.reply_text('Message received and will be forwarded.')
    else:
        update.message.reply_text('Please start forwarding messages using /forward.')

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('forward', forward))
    dispatcher.add_handler(CommandHandler('send', send_to_channel))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_received))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
