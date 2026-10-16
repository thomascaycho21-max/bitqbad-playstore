"""Servicio de monedas: cache local + persistencia GitHub."""
import json
from .models import Wallet, Transaction
from .github_wallet import GitHubWallet


class CoinsService:
    _instance = None

    def __new__(cls, *a, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.gh = GitHubWallet()
        self.enabled = self.gh.enabled
        self.error = self.gh.error
        self._cache = {}   # user -> Wallet

    # ---------- API ----------
    def get_wallet(self, user: str = "anon") -> Wallet:
        if user in self._cache:
            return self._cache[user]
        data = None
        if self.enabled:
            data = self.gh.load(user)
        if data:
            wallet = Wallet.from_dict(data)
        else:
            wallet = Wallet(user=user, balance=100)   # regalo de bienvenida
        self._cache[user] = wallet
        return wallet

    def add_coins(self, user: str, amount: int, reason: str) -> Wallet:
        wallet = self.get_wallet(user)
        wallet.balance += amount
        wallet.transactions.append(Transaction(amount=amount, reason=reason))
        # limite de historial
        wallet.transactions = wallet.transactions[-50:]
        self._cache[user] = wallet
        # persistir
        if self.enabled:
            self.gh.save(user, wallet.to_dict())
        return wallet

    def spend_coins(self, user: str, amount: int, reason: str) -> bool:
        wallet = self.get_wallet(user)
        if wallet.balance < amount:
            return False
        wallet.balance -= amount
        wallet.transactions.append(Transaction(amount=-amount, reason=reason))
        wallet.transactions = wallet.transactions[-50:]
        self._cache[user] = wallet
        if self.enabled:
            self.gh.save(user, wallet.to_dict())
        return True