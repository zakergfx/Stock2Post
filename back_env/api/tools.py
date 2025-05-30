import random, time, string, smtplib, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def formatDate(date):
    try:
        month, year = date.split("/")
        return f"{year}/{month}"
    except:
        return date

def convertPrice(price):
    return int(re.sub(r"[^\d]", "", price))

def isValidEmail(email):
    # Expression régulière pour valider une adresse email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Vérifie si l'email correspond à l'expression régulière
    return re.match(regex, email)

def isValidPhoneNumber(phone):
    for number in phone:
        if not number.isdigit() and number != " ":
            return False
        
    return len(phone) >= 9

def formatKm(km):
    return int(km.replace(" ", "").replace("\u202f", "")[:-2])

def formatPrice(price):
    return int(price.replace(" ", "").replace("\u202f", "")[1:].split(",")[0])

def formatPower(power):
    power = power.split(" ")
    kw = int(power[0])
    ch = int(power[2].replace(" ", "").replace("(", "").replace(" CH", ""))
    return kw, ch

def sendMail(to, subject, body):
    # Configuration de l'email
    sender = "REMOVED_EMAIL"
   
    # Création du message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = subject

    # Attacher le corps du texte au message
    message.attach(MIMEText(body, "plain"))

    # Configuration du serveur SMTP
    serveur = smtplib.SMTP("smtp.gmail.com", 587)
    serveur.starttls()  # Sécurisation de la connexion
    serveur.login(sender, "xxxxxxxxx")

    # Envoi de l'email
    try:
        serveur.sendmail(sender, to, message.as_string())
        serveur.quit()
        return True
        
    except:
        serveur.quit()
        return False
