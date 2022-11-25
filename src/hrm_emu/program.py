from enum import Enum
from typing import List, cast
from hrm_emu.tile import Tile, TileType
import hrm_emu.errors as err

class ProgramState(Enum):
    RUNNING = 1
    FINISHED = 0
    WAITING = -1

class Program:
    _acc: Tile | None         #accumulator
    _i: List[Tile]            #inbox/input
    _o: List[Tile]            #outbox/output
    _mem: List[Tile | None]   #memory
    _prgCnt: int              #program counter
    _intrCnt: int             #instruction counter (number of instructions exec)
    _state: ProgramState      #program state

    _prg: List[str]           #program

    _prgPre: List[str] | None #program before pre-processing
    _prgMap: None             #line mappings between pre-processed and processed

    def __init__(self, program: List[str], memoryInit: List[Tile | None],
                 inbox: List[Tile] = [], programPre: List[str] | None = None,
                 programMap: None = None) -> None:
        self._prg = program
        self._mem = memoryInit
        self._i = inbox

        self._prgPre = programPre
        self._prgMap = programMap

        self._acc = None
        self._o = []
        self._prgCnt = -1
        self._intrCnt = 0        
        self._state = ProgramState.WAITING
        
    @property
    def program(self):
        return self._prg
        
    @property
    def programPre(self):
        return self._prgPre
        
    @property
    def programMap(self):
        return self._prgMap
        
    @property
    def mem(self):
        return self._mem
        
    @property
    def acc(self):
        return self._acc
        
    @property
    def inbox(self):
        return self._i
        
    @property
    def outbox(self):
        return self._o
        
    @property
    def programCounter(self):
        return self._prgCnt        
        
    @property
    def instructionCounter(self):
        return self._intrCnt

    @property
    def state(self):
        return self._state
    
    #=======================
    
    def step(self):
        if (self._state == ProgramState.FINISHED): raise "foo"  # type: ignore

        self._prgCnt += 1
        if (self._prgCnt > len(self._prg) - 1):
            self._state = ProgramState.FINISHED
            return
        self._state = ProgramState.RUNNING

        opcode = self._prg[self._prgCnt].split()[0]
        if (len(self._prg[self._prgCnt].split()) == 2):
            value = self._prg[self._prgCnt].split()[1]
        else:
            value = None

        if (value == None):
            #0 PARAM OPCODES
            match opcode:
                case "INBOX":
                    if (len(self._i) > 0):
                        self._acc = self._i.pop(0)
                    else:
                        self._state = ProgramState.FINISHED
                        return
                case "OUTBOX":
                    if (self._acc != None):
                        self._o.append(self._acc)
                        self._acc = None
                    else:
                        raise err.EMPTY_VALUE
                case _:
                    #temp hack
                    if not opcode.endswith(":"):
                        raise err.INVALID_OPCODE(opcode)
                    else:
                        return
        else:
            #1 PARAM OPCODES
            match opcode:
                case "COPYFROM":
                    if self._mem[self.getAddress(value)] != None:
                        self._acc = self._mem[self.getAddress(value)]
                    else:
                        raise err.EMPTY_VALUE
                case "COPYTO":
                    if self._acc != None and self.getAddress(value) < len(self._mem) and self.getAddress(value) >= 0:
                        self._mem[self.getAddress(value)] = self._acc
                    elif self._acc == None:
                        raise err.EMPTY_VALUE
                    else:
                        raise err.OUT_OF_BOUNDS

                case "ADD":
                    if self._acc != None and self._mem[self.getAddress(value)] != None:
                        self._acc += cast(Tile, self._mem[self.getAddress(value)])
                    else:
                        raise err.EMPTY_VALUE
                case "SUB":
                    if self._acc != None and self._mem[self.getAddress(value)] != None:
                        self._acc -= cast(Tile, self._mem[self.getAddress(value)])
                    else:
                        raise err.EMPTY_VALUE      

                case "JUMP":
                    self._prgCnt = self._prg.index(value + ":")
                case "JUMPZ":
                    if (self._acc != None and self._acc.value == 0 and self._acc.type == TileType.INTEGER):
                        self._prgCnt = self._prg.index(value + ":")
                case "JUMPN":
                    if (self._acc != None and self._acc.value < 0 and self._acc.type == TileType.INTEGER):
                        self._prgCnt = self._prg.index(value + ":")

                case "BUMPUP":
                    if self._mem[self.getAddress(value)] != None:
                        self._mem[self.getAddress(value)] += 1  # type: ignore
                        self._acc = self._mem[self.getAddress(value)]
                    else:
                        raise err.EMPTY_VALUE
                case "BUMPDN":
                    if self._mem[self.getAddress(value)] != None:
                        self._mem[self.getAddress(value)] -= 1  # type: ignore
                        self._acc = self._mem[self.getAddress(value)]
                    else:
                        raise err.EMPTY_VALUE
                case _:
                    raise err.INVALID_OPCODE(opcode)                   

    def getAddress(self, adrParse: str) -> int:
        if (adrParse.startswith("[")):
            adr = int(adrParse[1:-1])
            tile = self._mem[adr]
            if (tile == None):
                raise err.EMPTY_VALUE
            if (tile.type == TileType.LETTER):
                raise err.TYPE_ERROR
            if (tile.type == TileType.INTEGER):
                return tile.value
        return int(adrParse)        

    def displayMem(self):
        #Get header
        if (self._prgCnt == -1):
            title = "START"
        elif (self._prgCnt >= len(self._prg)):
            title = "END"
        else:
            title = self._prg[self._prgCnt]

        print(title)
        print(f"i: {self._i}")
        print(f"a: {self._acc}")

        print("mem: [", end="")
        for (i, item) in enumerate(self._mem):
            print(f"{i}: {item}", sep="", end="")
            if (i != len(self._mem) - 1):
                print(", ", end="")
        print("]")
        
        print(f"o: {self._o}")
        print("==========")
