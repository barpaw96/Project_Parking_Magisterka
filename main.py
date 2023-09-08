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

        if odczyt_tablicy_activ[2] == " " or odczyt_tablicy_activ[3] == " ":
            tablica_edyt_active = re.sub("[^A-Z0-9]", "", tablica_edyt_active)
            sql_tablice_active = "SELECT id, name, idcolor_car, number_plates FROM users WHERE number_plates = %s"

            cursor = connection.cursor()
            cursor.execute(sql_tablice_active, (tablica_edyt_active,))
            bramka_active = 0

            for row in cursor:
                print(row)
                bramka_active = 1
                print(row[1])
            if bramka_active == 0:
                print("BRAMA ZAMKNIĘTA")
            elif bramka_active == 1:
                print("BRAMA OTWARTA")
                break
        else:
            print("Tablica jest niepoprawna")
            break


    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 78 or k == 110:  ##duże i małe n

        break

cap.release()
cv2.destroyAllWindows()

while True:

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

    read_tablic_error = odczyt_tabicy
    read_tablic_error_sql = read_tablic_error.replace(" ", "%")
    odczyt_tabicy = odczyt_tabicy.lstrip()
    sprawdzenie_tablicy_w_zanki_puste = 0
    dlugosc_iteracji = len(read_tablic_error) - 1
    if read_tablic_error[2] == " " and read_tablic_error[3] == range(0,9):

        for i in range(0,dlugosc_iteracji):
            if i == 2:
                i +=1
            elif read_tablic_error[i] == " ":
                sprawdzenie_tablicy_w_zanki_puste = 1
    elif read_tablic_error[3] == " ":
        for i in range(0,dlugosc_iteracji):
            if i == 3:
                i +=1
            elif read_tablic_error[i] == " ":
                sprawdzenie_tablicy_w_zanki_puste = 1

#    print(sprawdzenie_tablicy_w_zanki_puste)

#    print(read_tablic_error)
#    print(read_tablic_error_sql)

    tablica_edyt_static = odczyt_tabicy.rstrip()




#    print(odczyt_tabicy)
#    print(len(odczyt_tabicy))


    if tablica_edyt_static[2] == " " or tablica_edyt_static[3] == " ":
        tablica_edyt_static = re.sub("[^A-Z0-9]", "", tablica_edyt_static)
        print(tablica_edyt_static)
        print(len(tablica_edyt_static))
        sql_tablice_static = "SELECT id, name, idcolor_car, number_plates FROM users WHERE number_plates = %s"
        cursor = connection.cursor()
        cursor.execute(sql_tablice_static, (tablica_edyt_static,))

        bramka_static = 0

        for row in cursor:
            #print(row)
            bramka_static = 1

        if bramka_static == 1:
            print(odczyt_tabicy,"BRAMA OTWARTA ")
            break
        elif bramka_static == 0:
            print("BRAMA ZAMKNIĘTA")
            sql_tablice_niepelne1 = tablica_edyt_static.replace("W", "%")
            sql_tablice_niepelne2 = sql_tablice_niepelne1.replace("A", "%")
            sql_tablice_niepelne3 = sql_tablice_niepelne2.replace("Z", "%")
            sql_tablice_niepelne4 = sql_tablice_niepelne3.replace("H", "%")
            sql_tablice_niepelne5 = sql_tablice_niepelne4.replace("N", "%")
            sql_tablice_niepelne6 = sql_tablice_niepelne5.replace("O", "%")
            sql_tablice_niepelne7 = sql_tablice_niepelne6.replace("I", "%")
            sql_tablice_niepelne8 = sql_tablice_niepelne7.replace("D", "%")
            sql_tablice_niepelne9 = sql_tablice_niepelne8.replace("S", "%")
            sql_tablice_niepelne10 = sql_tablice_niepelne9.replace("1", "%")
            sql_tablice_niepelne11 = sql_tablice_niepelne10.replace("7", "%")
            sql_tablice_niepelne12 = sql_tablice_niepelne11.replace("2", "%")
            sql_tablice_niepelne13 = sql_tablice_niepelne12.replace("0", "%")
            sql_tablice_niepelne14 = sql_tablice_niepelne13.replace("5", "%")

            sql_tablice_niepelne = sql_tablice_niepelne14

