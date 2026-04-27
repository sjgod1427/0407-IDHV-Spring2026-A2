import re
import os
from collections import defaultdict
from model import Item, Transaction, User, Day


def parse(filepath: str) -> list[Day]:
    # Two-pass build: first collect raw transactions per day,
    # then group by user to construct the final Day objects.
    day_transactions: dict[int, list[Transaction]] = {}
    day_num_transactions: dict[int, int] = {}
    current_day = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            # Skip blank lines and "---" separator lines
            if not line or line.startswith("---"):
                continue

            # Match day header e.g. "D1(3)" — captures day number and declared transaction count
            day_match = re.match(r'D(\d+)\((\d+)\)', line)
            if day_match:
                current_day = int(day_match.group(1))
                day_transactions[current_day] = []
                day_num_transactions[current_day] = int(day_match.group(2))
                continue

            # Match transaction line e.g. "U5: Q(93.04) C(414.38)"
            trans_match = re.match(r'(U\d+):\s*(.+)', line)
            if trans_match and current_day is not None:
                user_id = trans_match.group(1)
                items_str = trans_match.group(2)

                # Each item is a single capital letter followed by its price in parens
                pairs = re.findall(r'([A-Z])\(([0-9.]+)\)', items_str)
                items = [Item(name=name, price=float(price)) for name, price in pairs]

                transaction = Transaction(
                    user_id=user_id,
                    day=current_day,
                    items=items
                )
                day_transactions[current_day].append(transaction)

    # Sort by day number so the returned list is in chronological order
    days = []
    for day_num, transactions in sorted(day_transactions.items()):
        # A user can have multiple transactions per day; group them so each
        # User object holds all of that user's transactions for the day
        user_trans: dict[str, list[Transaction]] = defaultdict(list)
        for t in transactions:
            user_trans[t.user_id].append(t)

        users = [
            User(name=uid, transactions=trans)
            for uid, trans in user_trans.items()
        ]

        days.append(Day(
            day=day_num,
            transactions=transactions,
            users=users,
            num_transactions=day_num_transactions[day_num]
        ))

    return days


if __name__ == "__main__":
    days = parse(os.path.join(os.path.dirname(__file__), "..", "data", "data.txt"))
    print(f"Total days parsed: {len(days)}")
    for day in days[:30]:  # preview all 30 days
        print(f"\nDay {day.day}: {day.num_transactions} transactions")
        print(f"  Revenue: {day.total_revenue:.2f}")
        print(f"  Most active user: {day.most_active_user}")
        print(f"  Most popular item: {day.most_popular_item}")
