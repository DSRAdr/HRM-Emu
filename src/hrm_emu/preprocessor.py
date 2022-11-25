import re
from typing import List, Tuple


def prepareProgramWithMapping(program: str) -> Tuple[List[str], None]:
    output: List[str] = []

    for line in re.sub("--.+|DEFINE((.|\n)*);", "", program).split("\n"):
        if not (line.strip().startswith("--") or line.strip().startswith("COMMENT") or line.isspace() or line == ""):
            output.append(line.strip())

    return (output, None)


def prepareProgram(program: str) -> List[str]:
    '''
    Wrapper function for actual preprocessing, just discards the map though.
    '''
    return prepareProgramWithMapping(program)[0]