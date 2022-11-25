from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import cast

import hrm_emu.errors as err


class TileType(Enum):
    INTEGER = 0
    LETTER = 1

@dataclass
class Tile:
    value: int
    type: TileType = TileType.INTEGER

    def __repr__(self) -> str:
        if (self.type == TileType.LETTER):
            return chr(ord('A') + self.value - 1)
        else:
            return str(self.value)

    def __init__(self, other: int | str):
        if (type(other) is str and len(other) == 1):
            self.type = TileType.LETTER
            self.value = ord(other.upper()) - ord('A') + 1
            if (self.value > 26 or self.value < 1):
                raise err.OVERFLOW
        elif (type(other) is int):
            self.type = TileType.INTEGER
            self.value = other
            if (self.value > 999 or self.value < -999):
                raise err.OVERFLOW
        else:
            raise err.TYPE_ERROR

    def __add__(self, other: Tile | int):
        if (type(other) == int):
            return Tile(self.value + cast(int, other))

        else:
            if (self.type == cast(Tile, other).type and self.type == TileType.INTEGER):
                return Tile(self.value + cast(Tile, other).value)
            else:
                raise err.TYPE_ERROR

    def __sub__(self, other: Tile | int):
        if (type(other) == int):
            return Tile(self.value - cast(int, other))

        else:
            if (self.type == cast(Tile, other).type):
                return Tile(self.value - cast(Tile, other).value)
            else:
                raise err.TYPE_ERROR
