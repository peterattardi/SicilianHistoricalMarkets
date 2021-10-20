import telebot #pyTelegramBotAPI
import csv
import requests


# Bot Name = @OpenData2021Bot
# weather key = 1fd811a4037fe76cc9cca0d5d0f240c9
API = '1841076560:AAF2cVQ8SjXK6-Vo6iQMlflAOno4V0pfCVM'
FILE = "mercatiStoriciSiciliani.csv"
bot = telebot.TeleBot(API)



@bot.message_handler(commands=["town"])
def handle_all_message(message):
    text = ""
    body = message.text[6:]
    with open(FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(row["Comune"] == body.title()):
                if (row["Denominazione"] == "Mercato"):
                    text += "Mercato di " + body.title()
                else:
                    text += (row["Denominazione"]+"\n")
    if text == "":
        bot.reply_to(message, "No markets in "+body.title()+ " found")
    else:
        bot.reply_to(message, text)


@bot.message_handler(commands=["province"])
def handle_all_message(message):
    text = ""
    body = message.text[10:]
    with open(FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(row["Provincia"] == body.title()):
                if (row["Denominazione"] == "Mercato"):
                    text += "Mercato di " + row["Comune"] + "   (" + row["Comune"] + ")" +"\n"
                else:
                    text += (row["Denominazione"] + "   (" + row["Comune"] + ")" +"\n")
    if text == "":
        bot.reply_to(message, "No markets in "+body.title()+ " found")
    else:
        bot.reply_to(message, text)


@bot.message_handler(commands=["market"])
def handle_all_message(message):
    text = ""
    body = message.text[8:]
    with open(FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(body.title() in row["Denominazione"] or body in row["Denominazione"] ):
                text += row["Descrizione"] + "\n\n\n"
                text += "Il mercato è ubicato in:\n " + row["Localizzazione"] + "\n\n\n"
                google = "https://www.google.it/maps/place/" + row["Latitudine"] + ","+ row["Longitudine"]
                text += "Raggiungi il mercato: \n"
                text += google + "\n\n\n"

                api_call = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(row["Latitudine"],row["Longitudine"],"1fd811a4037fe76cc9cca0d5d0f240c9")
                api_request = requests.get(api_call).json()
                temperature = round(api_request["main"]["temp"] - 273.15)
                feels_like = round(api_request["main"]["feels_like"] - 273.15)
                temp_min = round(api_request["main"]["temp_min"] - 273.15)
                temp_max = round(api_request["main"]["temp_max"] - 273.15)
                humidity = round(api_request["main"]["humidity"])
                descr = api_request["weather"][0]["description"].title()
                emojii = ""
                if temperature >= 30:
                    emojii = "🔴"
                elif temperature >= 25:
                    emojii = "🔶"
                else:
                    emojii = "✅"

                text += emojii + " La temperatura a " + row["Comune"] + " oggi è di " + str(temperature) + "°C." + emojii + "\n"
                text += "🤔 La temperatura percepita è di " + str(feels_like) + "°C.\n"
                text += "🔽 La minima sarà di " + str(temp_min) + "°C.\n" +\
                        "🔝 La massima raggiungerà i " + str(temp_max)+ "°C.\n"
                text += "💧 Umidità: " + str(humidity) +"%.\n\n"
                text += "Condizione meteo generale: " + descr + "\n\n\n"




    if text == "":
        bot.reply_to(message, "No markets in "+body.title()+ " found")
    else:
        bot.reply_to(message, text)




bot.polling()


#8igjbYRpyOsat65h4qVUiM8CzABPogT0

#api.openweathermap.org/data/2.5/weather?q=palermo&appid=1fd811a4037fe76cc9cca0d5d0f240c9
