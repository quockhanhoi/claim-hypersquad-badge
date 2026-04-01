import sys
import io
import time
from colorama import init, Fore, Style

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

init(autoreset=True)

quangthangcoder = Fore.CYAN
quangthangtruong = Fore.LIGHTCYAN_EX
iconInfo = f"{quangthangcoder}◆{Style.RESET_ALL}"
iconSuccess = f"{quangthangcoder}★{Style.RESET_ALL}"
iconError = f"{quangthangcoder}✕{Style.RESET_ALL}"
iconWarning = f"{quangthangcoder}⚠{Style.RESET_ALL}"

def printBanner(content):
    print(f"{quangthangcoder}{content}{Style.RESET_ALL}")

def printInfo(content):
    currentTime = time.strftime("%H:%M:%S")
    print(f"{quangthangtruong}[{currentTime}] {iconInfo} {quangthangcoder}{content}{Style.RESET_ALL}")

def printSuccess(content):
    currentTime = time.strftime("%H:%M:%S")
    print(f"{quangthangtruong}[{currentTime}] {iconSuccess} {quangthangcoder}{content}{Style.RESET_ALL}")

def printError(content):
    currentTime = time.strftime("%H:%M:%S")
    print(f"{quangthangtruong}[{currentTime}] {iconError} {quangthangcoder}{content}{Style.RESET_ALL}")

def printWarning(content):
    currentTime = time.strftime("%H:%M:%S")
    print(f"{quangthangtruong}[{currentTime}] {iconWarning} {quangthangcoder}{content}{Style.RESET_ALL}")