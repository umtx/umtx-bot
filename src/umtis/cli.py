import os
from umtis import spawn
from umtis import fetch


def main():
    print(
        "1. SPAWN\n2. FETCH\n",end='')
    current_select = int(input())
    if current_select == 1:
        spawn.authorize()
    elif current_select == 2:
        fetch.manual()