from rich.layout import Layout
from rich.live import Live
#from rich.text import Text
from rich.align import Align

import time

from hrm_emu.program import Program, ProgramState

def fancyOut(program: Program):
    layout = Layout()
    layout.split_row(
        Layout(name="left", ratio=2),
        Layout(name="program")
    )
    layout["left"].split_column(
        Layout(name="memory", ratio=4),
        Layout(name="lower", ratio=3),
        Layout(name="controls")
    )
    layout["lower"].split_row(
        Layout(name="inbox", ratio=3),
        Layout(name="accumulator"),
        Layout(name="outbox", ratio=3)
    )

    with Live(refresh_per_second=30) as live:

        while(program.state != ProgramState.FINISHED):
            time.sleep(0.1)

            layout["accumulator"].update(Align(str(program.acc), align="center", vertical="middle"))
            layout["memory"].update(Align(str(program.mem), align="center", vertical="middle"))
            
            layout["inbox"].update(Align(str(program.inbox), align="left", vertical="middle"))
            layout["outbox"].update(Align(str(program.outbox), align="right", vertical="middle"))
            
            size = live.console.height // 2 - 1
            pos = clamp(program.programCounter, len(program.program))
            minVal = max(0, pos - size)
            maxVal = min(len(program.program) - 1, pos + size + 1)
            foo = [" " + x for x in program.program]
            foo[pos] = ">" + program.program[pos]
            bar = foo[minVal:maxVal]

            layout["program"].update(Align("\n".join(bar), align="left", vertical="middle"))

            live.update(layout)
            program.step()

def clamp(inputVal: int, maxVal: int, minVal: int = 0):
    if inputVal < minVal:
        return minVal
    elif inputVal > maxVal:
        return maxVal
    return inputVal