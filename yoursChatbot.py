import logging
import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
import sys
import google.generativeai as palm
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Initialize bot and dispatcher
TOKEN = "6968347125:AAFdH3osAcsCH-4wFboKMbDwV-zoxgkpwY4"
dispatcher = Dispatcher()



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dispatcher.start_polling(bot)

class Reference:
    '''
    A class to store previously response from the Bard API
    '''

    def __init__(self) -> None:
        self.response = ""



load_dotenv()
palm.configure(api_key="AIzaSyCkuMp3Dp2ArsvDR-DuxlZbFmvDQFFuB7o") 

reference = Reference()



def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dispatcher.message(Command('start'))
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Your Knowledge Partner!\Created by Tanmoy Chandra. How can i assist you?")



@dispatcher.message(Command('clear'))
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message(Command('help'))
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



@dispatcher.message()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = palm.generate_text(
        prompt=message.text
        )
    reference.response = str(response.result)
    print(f">>> Answer: \n\t{reference.response}")
    await message.answer(reference.response)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())