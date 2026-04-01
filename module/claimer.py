import random
import time
from dataclasses import dataclass
from typing import List, Optional
from threading import Thread
from queue import Queue, Empty
from module.color import printInfo, printSuccess, printError, printWarning
from module.discord import DiscordAPI
from module.rate_limit import RateLimitManager

@dataclass
class DiscordAccount:
    token: str
    
    @property
    def tokens(self) -> str:
        if len(self.token) > 10:
            return f"{self.token[:10]}...{self.token[-6:]}"
        return "token die or very"

    @classmethod
    def fromLine(cls, line: str) -> Optional['DiscordAccount']:
        tokenStr = line.strip()
        if tokenStr:
            return cls(token=tokenStr)
        return None

class BadgeClaimer:
    quangthang = {
        1: "Bravery",
        2: "Brilliance",
        3: "Balance"
    }

    def __init__(self, maxThreads: int = 3):
        self.maxThreads = maxThreads
        self.accountQueue = Queue()
        self.isRunning = True
        self.rateLimitManager = RateLimitManager()

    def loadAccounts(self, fileToken: str) -> List[DiscordAccount]:
        accountList = []
        try:
            with open(fileToken, 'r', encoding='utf-8') as fileData:
                for lineNum, lineContent in enumerate(fileData, 1):
                    accountObj = DiscordAccount.fromLine(lineContent)
                    if accountObj:
                        accountList.append(accountObj)
            return accountList
        except Exception:
            return []

    def claimBadgeApi(self, account: DiscordAccount) -> bool:
        discordApi = DiscordAPI(account.token)
        houseId = random.randint(1, 3)
        
        try:
            printInfo(f"Claim {self.quangthang[houseId]} | Token: {account.tokens}")
            response = discordApi.claimHypeSquad(houseId)
            
            if response.status_code == 204:
                printSuccess(f"Claim success {self.quangthang[houseId]} | Token: {account.tokens}")
                return True
            
            elif response.status_code == 401:
                printError(f"Token die or very | Token: {account.tokens}")
            
            elif response.status_code == 429:
                retryAfter = int(response.headers.get('Retry-After', 60))
                self.rateLimitManager.addAccount(account, retryAfter)
                printWarning(f"Rate limit | Token: {account.tokens} | Sẽ thử lại sau {retryAfter}s")
            
            else:
                printError(f"Không thể nhận huy hiệu | Token: {account.tokens}")
        finally:
            discordApi.closeSession()

    def workerThread(self):
        while self.isRunning:
            try:
                accountData = self.accountQueue.get_nowait()
            except Empty:
                break
            
            self.claimBadgeApi(accountData)
            self.accountQueue.task_done()
            time.sleep(random.uniform(1, 3))

    def runProcess(self, tokenFile: str):
        accountList = self.loadAccounts(tokenFile)
            
        if not accountList:
            printWarning("k có token. exit...")
            return
        for accountObj in accountList:
            self.accountQueue.put(accountObj)

        activeThreads = []
        for _ in range(min(self.maxThreads, len(accountList))):
            newThread = Thread(target=self.workerThread)
            newThread.daemon = True  
            newThread.start()
            activeThreads.append(newThread)

        self.accountQueue.join()
        self.isRunning = False
        
        for pThread in activeThreads:
            pThread.join(timeout=1.0)  

        self.rateLimitManager.processLimitedAccounts(self.claimBadgeApi)
