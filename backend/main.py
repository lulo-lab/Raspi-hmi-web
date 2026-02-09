from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from register_service import RegisterService


# ------------------------------------------------
# INIT
# ------------------------------------------------

app = FastAPI(title="FPGA HMI Backend")

reg = RegisterService("register_map.json")


# ------------------------------------------------
# CORS
# ------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------
# REQUEST MODELS
# ------------------------------------------------

class FloatValue(BaseModel):
    value: float


class BoolValue(BaseModel):
    value: bool


class RegisterWrite(BaseModel):
    values: list[int]


class MetadatenUpdate(BaseModel):

    geraete_name: str | None = None
    seriennummer: str | None = None
    firmware_version: str | None = None


# ------------------------------------------------
# METADATEN
# ------------------------------------------------

metadaten = {
    "geraete_name": "DeviceXYZ",
    "seriennummer": "SN123456",
    "firmware_version": "v1.0.0",
    "letzte_aktualisierung": None
}


# ------------------------------------------------
# SIGNAL LISTE
# ------------------------------------------------

@app.get("/signals")
def get_signals():

    return {
        "numerisch": list(reg.num_map.keys()),
        "binaer": list(reg.bin_map.keys())
    }


# ------------------------------------------------
# GESAMTZUSTAND (Frontend Hauptendpoint)
# ------------------------------------------------

@app.get("/state")
def get_state():

    numerisch_soll = {}
    numerisch_ist = {}

    binaer_soll = {}
    binaer_ist = {}

    for name in reg.num_map:

        numerisch_soll[name] = reg.get_numerisch_soll(name)
        numerisch_ist[name] = reg.get_numerisch_ist(name)

    for name in reg.bin_map:

        binaer_soll[name] = reg.get_binaer_soll(name)
        binaer_ist[name] = reg.get_binaer_ist(name)

    return {

        "numerisch":
        {
            "soll": numerisch_soll,
            "ist": numerisch_ist
        },

        "binaer":
        {
            "soll": binaer_soll,
            "ist": binaer_ist
        },

        "register":
        {
            "soll": reg.get_register_soll(),
            "ist": reg.get_register_ist()
        },

        "metadaten": metadaten
    }


# ------------------------------------------------
# NUMERISCH
# ------------------------------------------------

@app.post("/numerisch/soll/{name}")
def set_num_soll(name: str, req: FloatValue):

    try:

        reg_value = reg.set_numerisch_soll(name, req.value)

        return {
            "signal": name,
            "value": req.value,
            "register": reg_value
        }

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/numerisch/soll/{name}")
def get_num_soll(name: str):

    try:
        return {"value": reg.get_numerisch_soll(name)}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/numerisch/ist/{name}")
def get_num_ist(name: str):

    try:
        return {"value": reg.get_numerisch_ist(name)}

    except Exception as e:
        raise HTTPException(400, str(e))


# ------------------------------------------------
# BINAER
# ------------------------------------------------

@app.post("/binaer/soll/{name}")
def set_bin_soll(name: str, req: BoolValue):

    try:

        reg.set_binaer_soll(name, req.value)

        return {"signal": name, "value": req.value}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/binaer/soll/{name}")
def get_bin_soll(name: str):

    try:
        return {"value": reg.get_binaer_soll(name)}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/binaer/ist/{name}")
def get_bin_ist(name: str):

    try:
        return {"value": reg.get_binaer_ist(name)}

    except Exception as e:
        raise HTTPException(400, str(e))


# ------------------------------------------------
# REGISTER DIREKT (FPGA Zugriff)
# ------------------------------------------------

@app.get("/register/soll")
def get_register_soll():

    return reg.get_register_soll()


@app.post("/register/soll")
def set_register_soll(req: RegisterWrite):

    try:

        reg.set_register_soll(req.values)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/register/ist")
def get_register_ist():

    return reg.get_register_ist()


@app.post("/register/ist")
def set_register_ist(req: RegisterWrite):

    try:

        reg.set_register_ist(req.values)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(400, str(e))


# ------------------------------------------------
# METADATEN
# ------------------------------------------------

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


# ------------------------------------------------
# LOOPBACK DEBUG
# ------------------------------------------------

@app.post("/loopback")
def loopback():

    reg.loopback()

    return {

        "message": "Loopback OK",
        "register_ist": reg.get_register_ist()
    }
