import time
from threading import Lock
from module.color import printWarning

class RateLimitManager:
    def __init__(self):
        self.limitedAccounts = []
        self.threadLock = Lock()

    def addAccount(self, account, retryAfter: int):
        with self.threadLock:
            self.limitedAccounts.append({
                'account': account,
                'retryAfter': retryAfter
            })

    def processLimitedAccounts(self, claimFunction):
        with self.threadLock:
            accountsToProcess = self.limitedAccounts.copy()
            self.limitedAccounts.clear()
            
        if not accountsToProcess:
            return

        printWarning(f"Run {len(accountsToProcess)} account rate limited...")
        time.sleep(60)
        
        for item in accountsToProcess:
            claimFunction(item['account'])
