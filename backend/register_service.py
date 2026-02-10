import json
from pathlib import Path

class RegisterService:
    def __init__(self, map_file="register_map.json"):
        path = Path(map_file)
        if not path.exists():
            raise Exception(f"Register map nicht gefunden: {map_file}")

        with open(path, "r") as f:
            self.map = json.load(f)

        self.register_count = self.map["register"]["count"]

        # Ein einziges Register-Array für alles
        self.register = [0] * self.register_count

        self.num_map = self.map["numerisch"]
        self.bin_map = self.map["binaer"]

    # -------------------------------
    # Bitoperationen
    # -------------------------------
    def _get_bit(self, value, bit):
        return (value >> bit) & 1

    def _set_bit(self, value, bit, state):
        return value | (1 << bit) if state else value & ~(1 << bit)

    # -------------------------------
    # Skalierung
    # -------------------------------
    def _to_register(self, signal, value):
        scale = signal.get("scale", 1.0)
        return int(round(value * scale))

    def _from_register(self, signal, value):
        scale = signal.get("scale", 1.0)
        return value / scale

    # -------------------------------
    # Bereich prüfen
    # -------------------------------
    def _check_range(self, signal, value):
        if "min" in signal and value < signal["min"]:
            raise ValueError(f"Wert {value} kleiner als Minimum {signal['min']}")
        if "max" in signal and value > signal["max"]:
            raise ValueError(f"Wert {value} größer als Maximum {signal['max']}")

    # -------------------------------
    # Zugriff prüfen
    # -------------------------------
    def _check_write_access(self, signal):
        if signal.get("access", "rw") != "rw":
            raise PermissionError("Signal ist read-only")

    # -------------------------------
    # Numerische Signale
    # -------------------------------
    def set_numerisch(self, name, value):
        if name not in self.num_map:
            raise KeyError("Signal unbekannt")

        signal = self.num_map[name]
        self._check_write_access(signal)
        self._check_range(signal, value)

        reg_index = signal["register"]
        reg_value = self._to_register(signal, value)
        self.register[reg_index] = reg_value
        return reg_value

    def get_numerisch(self, name):
        signal = self.num_map[name]
        reg_index = signal["register"]
        return self._from_register(signal, self.register[reg_index])

    # -------------------------------
    # Binäre Signale
    # -------------------------------
    def set_binaer(self, name, state):
        if name not in self.bin_map:
            raise KeyError("Signal unbekannt")

        signal = self.bin_map[name]
        self._check_write_access(signal)

        reg_index = signal["register"]
        bit = signal["bit"]
        self.register[reg_index] = self._set_bit(self.register[reg_index], bit, state)

    def get_binaer(self, name):
        signal = self.bin_map[name]
        reg_index = signal["register"]
        bit = signal["bit"]
        return bool(self._get_bit(self.register[reg_index], bit))

    # -------------------------------
    # Direkter Registerzugriff
    # -------------------------------
    def get_register(self):
        return self.register

    def set_register(self, values):
        if len(values) != self.register_count:
            raise ValueError("Falsche Registeranzahl")
        self.register = values.copy()

    def get_register_index(self, index):
        if index < 0 or index >= len(self.register):
            raise IndexError("Registerindex außerhalb Bereich")
        return self.register[index]

    def set_register_index(self, index, value):
        if index < 0 or index >= len(self.register):
            raise IndexError("Registerindex außerhalb Bereich")
        if value < 0 or value > 0xFFFF:
            raise ValueError("Registerwert außerhalb 16bit Bereich")
        self.register[index] = value

    # -------------------------------
    # Debug / Loopback
    # -------------------------------
