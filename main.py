import os
from module.config import banner, maxThreads, tokenFile
from module.claimer import BadgeClaimer
from module.color import printWarning, printError, printBanner

def hypersquadClaimByQuangThangCoder():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        printBanner(banner)
        
        badgeClaimer = BadgeClaimer(maxThreads=maxThreads)
        badgeClaimer.runProcess(tokenFile)
    except KeyboardInterrupt:
        printWarning("exit...")
    except Exception as systemError:
        printError(f"Error: {str(systemError)}")

if __name__ == "__main__":
    hypersquadClaimByQuangThangCoder()