"""Modelo Wallet (cartera de monedas)."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Transaction:
    """Una transaccion de monedas."""
    amount: int
    reason: str
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class Wallet:
    """Cartera del usuario."""
    user: str = "anon"
    balance: int = 0
    transactions: List[Transaction] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "user": self.user,
            "balance": self.balance,
            "transactions": [
                {"amount": t.amount, "reason": t.reason, "timestamp": t.timestamp}
                for t in self.transactions
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Wallet":
        txs = [
            Transaction(
                amount=t.get("amount", 0),
                reason=t.get("reason", ""),
                timestamp=t.get("timestamp", ""),
            )
            for t in d.get("transactions", [])
        ]
        return cls(
            user=d.get("user", "anon"),
            balance=int(d.get("balance", 0)),
            transactions=txs,
        )