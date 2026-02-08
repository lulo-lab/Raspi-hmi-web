from datetime import datetime
from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel

class SystemStatus(str, Enum):
    OK = "OK"
    WARNUNG = "Warnung"
    FEHLER = "Fehler"

class NumerischesSignal(str, Enum):
    SPANNUNG = "spannung"
    STROM = "strom"
    TEMPERATUR = "temperatur"
    LEISTUNG = "leistung"

class BinaeresSignal(str, Enum):
    ENABLE = "enable"
    RESET = "reset"
    FEHLER_QUIT = "fehler_quit"
    BETRIEB = "betrieb"
    BEREIT = "bereit"

class BenutzerInfo(BaseModel):
    benutzername: Optional[str] = None
    rolle: Optional[str] = None

class Metadaten(BaseModel):
    geraete_name: str
    seriennummer: str
    firmware_version: Optional[str] = None
    system_status: SystemStatus = SystemStatus.OK
    fehlercode: Optional[int] = None
    fehlerbeschreibung: Optional[str] = None
    benutzer: Optional[BenutzerInfo] = None

class WerteNumerisch(BaseModel):
    soll: Dict[NumerischesSignal, float]
    ist: Dict[NumerischesSignal, float]

class WerteBinaer(BaseModel):
    soll: Dict[BinaeresSignal, bool]
    ist: Dict[BinaeresSignal, bool]

class DatenBasis(BaseModel):
    numerisch: WerteNumerisch
    binaer: WerteBinaer
    numerisch_geprueft: Optional[WerteNumerisch] = None
    binaer_geprueft: Optional[WerteBinaer] = None
    metadaten: Optional[Metadaten] = None
