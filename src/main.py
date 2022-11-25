import click

from typing import List

from hrm_emu import preprocessor
from hrm_emu.program import Program, ProgramState
from hrm_emu.tile import Tile

from lupa import LuaRuntime  # type: ignore

@click.command()
@click.option('--program', '-p',
            type=click.File("r"),
            help="Program to run")
@click.option('--inbox', '-i',
            type=click.File("r"),
            help="Program to run",
            required=False)
@click.option('--fancy', '-f',
            is_flag=True,
            help="Use fancy printing",
            default=False)


def runProgram(program: click.File, inbox: click.File, fancy: bool):
    lua = LuaRuntime() #type: ignore

    programFile = preprocessor.prepareProgram(program.read()) # type: ignore
    inboxFile: str = inbox.read() # type: ignore

    inputFunction = lua.eval(inboxFile) # type: ignore
    inboxList = [Tile(x) for x in luaTableToList(inputFunction())]  # type: ignore

    foo = Program(programFile, mem, inboxList)


    if (fancy):
        from fancy_out import fancyOut
        fancyOut(foo)
    else:
        while(foo.state != ProgramState.FINISHED):
            foo.step()
        foo.displayMem()

def luaTableToList(table): #type: ignore
    return list(table.values()) #type: ignore

mem: List[Tile | None] = [Tile(x) if x != None else x for x in [None] * 23 + [0] + [10]]  # type: ignore

if __name__ == '__main__':
    runProgram()