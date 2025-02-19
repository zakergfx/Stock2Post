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
