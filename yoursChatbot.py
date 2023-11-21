import logging
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import sys
import google.generativeai as palm


class Reference:
    '''
    A class to store previously response from the Bard API
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
palm.configure(api_key=os.getenv("BARD_TOKEN")) 

reference = Reference()

TOKEN = os.getenv("TOKEN")

#configure logging
logging.basicConfig(Level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Tele Bot!\Created by Bappy. How can i assist you?")



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm your  Knowledge Partner created by Tanmoy Chandra! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)



@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = palm.generate_text(
          prompt=message.text
        )
    reference.response = response.result
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)