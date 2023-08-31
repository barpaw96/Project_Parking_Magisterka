import re
import connection as connection
import mysql.connector
from mysql.connector import Error
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
connection = mysql.connector.connect(user='root',
                                     password='admin',
                                     host='127.0.0.1',
                                     database='magisterka',
                                     auth_plugin='mysql_native_password')


vw_cascade = cv2.CascadeClassifier('cascade_VW1.xml')
toyota_cascade = cv2.CascadeClassifier('cascade_Toyota.xml')
audi_cascade = cv2.CascadeClassifier('cascade_Audi.xml')
renault_casade = cv2.CascadeClassifier('cascade_Renault.xml')
hyundai_casade = cv2.CascadeClassifier('cascade_Hyundai.xml')
tablica_casade = cv2.CascadeClassifier('cascade_Tablice.xml')

cap = cv2.VideoCapture(0)

while True:

    ret, img = cap.read()
    color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tablice_rej_activ = tablica_casade.detectMultiScale(color)

    for (x,y,w,h) in tablice_rej_activ:
        foto2 = color[y:y + +h, x:x + w + 60, :]
        time.sleep(0.5)
        thresh = cv2.threshold(foto2, 110, 255, cv2.THRESH_BINARY)[1]
        from pytesseract import image_to_string
        odczyt_tablicy_activ = image_to_string(thresh, lang='eng', config='--psm 9')
        tablica_edyt_active = odczyt_tablicy_activ.rstrip()
        tablica_edyt_active = re.sub("[^A-Z0-9]", "", tablica_edyt_active)
        sql_tablice_active = "SELECT id, name, idcolor_car, number_plates FROM users WHERE number_plates = %s"

        cursor = connection.cursor()
        cursor.execute(sql_tablice_active, (tablica_edyt_active,))
        bramka_active = 0

        for row in cursor:
            print(row)
            bramka_active = 1

        if bramka_active == 0:
            print("BRAMA ZAMKNIĘTA")
        elif bramka_active == 1:
            print("BRAMA OTWARTA")
            break



    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:

        break

cap.release()
cv2.destroyAllWindows()



foto = cv2.imread('TEST25.jpg')
foto = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
tablice_rej_static = tablica_casade.detectMultiScale(foto)
for (x, y, w, h) in tablice_rej_static:
    foto2 = foto[y:y + +h, x:x + w + 60, :]
    thresh = cv2.threshold(foto2, 110, 255, cv2.THRESH_BINARY)[1]

width = x +120
height = y - 480
xwith = x + w + 140
yheight = y + h - 520

from pytesseract import image_to_string
odczyt_tabicy = image_to_string(thresh, lang='eng', config='--psm 9')
tablica_edyt_static = odczyt_tabicy.rstrip()
print(odczyt_tabicy)
#print(len(tablica_edyt_static))
tablica_edyt_static = re.sub("[^A-Z0-9]", "", tablica_edyt_static)

sql_tablice_static = "SELECT id, name, idcolor_car, number_plates FROM users WHERE number_plates = %s"
cursor = connection.cursor()
cursor.execute(sql_tablice_static, (tablica_edyt_static, ))

bramka_static = 0

for row in cursor:
    print(row)
    bramka_static = 1

if bramka_static == 0:
    print("BRAMA ZAMKNIĘTA")
elif bramka_static == 1:
    print("BRAMA OTWARTA")

#for i in tablica_edyt_static:

 #   print(i)

#plt.imshow(foto2)
#plt.show()

plt.imshow(thresh)
plt.show()

#print(height)
#print(yheight)
#print(width)
#print(xwith)

#test_obraz1 = cv2.rectangle(foto, (width+120,height-480), (xwith+80, yheight-520), (255,255,0), 5)
cut_color = foto[height:yheight, width:xwith, :]
#plt.imshow(test_obraz1)
#plt.show()
plt.imshow(cut_color)
plt.show()
cut_x = (xwith - width) / 2
cut_y = (yheight - height) / 2 # trzeba zamienić na liczbę całkowitą

print(cut_y)
print(cut_x)
px = cut_color[90,240]
print(px)

if px[0] >= 250 and px[1] <= 5 and px[2] <= 5:
    print('czerwony')
    read_color = "Czerwony"
