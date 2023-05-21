import os 
from pyrogram import Client , filters
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")
bot_token = os.environ.get("BOT_TOKEN")
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
role_play_text = os.environ.get("ROLE_PLAY_TEXT")

bot = Client("my_bot",
             api_id=api_id,
             api_hash=api_hash)

config = {
    "max_tokens": 100,
    "temperature": 0.7,
    "engine": "text-davinci-003"
}

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Welcome to Role Playing bot. Follow @BugHunterBots"
    )

@bot.on_message(filters.text)
async def role_play(bot, message):
    role_play_sentence = message.text
    try:
        generated_response = await generate_response(role_play_sentence)
        await bot.send_message(
            chat_id=message.chat.id,
            text=generated_response
        )
    except openai.error.RateLimitError as e:
        # Handle token limit exception
        await bot.send_message(
            chat_id=message.chat.id,
            text="Oops! The bot has exceeded its usage limits. Please try again later."
        )

async def generate_response(input_sentence):
    prompt = f"""{role_play_text},and i need you be to role played. I need answer for {input_sentence}.If the question is not realated to 
    {role_play_text}, Reply 'Sorry, I don't know the Answer'
    """

    response = await openai.Completion.create(
        engine=config["engine"],
        prompt=prompt,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"],
        n=1,
        stop=None,
    )

    generated_text = response.choices[0].text.strip()
    return generated_text