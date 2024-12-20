# -*- coding: utf-8 -*-
import os

import telebot
from dotenv import load_dotenv

from assistant_ai import VOICE_INPUT_FILE, AssistantAI

import ssl
import certifi
import urllib.request

# use certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
ai_assistant = AssistantAI(language="en")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """Handle start and help commands"""
    bot.reply_to(
        message,
        "ELIZA—the next generation of Artificial General Intelligence.\n "
        "how are you doing, how can I help you?\n "
    )


@bot.message_handler(commands=["use_en"])
def change_language_to_en(message):
    """Handle changing language to English command"""
    global ai_assistant
    ai_assistant = AssistantAI(language="en")
    bot.send_message(message.chat.id, "Done")


# @bot.message_handler(commands=["use_ru"])
# def change_language_to_ru(message):
#     """Handle changing language to Russian command"""
#     global ai_assistant
#     ai_assistant = AssistantAI(language="ru")
#     bot.send_message(message.chat.id, "Done")
    

@bot.message_handler(commands=["adult"])
def change_gpt_system_setup_to_adult(message):
    """Handle changing GPT system setup to adult"""
    ai_assistant.change_gpt_system_prompt(message.from_user.id, is_adult=True)
    bot.send_message(message.chat.id, "Done")


@bot.message_handler(commands=["child"])
def change_gpt_system_setup_to_child(message):
    """Handle changing GPT system setup to child"""
    ai_assistant.change_gpt_system_prompt(message.from_user.id, is_adult=False)
    bot.send_message(message.chat.id, "Done")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    """Handle text input"""
    # Get text response from assistant
    text_response = ai_assistant.create_response_from_text(
        message.text, message.from_user.id
    )
    # Send text response to user
    bot.send_message(message.chat.id, text_response)


# @bot.message_handler(content_types=["voice"])
# def handle_voice(message):
#     """Handle voice input"""
#     # Download voice message file
#     file_info = bot.get_file(message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     # Save voice message file locally
#     with open(f"{str(message.from_user.id)}_{VOICE_INPUT_FILE}", "wb") as new_file:
#         new_file.write(downloaded_file)

#     try:
#         # Get voice response from assistant
#         voice_response = ai_assistant.create_response_from_voice(message.from_user.id)
#     except Exception as err:
#         # Send error message to user if response is too long
#         bot.send_message(message.chat.id, f"{err}")
#         return
#     # Send voice response to user
#     bot.send_voice(message.chat.id, voice_response)


bot.infinity_polling()