elif px[0] <= 5 and px[1] >= 250 and px[2] <= 5:
    print('zielony')
    read_color = "Zielony"
elif px[0] <= 5 and px[1] <= 5 and px[2] >= 250:
    print('niebieski')
    read_color = "Niebieski"
elif px[0] >= 250 and px[1] >= 250 and px[2] <= 5:
    print('żółty')
    read_color = "Żółty"
elif px[0] >= 240 and px[1] <= 5 and px[2] >= 240:
    print('fioletowy')
    read_color = "Fioletowy"
elif px[0] <= 5 and px[1] >= 240 and px[2] >= 240:
    print('turkusowy')
    read_color = "Turkusowy"
elif px[0] >= 250 and px[1] >= 250 and px[2] >= 250:
    print('biały')
    read_color = "Biały"
elif px[0] <= 5 and px[1] <= 5 and px[2] <= 5:
    print('czarny')
    read_color = "Czarny"
elif px[0] >= 128 and px[1] <= 20 and px[2] <= 20:
    print('bordo')
    read_color = "Bordo"
elif px[0] >= 110 and px[1] >= 120 and px[2] >= 120:
    print('szary')
    read_color = "Szary"
elif px[0] <= 10 and px[1] >= 42 and px[2] >= 110:
    print('granatowy')
    read_color = "Granatowy"
elif px[0] >= 240 and px[1] >= 115 and px[2] <= 5:
    print('pomarańczowy')
    read_color = "Pomarańcz"


VW = "pusty"
HY = "pusty"
REN = "pusty"
AD = "pusty"
TY = "pusty"

vw = vw_cascade.detectMultiScale(foto) ## działa poprawnie może trzeba zmienić model
toyota = toyota_cascade.detectMultiScale(foto)
audi = audi_cascade.detectMultiScale(foto) ## to samo co vw
renault = renault_casade.detectMultiScale(foto) ## działa super
hyundai = hyundai_casade.detectMultiScale(foto)

for (x, y, w, h) in vw:
    VW = "Volkswagen"
    foto3 = cv2.rectangle(foto, (x,y), (x+w, y+h), (255,255,0), 2)

    # cv2.rectangle(img, (x,y), (xw, y+h), (255,255,0), 5)
for (x, y, w, h) in renault:
    REN = "Renault"
    foto3 = cv2.rectangle(foto, (x,y), (x+w, y+h), (0,255,0), 5)

for (x, y, w, h) in toyota:
    TY = "Toyota"
    foto3 = cv2.rectangle(foto, (x,y), (x+w, y+h), (125,125,125), 10)

for (x, y, w, h) in audi:
    AD = "Audi"
    foto3 = cv2.rectangle(foto, (x,y), (x+w, y+h), (255,0,0), 15)

for (x, y, w, h) in hyundai:
    HY = "Hyundai"
    foto3 = cv2.rectangle(foto, (x,y), (x+w, y+h), (0,0,0), 20)

plt.imshow(foto3)
plt.show()

print(VW)
print(AD)
print(HY)
print(TY)
print(REN)

if VW == "Volkswagen":
    sql_VW = "SELECT id, name, idcolor_car, idvehicle_brand, number_plates FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
    cursor = connection.cursor()
    cursor.execute(sql_VW, (VW,read_color,))
    for row in cursor:
        print(row)
if AD == "Audi":
    sql_AD = "SELECT id, name, idcolor_car, idvehicle_brand, number_plates FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
    cursor = connection.cursor()
    cursor.execute(sql_AD, (AD,read_color,))
    for row in cursor:
        print(row)
if TY == "Toyota":
    sql_TY = "SELECT id, name, idcolor_car, idvehicle_brand, number_plates FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
    cursor = connection.cursor()
    cursor.execute(sql_TY, (TY,read_color))
    for row in cursor:
        print(row)
if HY == "Hyundai":
    sql_TY = "SELECT id, name, idcolor_car, idvehicle_brand, number_plates FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
    cursor = connection.cursor()
    cursor.execute(sql_TY, (TY,read_color))
    for row in cursor:
        print(row)
if REN == "Renault":
    sql_REN = "SELECT id, name, idcolor_car, idvehicle_brand, number_plates FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
    cursor = connection.cursor()
    cursor.execute(sql_REN, (REN,read_color))
    for row in cursor:
        print(row)








