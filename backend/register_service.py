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

        # FPGA Register
        self.register_soll = [0] * self.register_count
        self.register_ist = [0] * self.register_count

        self.num_map = self.map["numerisch"]
        self.bin_map = self.map["binaer"]

    # ------------------------------------------------
    # Bitoperationen
    # ------------------------------------------------

    def _get_bit(self, value, bit):
        return (value >> bit) & 1

    def _set_bit(self, value, bit, state):

        if state:
            return value | (1 << bit)
        else:
            return value & ~(1 << bit)

    # ------------------------------------------------
    # Skalierung
    # ------------------------------------------------

    def _to_register(self, signal, value):

        scale = signal.get("scale", 1.0)

        return int(round(value * scale))

    def _from_register(self, signal, value):

        scale = signal.get("scale", 1.0)

        return value / scale

    # ------------------------------------------------
    # Bereich prüfen
    # ------------------------------------------------

    def _check_range(self, signal, value):

        if "min" in signal and value < signal["min"]:
            raise ValueError(
                f"Wert {value} kleiner als Minimum {signal['min']}"
            )

        if "max" in signal and value > signal["max"]:
            raise ValueError(
                f"Wert {value} größer als Maximum {signal['max']}"
            )

    # ------------------------------------------------
    # Zugriff prüfen
    # ------------------------------------------------

    def _check_write_access(self, signal):

        if signal.get("access", "rw") != "rw":
            raise PermissionError("Signal ist read-only")

    # ------------------------------------------------
    # NUMERISCH SOLL
    # ------------------------------------------------

    def set_numerisch_soll(self, name, value):

        if name not in self.num_map:
            raise KeyError("Signal unbekannt")

        signal = self.num_map[name]

        self._check_write_access(signal)

        self._check_range(signal, value)

        reg = signal["register"]

        reg_value = self._to_register(signal, value)

        self.register_soll[reg] = reg_value

        return reg_value

    def get_numerisch_soll(self, name):

        signal = self.num_map[name]

        reg = signal["register"]

        reg_value = self.register_soll[reg]

        return self._from_register(signal, reg_value)

    def get_numerisch_ist(self, name):

        signal = self.num_map[name]

        reg = signal["register"]

        reg_value = self.register_ist[reg]

        return self._from_register(signal, reg_value)

    # ------------------------------------------------
    # BINAER SOLL
    # ------------------------------------------------

    def set_binaer_soll(self, name, state):

        if name not in self.bin_map:
            raise KeyError("Signal unbekannt")

        signal = self.bin_map[name]

        self._check_write_access(signal)

        reg = signal["register"]
        bit = signal["bit"]

        self.register_soll[reg] = self._set_bit(
            self.register_soll[reg],
            bit,
            state
        )

    def get_binaer_soll(self, name):

        signal = self.bin_map[name]

        reg = signal["register"]
        bit = signal["bit"]

        return bool(
            self._get_bit(self.register_soll[reg], bit)
        )

    def get_binaer_ist(self, name):

        signal = self.bin_map[name]

        reg = signal["register"]
        bit = signal["bit"]

        return bool(
            self._get_bit(self.register_ist[reg], bit)
        )

    # ------------------------------------------------
    # FPGA Zugriff
    # ------------------------------------------------

    def get_register_soll(self):
        return self.register_soll

    def get_register_ist(self):
        return self.register_ist

    def set_register_ist(self, values):

        if len(values) != self.register_count:
            raise ValueError("Falsche Registeranzahl")

        self.register_ist = values.copy()


    def set_register_soll_index(self, index: int, value: int):
        if index < 0 or index >= len(self.register_soll):
            raise Exception("Registerindex außerhalb Bereich")

        if value < 0 or value > 0xFFFF:
            raise Exception("Registerwert außerhalb 16bit Bereich")

        self.register_soll[index] = value


    def get_register_soll_index(self, index: int):

        if index < 0 or index >= len(self.register_soll):
            raise Exception("Registerindex außerhalb Bereich")

        return self.register_soll[index]


    def get_register_ist_index(self, index: int):

        if index < 0 or index >= len(self.register_ist):
            raise Exception("Registerindex außerhalb Bereich")

        return self.register_ist[index]


    def set_register_ist_index(self, index: int, value: int):

        if index < 0 or index >= len(self.register_ist):
            raise Exception("Registerindex außerhalb Bereich")

        if value < 0 or value > 0xFFFF:
            raise Exception("Registerwert außerhalb 16bit Bereich")

        self.register_ist[index] = value


    # ------------------------------------------------
    # Debug
    # ------------------------------------------------

    
