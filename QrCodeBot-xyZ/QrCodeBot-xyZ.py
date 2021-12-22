import uuid
import os
import discord 
from discord.ext import tasks, commands
from discord.ext.commands import Bot

from SecretStorage import *
from QRCodeBot import *
from datetime import datetime
import pyqrcode
import png
from PIL import Image
from pyqrcode import QRCode

from bs4 import BeautifulSoup as bs
import time
import requests
import random
import re
import asyncio
import os


page = requests.get("https://www.coingecko.com/en/coins/smooth-love-potion/php","html.paraser")
soup = bs(page.content)
now = datetime.now()
client = discord.Client()

bot_prefix = "$"

client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
   # print('\nWe are logged in as {0.user}'.format(client))
    await client.wait_for('message', check=check(context.author), timeout=30)

  #
async def status_task():
    slpvalue = soup.find(attrs={"data-coin-id" : "10366"})
    if(slpvalue):
        slptextvalue=slpvalue.text
    else:
        slptextvalue="is being fetch. Please wait "
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="SLP "+slptextvalue))
        await asyncio.sleep(60) # task runs every 60 seconds



@client.command(pass_context=True)
async def qr(ctx):
        current_time = now.strftime("%H:%M:%S")
        user = ctx.message.author
        # This for loop check for all the user's DiscordID in the Database
        if str(user.id) in ScholarsDict:
            print("This user received his QR Code : " + user.name)
            print("Discord ID : " + str(user.id))
            print("Current time : ", current_time)
            # value with discordID
            botPlaceHolders = ScholarsDict[str(user.id)]
            # discordID's privateKey from the database
            accountPrivateKey = botPlaceHolders[2]
            # discordID's EthWalletAddress from the database
            accountAddress = botPlaceHolders[1]
            # Get a message from AxieInfinty
            rawMessage = getRawMessage()
            # Sign that message with accountPrivateKey
            signedMessage = getSignMessage(rawMessage, accountPrivateKey)
            # Get an accessToken by submitting the signature to AxieInfinty
            accessToken = submitSignature(signedMessage, rawMessage, accountAddress)
            # Create a QrCode with that accessToken




            qrCode = f"QRCode_{user.id}_{str(uuid.uuid4())[0:8]}"
            qrCodePath=qrCode+".png"

            url = pyqrcode.create(qrCodePath)
            url.png(qrCodePath)
        
                        
            # taking image which user wants 
            # in the QR code center
              
            logo = Image.open("logo.jpg")
              
            # taking base width
            basewidth = 200
            # adjust image size
            wpercent = (basewidth/float(logo.size[1]))
            hsize = int((float(logo.size[1])*float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                version=5,
                box_size=10,
                border=3
            )
              
              
            # addingg the user data to QRcode
            QRcode.add_data(accessToken)
              
            # generating QR code
            QRcode.make()
              
            # taking color name from user
            QRcolor = 'black'
              
            # adding color to QR code
            QRimg = QRcode.make_image(
                fill_color=QRcolor, back_color="white").convert('RGB')
              
            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                   (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)
              
            # save the QR code generated
            QRimg.save(qrCodePath)
              
            print('QR code generated!')
            print('\n\n')



            # Send the QrCode the the user who asked for
            await ctx.message.author.send(
                "------------------------------------------------\nHello " + user.name + "\nMalakas ka ?  : ")
            await ctx.message.author.send(file=discord.File(qrCodePath))
            os.remove(qrCodePath)
            return
        else:
            print("This user didn't receive a QR Code : " + user.name)
            print("Discord ID : " + str(getattr(user,'id')))
            print("Current time : ", current_time)
            return




# @client.event
# # Listen for an incomming message
# async def on_message(message):
#     # If the author is the robot itself, then do nothing!
#     if message.author == client.user:
#         return

#     if message.content.startswith("add"):
#        # ToggleSwitch(message.content)
#         #read input file

#       #  with open("SecretStorage.py", 'rb+') as filehandle:
#      #           filehandle.seek(-1, os.SEEK_END)
#     #            filehandle.truncate()
#     #    fin = open("SecretStorage.py", "a")
#       # await test()
#     #    fin.write("\n")
#       #  await message.author.send("Enter UserID")
#       #  userID = message.content

#     #    new_string = ", '"+userID+ "': ['kirababy23#9004 | account2', '0x2af6c09c2fde55c5b2ac72936f89591bb6b6e090','b8c8400dea33901f94855aaa094cba76e248d1f8ca3e6da520743ed72f57'] }"
#     #    fin.write(new_string)
#         return

#     if message.content.find("convert")==0:
#         slpvalue = soup.find(attrs={"data-coin-id" : "10366"})
#         if(slpvalue):
#             slptextvalue=slpvalue.text
#             slpvalue=float(slptextvalue[1:])
#             slpqty = float(re.sub(r'[^0-9]', '', message.content.lower()))
#             mul=slpvalue*slpqty
#             print("You have P: ", mul )
#             await message.author.send("You have  P"+ str(mul) )
#         else:
#             await message.author.send("SLP value is currently unavailable" )

#         return

    

 


@client.event
async def on_ready():
    print("Name:", client.user.name)
    print("ID:", client.user.id)
    client.loop.create_task(status_task())





#Run the client (This runs first)
client.run(DiscordBotToken)