#            print(sql_tablice_niepelne)

#            plt.imshow(thresh)
#            plt.show()

            cut_color = foto[height:yheight, width:xwith, :]

#            plt.imshow(cut_color)
#            plt.show()
            cut_x = (xwith - width) / 2
            cut_y = (yheight - height) / 2 # trzeba zamienić na liczbę całkowitą

            px = cut_color[90,240]

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

#            plt.imshow(foto3)
#            plt.show()

#            print(VW)
#            print(AD)
#            print(HY)
#            print(TY)
#            print(REN)
            lenrowtabHY = 0
            lenrowtabTY = 0
            lenrowtabREN = 0
            lenrowtabVW = 0
            lenrowtabAD = 0
            lenrowtaberrorHY = 0
            lenrowtaberrorTY = 0
            lenrowtaberrorREN = 0
            lenrowtaberrorVW = 0
            lenrowtaberrorAD = 0
            lenrowHY = 0
            lenrowTY = 0
            lenrowREN = 0
            lenrowVW = 0
            lenrowAD = 0

            if VW == "Volkswagen":
                sql_VW = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                         "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
                cursor = connection.cursor()
                cursor.execute(sql_VW, (VW, read_color))
                for rowVW in cursor:
                    print(rowVW)
                    lenrowVW = rowVW[0]

            if AD == "Audi":
                sql_AD = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                         "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
                cursor = connection.cursor()
                cursor.execute(sql_AD, (AD, read_color))
                for rowAD in cursor:
                    print(rowAD)
                    lenrowAD = rowAD[0]
            if TY == "Toyota":
                sql_TY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                         "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s "
                cursor = connection.cursor()
                cursor.execute(sql_TY, (TY, read_color))
                for rowTY in cursor:
                    print(rowTY)
                    lenrowTY = rowTY[0]
            if HY == "Hyundai":
                sql_HY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                         "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s"
                cursor = connection.cursor()
                cursor.execute(sql_HY, (HY, read_color))
                for rowHY in cursor:
                    print(rowHY)
                    lenrowHY = rowHY[0]
            if REN == "Renault":
                sql_REN = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                          "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s "
                cursor = connection.cursor()
                cursor.execute(sql_REN, (REN, read_color))
                for rowREN in cursor:
                    print(rowREN)
                    lenrowREN = rowREN[0]


            if len(tablica_edyt_static) == 7 or len(tablica_edyt_static)==8:
                if VW == "Volkswagen":
                    sql_VW = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_VW, (VW,read_color,sql_tablice_niepelne))
                    for rowtabVW in cursor:
                        print(rowtabVW)
                        lenrowtabVW = rowtabVW[0]

                if AD == "Audi":
                    sql_AD = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_AD, (AD,read_color, sql_tablice_niepelne))
                    for rowtabAD in cursor:
                        print(rowtabAD)
                        lenrowtabAD = rowtabAD[0]
                if TY == "Toyota":
                    sql_TY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_TY, (TY,read_color, sql_tablice_niepelne))
                    for rowtabTY in cursor:
                        print(rowtabTY)
                        lenrowtabTY = rowtabTY[0]
                if HY == "Hyundai":
                    sql_HY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_HY, (HY,read_color, sql_tablice_niepelne))
                    for rowtabHY in cursor:
                        print(rowtabHY)
                        lenrowtabHY = rowtabHY[0]
                if REN == "Renault":
                    sql_REN = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_REN, (REN,read_color, sql_tablice_niepelne))
                    for rowtabREN in cursor:
                        print(rowtabREN)
                        lenrowtabREN = rowtabREN[0]

                lentabend = lenrowtabREN + lenrowtabHY + lenrowtabAD + lenrowtabTY + lenrowtabVW
                lenend = lenrowREN + lenrowHY + lenrowTY + lenrowAD + lenrowVW

                if lentabend == 0:
                    szansa_trafien_not_tab = (1 / lenend) * 100
                    print(odczyt_tabicy)
                    print("Użytkonik nie zajerstrowany! \n Należy skorzystaćc z parkometru", \
                          "Możesz być 1 z: ", lenend)
                    break
                elif lentabend > 0:
                    szansa_trafienia = (lentabend / lenend) * 100
                    if szansa_trafienia < 80:
                        print(odczyt_tabicy)
                        print("Należy skorzystać z parkometru.")

                        break
                    elif szansa_trafienia > 80   and szansa_trafienia < 90:
                        print(odczyt_tabicy)
                        print("Pprawdopodobnie jesteś naszym klinetem")
                        print("Zaleca się skorzystać z parkometru")
                        break
                    else:
                        print(odczyt_tabicy)
                        print("Dziękujemy za skorzystanie z naszych  usług")
                        break


            elif len(tablica_edyt_static) != 7 or len(tablica_edyt_static) !=8 or sprawdzenie_tablicy_w_zanki_puste == 1:

                if VW == "Volkswagen":
                    sql_VW = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                             "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_VW, (VW, read_color, read_tablic_error_sql))
                    for rowtabVW in cursor:
                        print(rowtabVW)
                        lenrowtaberrorVW = rowtabVW[0]

                if AD == "Audi":
                    sql_AD = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                             "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_AD, (AD, read_color, read_tablic_error_sql))
                    for rowtabAD in cursor:
                        print(rowtabAD)
                        lenrowtaberrorAD = rowtabAD[0]
                if TY == "Toyota":
                    sql_TY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                             "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_TY, (TY, read_color, read_tablic_error_sql))
                    for rowtabTY in cursor:
                        print(rowtabTY)
                        lenrowtaberrorTY = rowtabTY[0]
                if HY == "Hyundai":
                    sql_HY = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                             "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_HY, (HY, read_color, read_tablic_error_sql))
                    for rowtabHY in cursor:
                        print(rowtabHY)
                        lenrowtaberrorHY = rowtabHY[0]
                if REN == "Renault":
                    sql_REN = "SELECT row_number() over (order by id), name, idcolor_car, idvehicle_brand, number_plates " \
                              "FROM users WHERE idvehicle_brand = %s AND idcolor_car =%s AND number_plates like %s"
                    cursor = connection.cursor()
                    cursor.execute(sql_REN, (REN, read_color, read_tablic_error_sql))
                    for rowtabREN in cursor:
                        print(rowtabREN)
                        lenrowtaberrorREN = rowtabREN[0]
                lentaberrorend = lenrowtaberrorREN + lenrowtaberrorTY + lenrowtaberrorVW + lenrowtaberrorAD + lenrowtaberrorHY
                lenend = lenrowREN + lenrowHY + lenrowTY + lenrowAD + lenrowVW

                if lentaberrorend == 0:
                    szansa_trafien_not_tab = (1 / lenend) * 100
                    print(odczyt_tabicy)
                    print("Użytkonik nie zajerstrowany! \n Należy skorzystaćc z parkometru", \
                          "Możesz być 1 z: ", lenend)
                    break
                elif lentaberrorend > 0:
                    szansa_trafienia = (lentaberrorend / lenend) * 100
                    if szansa_trafienia < 80:
                        print(odczyt_tabicy)
                        print("Należy skorzystać z parkometru.")

                        break
                    elif szansa_trafienia > 80 and szansa_trafienia < 90:
                        print(odczyt_tabicy)
                        print("Pprawdopodobnie jesteś naszym klinetem")
                        print("Zaleca się skorzystać z parkometru")
                        break
                    else:
                        print(odczyt_tabicy)
                        print("Dziękujemy za skorzystanie z naszych  usług")
                        break







    else:
        print("Tablica nie jest poprawnie rozpoznana")
        break




