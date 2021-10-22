#On importe les paquages nécessaires
from math import *
from readCoord import readCoord
import os

#l'ellipsoïde de CHTRS95 (WGS84) à les valeurs suivantes:
a_WGS84 = 6378137 #grand axe
b_WGS84 = 6356752.3142 #petit axe
e2_WGS84 = (a_WGS84**2-b_WGS84**2)/a_WGS84**2 #carré de la première exentricité numérique de l'ellispoïde

#l'ellipsoïde de Bessel (CH1903+) à les valeurs suivantes:
a_CH = 6377397.155 #grand axe
b_CH = 6356078.963 #petit axe
e2_CH = (a_CH**2-b_CH**2)/a_CH**2 #carré de la première exentricité numérique de l'ellispoïde

#Les valeurs de longitude et de latitude de l'origine à Berne sont:
ph_0 = (46+57/60+08.66/3600)*pi/180 #Latitude géographique de l'origine à Berne
l_0 = (7+26/60+22.5/3600)*pi/180 #Longitude géographique de l'origine à Berne

#Le calcul des grandeurs auxilliaires selon §3.1 (Formules et constantes pour le calcul de la projection cylindrique à axe oblique et pour la transformation entre des systèmes de référence)
R_CH = a_CH*sqrt(1-e2_CH)/(1-e2_CH*sin(ph_0)**2) #Rayon de la sphère de projection
alpha_CH = sqrt(1+(e2_CH/(1-e2_CH))*cos(ph_0)**4) #Rapport des longitudes
b_0 = asin(sin(ph_0)/alpha_CH) #Latitude de l'origine sur la sphère
K_CH = log(tan(pi/4 + b_0 /2)) - alpha_CH*log(tan(pi/4+ph_0 / 2)) + alpha_CH*sqrt(e2_CH)/2*log((1+sqrt(e2_CH)*sin(ph_0))/(1-sqrt(e2_CH)*sin(ph_0))) #Constante de la formule des latitudes

#fonction permettant de passer des coordonnées ellipsoïdales en coordonnées cartésiennes dans le système CHTRF95 (WGS84)
def elltocart_WGS(f, l, h):
    '''
    This function permit to do the transformation from elipsoidal coordinate, into cartesian coordinate in the CHTRF95(WGS84) system.
    '''
    f = f*pi/180 #phi
    l = l*pi/180 #lambda
    R_N = a_WGS84/(sqrt(1-e2_WGS84*sin(f)*sin(f))) #Rayon de courbure normal
    X = (R_N + h)*cos(f)*cos(l) 
    Y = (R_N + h)*cos(f)*sin(l)
    Z = (R_N*(1-e2_WGS84)+h)*sin(f)
    return X, Y, Z

#Fonction permettant de passer des coordonnées cartésiennes dans le système CHTRF95 (WGS84) jusqu'en coordonnées cartésiennes dans le système CH1903+ (§1.4)
def WGStoCH(X_WGS, Y_WGS, Z_WGS):
    '''
    This function permit to do the transformation from cartesian coordinate in the CHTRF95(WGS84) system, into cartesian coordinate in the CH1903+ system.
    '''
    X_CH = X_WGS - 674.374
    Y_CH = Y_WGS - 15.056
    Z_CH = Z_WGS - 405.346
    return X_CH, Y_CH, Z_CH

#Fonction permettant de passer des coordonnées cartésiennes en coordonnées ellispoïdales dans le système CH1903+ (§2.2)
def carttoell_CH(X, Y, Z):
    '''
    This function permit to do the transformation from cartesian coordinate into ellipsoidal coordinate in the CH1903+ system.
    '''
    l = atan(Y/X) #lambda
    ph = atan((Z/sqrt(X**2+Y**2))) #phi (valeur de base approchée)
    ph_old = 0 #permet de stocker la valeur de phi entre les itérations
    
    while abs(ph - ph_old) > 10**(-10): #tant que la valeur absolue de la différence entre le nouveau phi et celui calculé à l'itération d'avant est supérieure a 10 puissance -10, on continue
        R_N = a_CH/sqrt(1-e2_CH*sin(ph)**2) #Rayon de courbure normal
        h = (sqrt(X**2+Y**2)/cos(ph))-R_N #hauteur 
        ph_old = ph #on stocke le phi dans phi_old avant de recalculer le nouveau phi
        ph = atan((Z/sqrt(X**2+Y**2))/(1-(R_N*e2_CH/(R_N+h)))) #calcul du nouveau phi
        
    #si on veut en finir là et avoir le phi et le lambda en degré, on peut décommenter les 2 prochaines lignes, mais si on veut utiliser les fonctions d'après, il faut les laisser en commentaire (parce que la fonction suivante demande un phi et un lambda en radian)
    #ph = ph*180/pi
    #l = l*180/pi
    return ph, l, h

