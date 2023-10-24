from config import *
import telebot
import openai
import requests  # import the requests library

chatStr = ''

def ChatModal(prompt):
    global chatStr
    openai.api_key = OPENAI_KEY
    chatStr += f"Infinity_PH1X: {prompt}\nInfinity_PH1X: "
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    chatStr += f"{response['choices'][0]['text']}"
    return response['choices'][0]['text']

bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, Welcome to Infinity_PH1X")

@bot.message_handler(commands=['search'])  # add a handler for the search command
def search(message):
    query = message.text[8:]  # get the search query from the message
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    response = requests.get(f"https://api.bing.microsoft.com/v7.0/search?q={query}", headers=headers)  # send a GET request to the Bing Search API
    results = response.json()  # parse the JSON response from the API
    bot.reply_to(message, "\n".join(results))  # send the search results back to the user

@bot.message_handler(content_types=['text'])
def chat(message):
    try:
        reply = ChatModal(message.text)
        bot.reply_to(message,reply)
    except Exception as e:
        print(e)
        bot.reply_to(message,e)

print("Bot Started...")
bot.polling()
n