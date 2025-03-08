import random, time, string, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def formatDate(date):
    try:
        month, year = date.split("/")
        return f"{year}/{month}"
    except:
        return date

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
    sender = "service.zakergfx@gmail.com"
   
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
    serveur.login(sender, "ygpf xybe ktrj uyoh")

    # Envoi de l'email
    try:
        serveur.sendmail(sender, to, message.as_string())
        serveur.quit()
        return True
        
    except:
        serveur.quit()
        return False