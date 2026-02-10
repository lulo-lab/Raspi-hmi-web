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
# CORS - welche Daten dürfen ausgetauscht werden
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

class Float(BaseModel):
    value: float


class Bool(BaseModel):
    value: bool


class MultiRegister(BaseModel):
    values: list[int]


class Register(BaseModel):
    value: int
    

class Metadaten(BaseModel):

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

    return {
        "numerisch": {
            name: reg.get_numerisch(name)
            for name in reg.num_map
        },
        "binaer": {
            name: reg.get_binaer(name)
            for name in reg.bin_map
        }
    }


# ------------------------------------------------
# NUMERISCH
# ------------------------------------------------

@app.post("/numerisch/{name}")
def set_num(name: str, req: Float):

    try:

        reg.set_numerisch(name, req.value)

        return {
            "signal": name,
            "value": req.value
        }

    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/numerisch/{name}")
def get_num(name: str):

    try:
        return {"value": reg.get_numerisch(name)}

    except Exception as e:
        raise HTTPException(400, str(e))

# ------------------------------------------------
# BINAER
# ------------------------------------------------

@app.post("/binaer/{name}")
def set_bin(name: str, req: Bool):

    try:

        reg.set_binaer(name, req.value)

        return {"signal": name, "value": req.value}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/binaer/{name}")
def get_bin(name: str):

    try:
        return {"value": reg.get_binaer(name)}

    except Exception as e:
        raise HTTPException(400, str(e))


# ------------------------------------------------
# REGISTER DIREKT
# ------------------------------------------------

@app.post("/register")
def set_register(req: MultiRegister):

    try:

        reg.set_register(req.values)
        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/register")
def get_register():

    try:
        return {
            "register": reg.get_register()
        }

    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/register/{index}")
def set_register_index(index: int, req: Register):

    try:

        reg.set_register_index(index, req.value)

        return {
            "index": index,
            "value": req.value
        }

    except IndexError:
        raise HTTPException(404, "Register index out of range")

    except Exception as e:
        raise HTTPException(400, str(e))
        
        
@app.get("/register/{index}")
def get_register_index(index: int):

    try:
        value = reg.get_register_index(index)

        return {
            "index": index,
            "value": value
        }

    except IndexError:
        raise HTTPException(404, "Register index out of range")

    except Exception as e:
        raise HTTPException(400, str(e))

# ------------------------------------------------
# METADATEN
# ------------------------------------------------

@app.post("/metadaten")
def update_metadaten(update: Metadaten):

    if update.geraete_name is not None:
        metadaten["geraete_name"] = update.geraete_name

    if update.seriennummer is not None:
        metadaten["seriennummer"] = update.seriennummer

    if update.firmware_version is not None:
        metadaten["firmware_version"] = update.firmware_version

    metadaten["letzte_aktualisierung"] = datetime.now()

    return metadaten


@app.get("/metadaten")
def get_metadaten():

    return metadaten