#Fonction permettant de passer des coordonnées ellipsoïdales (sur l'ellispoïde de Bessel) jusqu'à des coordonnées suisses en projection (§3.2)
def ell_CHtomercator(ph, l):
    '''
    This function permit to pass from ellipsoidal coordinate (on the Bessel ellipsoid) into swiss coordinate in projection.
    
    There is three steps in this function:
    1. Go from ellipsoidal to spheric
    2. Go from equatorial to pseudo-équatorial system
    3. Go from spheric coordinates to plane coordinates (Mercator projection) 
    '''
    ## Première étape: Ellipsoïdal jusqu'à sphérique
    S = alpha_CH*log(tan(pi/4 + ph/2)) - alpha_CH*sqrt(e2_CH)/2*log((1+sqrt(e2_CH)*sin(ph))/(1-sqrt(e2_CH)*sin(ph))) + K_CH #Valeur auxiliaire
    b = 2*(atan(exp(S))-pi/4) #Latitude sphérique
    L = alpha_CH * (l-l_0) #Longitude sphérique

    ## Deuxième étape: equatorial jusqu'à pseudo-equatorial
    L_bar = atan(sin(L)/(sin(b_0)*tan(b)+cos(b_0)*cos(L)))
    b_bar = asin(cos(b_0)*sin(b)-sin(b_0)*cos(b)*cos(L))

    ##Dernière étape: spherique jusqu'au plan de projection (projection de Mercator)
    Y = R_CH * L_bar +2600000
    X = R_CH/2 * log((1+sin(b_bar))/(1-sin(b_bar))) + 1200000
    
    return(Y, X)

#Fonction permettant d'écrire dans notre fichier de base, à la dernière ligne, nos nouvelles coordonnées, après transformation.
def writeintxt(file, Y, X, h):
    '''
    This function permit to write in our basic file, the new coordinate optained in a new line.
    '''
    S = str(Y) + "[m] " + str(X) + "[m] " + str(h) + "[m]" #forme un ligne de caractère décrivant les coordonnées a partir de nos float obtenus.
    f = open(file, "a") #ouvre notre fichier de base en mode "add", c'est a dire pour ajouter quelque chose.
    f.write("\n" + S) #écris la ligne de caractère a la fin du fichier .txt (après avoir fait un retour à la ligne)
    f.close() #referme le fichier
    print(S)
    return

#Fonction permettant de faire la transformation complète en passant de CHTRF95 (WGS84) en coordonnées ellipsoidale à CH1903+ en coordonnées planes et d'écrire le résultat dans le fichier txt donné de base.
def WGS_CH_Complete(file):
    '''
    this function permit to:
    1. Open the .txt file and take coordinate in it (it's the readCoord() function that is used, imported from another file)
    2. Do the complete transformation from ellispoidal coordinate in CHTRF95(WGS84) system to plane coordinate in CH1903+ system 
    3. Reopen the .txt file and write the result of the transformation in the last line of it
    '''
    read_ph, read_l, read_h = readCoord(file) #utilisation de readCoord.py pour prendre les données du fichier .txt
    read_ph = float(read_ph)
    read_l = float(read_l)
    read_h = float(read_h)
    a, b, c = elltocart_WGS(read_ph, read_l, read_h)
    d, e, f = WGStoCH(a, b, c)
    ph_test, l_test, h_final = carttoell_CH(d,e,f)
    Y_final, X_final = ell_CHtomercator(ph_test, l_test)
    Y_final = round(Y_final, 2)
    X_final = round(X_final, 2)
    h_final = round(h_final, 2)
    writeintxt(file, Y_final, X_final, h_final)
    return

