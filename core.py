# coding=utf-8
#!/usr/bin/python

import telebot
import requests
from telebot import types
import time
from time import gmtime, strftime
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

token = 'aaa'
bot = telebot.TeleBot(token)

commands = {  # Descripción usada en el comando "/help"
              'start': 'Iniciar el bot',
              'help': 'Te proporciona información sobre los comandos disponibles',
              'showdown': 'Envia información de un jugador de pokemon showdown',
              'dreambeach': 'Cuenta atras para el Dreambeach 2018 (MAD - Bus 8)',
			  'cartel': 'Envia cartel del dreambeach',
}

# only used for console output now
def listener(messages):
    """
	Cuando un nuevo mensaje llegue, Telebot llamará a esta función
    """
    for m in messages:
        if m.content_type == 'text':
            # Imprime en el terminal el mensaje enviado
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot.set_update_listener(listener)  # registrar listener


# controla el comando "/start"
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Iniciando bot...")
    bot.send_chat_action(cid, 'typing')  # muestra el estado del bot a 'escribiendo...' (max: 5 seg)
    time.sleep(2)
    bot.send_message(cid, "¡Bot iniciado!")
    command_help(m)  # muestra el mensaje de ayuda

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Comandos disponibles: \n\n"
    for key in commands:  # Generar texto de ayuda con los comandos descritos arriba
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # enviar mensaje generado

@bot.message_handler(commands=['dreambeach'])
def command_showdown(m):
    cid = m.chat.id
    #a = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    a = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    a = a.strftime("%Y-%m-%d %H:%M:%S")
    b = '2018-08-08 12:00:00'

    f_actual = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
    f_dreambeach = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
    print a
    dif = relativedelta(f_dreambeach, f_actual)
    bot.send_message(cid, "Quedan *%d dias %d horas %d minutos y %d segundos* para el Dreambeach 2018" % (dif.days,dif.hours,dif.minutes,dif.seconds),parse_mode="Markdown")

@bot.message_handler(commands=['cartel'])
def command_showdown(m):
    cid = m.chat.id
    cartel = open('cartel.jpeg','rb')
    bot.send_photo(cid, cartel)

	
@bot.message_handler(commands=['showdown'])
def command_showdown(m):
    cid = m.chat.id
    bot.send_message(cid, "*Utilización:*\n\n_!showdown username_\n\nMuestra ELO de un jugador de Pokémon Showdown",parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text.startswith("!showdown"))
def command_text_showdown(m):
	usuario = ""
	try:
		usuario = str(m.text.split(" ")[1])
		print ">>>>>>>>>> "+usuario
        	page = requests.get("https://pokemonshowdown.com/users/"+usuario)
        	infojugador = ""
        	infojugador = "Información del jugador *"+usuario+"*:\n\n"
		#bot.send_message(m.chat.id, "",parse_mode="Markdown")
		soup = BeautifulSoup(page.content, 'html.parser')
		print("soup: "+soup.prettify())
		tabla = soup.findChildren('table')[0] # Coge la primera tabla
		filas = tabla.findChildren(['tr'])
		for fila in filas:
            		celdas = fila.findChildren('td')
            	for celda in celdas:
                	valor = celda.string
                	print "Valor de esta celda: %s" % valor
	        	if valor is 'none':
                    		print "error"
	        	elif valor:
                    		infojugador +=" "+valor
                    	#bot.send_message(m.chat.id,valor)
			if valor is '(more games needed)':
                	    bot.send_message(m.chat.id,"Se necesitan mas partidas a este modo para obtener esta información papapa")
        		#valor+="\n"
		bot.send_message(m.chat.id,str(infojugador),parse_mode="Markdown")
	except Exception as e:
		print(str(e))
		if "list index out" in str(e):
			errorm="El jugador "+usuario+ " no existe"
		elif str(e):
			errorm = "Error al ejecutar el comando con el jugador "+usuario+" \n"+str(e)
        	bot.send_message(m.chat.id,errorm)
bot.polling()
