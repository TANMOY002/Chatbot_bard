import logging
import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
import sys
import google.generativeai as palm
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.utils.chat_action import ChatActionSender
import telegram


# Initialize bot and dispatcher
TOKEN = "6968347125:AAFdH3osAcsCH-4wFboKMbDwV-zoxgkpwY4"
dispatcher = Dispatcher()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
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
palm.configure(api_key="AIzaSyDMdCuMazDiRgnw3xVas_R-z_1wMcwQYNQ") 

reference = Reference()


@dispatcher.message(Command('start'))
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    welcome_command = """
    I'm Your Knowledge Partner Chatbot created by Tanmoy Chandra! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context
    """
    await message.reply(f"Hello, {hbold(message.from_user.full_name)}! "+welcome_command)

class ChatState:
    def __init__(self):
        self.messages = []
    def clear(self):
        self.messages = []


# Assuming `reference` is defined before the function
reference = ChatState()

@dispatcher.message(Command('clear'))
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    reference.clear()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message()
async def chatgpt(message: types.Message):
    global reference

    print(f">>> USER: \n\t{message.text}")

    # Add the user's message to the messages list
    reference.messages.append(message.text)
    # Use all the messages in the conversation so far
    response = palm.chat(messages=reference.messages).reply(message.text)
    
    # Update the reference.response
    reference.response = str(response.last)
    print(f">>> Answer: \n\t{reference.response}")
    await message.answer(reference.response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())