#WGS_CH_Complete("In_WGS84_lab1-2021.txt")

############################################################################################################################################################################################
#TRANSFORMATION INVERSE #####################################
############################################################################################################################################################################################
#Fonction permettant de passer des coordonnées suisses en projection jusqu'aux coordonnées ellipsoïdales
def mercatortoell_CH(E, N):
    '''
    This function permit to pass from swiss coordinate in projection into ellipsoidal coordinate.
    
    There is three steps in this function:
    1. Go from plane coordinates to spheric coordinates
    2. Go from pseudo-équatorial to equatorial system
    3. Go from spheric to ellipsoidal with iterations
    '''
    ##première étape: plan de projection jusqu'à sphère
    Y = E - 2600000
    X = N - 1200000
    I_bar = Y/R_CH
    b_bar = 2*(atan(exp(X/R_CH))-pi/4)
    
    ##Deuxième étape: système pseudo-équatorial jusqu'à système équatorial
    b = asin( cos(b_0) * sin(b_bar) + sin(b_0)*cos(b_bar)*cos(I_bar))
    I = atan(sin(I_bar)/(cos(b_0)*cos(I_bar) - sin(b_0)*tan(b_bar)))
    
    ##Dernière étape: De sphérique jusqu'à ellispoïdal avec itérations (même principe que pour l'autre transformation)
    l = l_0 + I/alpha_CH #lambda
    ph_old = 0  #permet de stocker la valeur de phi entre les itérations
    ph = b #on prend b comme valeur initiale
    while abs(ph - ph_old) > 10**(-10):
        S = 1/alpha_CH *(log(tan(pi/4 +b/2))-K_CH) + sqrt(e2_CH)*log(tan(pi/4 + (asin(sqrt(e2_CH) * sin(ph))/2)))
        ph_old = ph #on stoque la valeur de phi de l'itération précédente dans ph_old
        ph = 2*atan(exp(S))-pi/2 #calcul du nouveau phi
    return ph, l

#Fonction permettant de passer des coordonnées ellipsoïdales jusqu'a des coordonnées cartésiennes géocentriques (CH1903+)
def elltocart_CH(f, l, h):
    '''
    This function permit to pass from ellipsoidal coordinate to geocentric cartesian coordinate (CH1903+). 
    '''
    R_N = a_CH/(sqrt(1-e2_CH*sin(f)*sin(f))) #rayon de courbure normal
    X = (R_N + h)*cos(f)*cos(l)
    Y = (R_N + h)*cos(f)*sin(l)
    Z = (R_N*(1-e2_CH)+h)*sin(f)
    return X, Y, Z

#Fonction permettant de passer de CH1903+ à CHTRS95 (coordonnées cartésiennes)
def CHtoWGS(X_CH, Y_CH, Z_CH):
    '''
    This function permit to pass from cartesian coordinate in CH1903+ to cartesian coordinate in CHTRS95(WGS84).
    '''
    X_WGS = X_CH + 674.374
    Y_WGS = Y_CH + 15.056
    Z_WGS = Z_CH + 405.346
    return X_WGS, Y_WGS, Z_WGS

#Fonction permettant de passer de coordonnées cartésiennes en coordonnées ellipsoïdales dans le système CHTRS95
def carttoell_WGS(X, Y, Z):
    '''
    This function permit to pass from cartesian coordinate in ellipsoidal coordianete in CHTRS(WGS84) system with iterations.
    '''
    l = atan(Y/X) #lambda
    ph = atan((Z/sqrt(X**2+Y**2))) #phi pour le début du calcul
    ph_old = 0  #permet de stocker la valeur de phi entre les itérations
    while abs(ph - ph_old) > 10**(-10): #tant que la valeur absolue de la différence entre le nouveau phi et celui calculé à l'itération d'avant est supérieure a 10 puissance -10, on continue
        R_N = a_WGS84/sqrt(1-e2_WGS84*sin(ph)**2) #rayon de courbure normal
        h = (sqrt(X**2+Y**2)/cos(ph))-R_N #hauteur
        ph_old = ph #on stoque la valeur de phi de l'itération précédente dans ph_old
        ph = atan((Z/sqrt(X**2+Y**2))/(1-(R_N*e2_WGS84/(R_N+h)))) #calcul du nouveau phi
    ph = ph*180/pi #passage en degrés de phi
    l = l*180/pi #passage en degrésde lambda
    return ph, l, h

