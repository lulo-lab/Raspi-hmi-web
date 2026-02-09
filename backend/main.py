from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


#middleware options
origins = [
    "http://localhost:5173",  # Beispiel: dein Frontend URL (z.B. Vue dev server)
    "http://localhost:3000",  # Andere falls du sie nutzt
    "http://localhost",       # oder auch localhost allgemein
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # erlaubt nur diese Hosts, "*" erlaubt alle (nicht empfohlen)
    allow_credentials=True,
    allow_methods=["*"],    # erlaubt alle Methoden wie GET, POST, OPTIONS
    allow_headers=["*"],    # erlaubt alle Header
)


# Anzahl Register
REGISTER_ANZAHL = 16

# Registerspeicher (FPGA-kompatibel)
register_soll = [0] * REGISTER_ANZAHL
register_ist = [0] * REGISTER_ANZAHL

# Metadaten
metadaten = {
    "geraete_name": "DeviceXYZ",
    "seriennummer": "SN123456",
    "firmware_version": "v1.0.0",
    "letzte_aktualisierung": None
}

# Signaldefinitionen

NUMERISCHE_SIGNALE = {

    "spannung":
    {
        "register": 0,
        "min": 0,
        "max": 60
    },

    "strom":
    {
        "register": 1,
        "min": 0,
        "max": 10
    },

    "temperatur":
    {
        "register": 2,
        "min": -40,
        "max": 125
    },
}

BINAERE_SIGNALE = {

    "enable":
    {
        "register": 10,
        "bit": 0
    },

    "reset":
    {
        "register": 10,
        "bit": 1
    },

    "start":
    {
        "register": 10,
        "bit": 2
    },

    "stop":
    {
        "register": 10,
        "bit": 3
    },

    "freigabe":
    {
        "register": 10,
        "bit": 4
    },
}

# Update-Klassen

class FloatWert(BaseModel):
    wert: float

class BinaerWert(BaseModel):
    wert: bool

class MetadatenUpdate(BaseModel):

    geraete_name: str | None = None
    seriennummer: str | None = None
    firmware_version: str | None = None


# Hilfsfunktionen

def get_bit(register, bit):
    return (register >> bit) & 1


def set_bit(register, bit, value):

    if value:
        return register | (1 << bit)
    else:
        return register & ~(1 << bit)


def get_bereich(signalname):

    if signalname not in NUMERISCHE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    return (
        NUMERISCHE_SIGNALE[signalname]["min"],
        NUMERISCHE_SIGNALE[signalname]["max"]
    )


# Numerisch SOLL

@app.post("/numerisch/soll/{signalname}")
def set_numerisch_soll(signalname: str, wert: FloatWert):

    if signalname not in NUMERISCHE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    register = NUMERISCHE_SIGNALE[signalname]["register"]

    min_wert, max_wert = get_bereich(signalname)

    if not (min_wert <= wert.wert <= max_wert):

        raise HTTPException(
            400,
            f"Wert außerhalb Bereich {min_wert} bis {max_wert}"
        )

    register_soll[register] = wert.wert

    return {
        "signal": signalname,
        "register": register,
        "wert": wert.wert
    }


@app.get("/numerisch/soll/{signalname}")
def get_numerisch_soll(signalname: str):

    if signalname not in NUMERISCHE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    register = NUMERISCHE_SIGNALE[signalname]["register"]

    return {
        "signal": signalname,
        "register": register,
        "wert": register_soll[register]
    }


# Numerisch IST

@app.get("/numerisch/ist/{signalname}")
def get_numerisch_ist(signalname: str):

    if signalname not in NUMERISCHE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    register = NUMERISCHE_SIGNALE[signalname]["register"]

    return {
        "signal": signalname,
        "register": register,
        "wert": register_ist[register]
    }


# Binär SOLL

@app.post("/binaer/soll/{signalname}")
def set_binaer_soll(signalname: str, wert: BinaerWert):

    if signalname not in BINAERE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    register = BINAERE_SIGNALE[signalname]["register"]
    bit = BINAERE_SIGNALE[signalname]["bit"]

    register_soll[register] = set_bit(
        register_soll[register],
        bit,
        wert.wert
    )

    return {
        "signal": signalname,
        "register": register,
        "bit": bit,
        "wert": wert.wert
    }


@app.get("/binaer/soll/{signalname}")
def get_binaer_soll(signalname: str):

    if signalname not in BINAERE_SIGNALE:
        raise HTTPException(404, "Signal unbekannt")

    register = BINAERE_SIGNALE[signalname]["register"]
    bit = BINAERE_SIGNALE[signalname]["bit"]

    wert = get_bit(register_soll[register], bit)

    return {
        "signal": signalname,
        "register": register,
        "bit": bit,
        "wert": bool(wert)
    }


# Register direkt (FPGA / Debug)

@app.get("/register/soll")
def get_register_soll():
    return register_soll


@app.get("/register/ist")
def get_register_ist():
    return register_ist


# Metadaten

@app.get("/metadaten")
def get_metadaten():
    return metadaten


@app.post("/metadaten")
def update_metadaten(update: MetadatenUpdate):

    if update.geraete_name is not None:
        metadaten["geraete_name"] = update.geraete_name

    if update.seriennummer is not None:
        metadaten["seriennummer"] = update.seriennummer

    if update.firmware_version is not None:
        metadaten["firmware_version"] = update.firmware_version

    metadaten["letzte_aktualisierung"] = datetime.now()

    return metadaten


#debug
@app.post("/loopback")
def loopback():
    global register_ist, register_soll
    register_ist = register_soll.copy()
    return {"message": "Loopback durchgeführt", "register_ist": register_ist}