#Fonction permettant d'écrire dans notre fichier de base, à la dernière ligne, nos nouvelles coordonnées, après transformation.
def writeintxt_deg(file, ph, l, h):
    '''
    This function permit to write in our basic file, the new coordinate optained in a new line.
    '''
    S = str(ph) + "[deg] " + str(l) + "[deg] " + str(h) + "[m]" #forme un ligne de caractère décrivant les coordonnées a partir de nos float obtenus.
    f = open(file, "a")  #ouvre notre fichier de base en mode "add", c'est a dire pour ajouter quelque chose.
    f.write("\n" + S) #écris la ligne de caractère a la fin du fichier .txt (après avoir fait un retour à la ligne)
    f.close() #referme le fichier .txt
    print(S)
    return

#Fonction permettant de faire la transformation complète en passant de CH1903+ en coordonnées planes à CHTRF95 (WGS84) en coordonnées ellipsoidale et d'écrire le résultat dans le fichier txt donné de base.
def CH_WGS_Complete(file):
    '''
    this function permit to:
    1. Open the .txt file and take coordinate in it (it's the readCoord() function that is used, imported from another file)
    2. Do the complete transformation from plane coordinate in CH1903+ system to ellispoidal coordinate in CHTRF95(WGS84) system
    3. Reopen the .txt file and write the result of the transformation in the last line of it
    '''
    read_e, read_n, read_h = readCoord(file)
    read_e = float(read_e)
    read_n = float(read_n)
    read_h = float(read_h)
    ph_CH, l_CH = mercatortoell_CH(read_e, read_n)
    a, b, c = elltocart_CH(ph_CH, l_CH, read_h)
    d, e, f = CHtoWGS(a, b, c)
    ph_final, l_final, h_final = carttoell_WGS(d, e, f)
    ph_final = round(ph_final, 9) #1" \approx 30m => 1° \approx 108000m => 1.10^-9° \approx 1cm
    l_final = round(l_final, 9)
    h_final = round(h_final, 2)
    writeintxt_deg(file, ph_final, l_final, h_final)
    return


#CH_WGS_Complete("In_CH03+_lab1-2020.txt")

######################################################################################################################################################################################################################################################
##### Partie pour executer les fonctions et transformer les coordonnées données. L'utilisation des fonctions "try" et except" est présente pour réduire les Erreurs et augmenter l'utilisabilité du programme ###############################################
######################################################################################################################################################################################################################################################


file = input("Entrer le nom du fichier .txt (sans le .txt):")
trans1 = input("Voulez vous transformer des coordonnées de CHTRF95(WGS84) jusqu'à CH1903+? [oui/non]")
if trans1 == "y" or trans1 == "Y" or trans1 == "yes" or trans1 == "Yes" or trans1 == "oui" or trans1 == "o":
    try:
        WGS_CH_Complete(file + ".txt")
    except (ValueError, FileNotFoundError):
        print("Sorry, your .txt file could not be read. Please make sure that the file is in the working directory and that the coordinates are written in the only line that does not begin with \"#\" (remove all empty lines).")
else:
    trans2 = input("Voulez vous transformer des coordonnées de CH1903+ jusqu'à CHTRF95(WGS84)? [oui/non]")
    if trans2 == "y" or trans2 == "Y" or trans2 == "yes" or trans2 == "Yes" or trans2 == "oui" or trans2 == "o":
        try:
            CH_WGS_Complete(file + ".txt")
        except (ValueError, FileNotFoundError):
            print("Sorry, your .txt file could not be read. Please make sure that the file is in the working directory and that coordinates are written in the only line that does not begin with \"#\" (remove all empty lines).")
    else:
        print("Sorry, these are the only two available transformations.")
