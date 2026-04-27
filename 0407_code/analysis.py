from parser import parse
from model import Day
import matplotlib.pyplot as plt
from collections import defaultdict
import itertools
import os


class Analyser:
    def __init__(self):
        self.days = parse(os.path.join(os.path.dirname(__file__), "..", "data", "data.txt"))
        self.plots_dir = os.path.join(os.path.dirname(__file__), "..", "plots")

    def _save_and_show(self, filename: str):
        plt.savefig(os.path.join(self.plots_dir, filename), dpi=150, bbox_inches="tight")
        plt.show()
        plt.close()

    # ─────────────────────────────────────────────
    # USER ANALYSIS
    # ─────────────────────────────────────────────

    # U1: Transaction frequency per user
    def user_transaction_frequency(self) -> dict[str, int]:
        freq = defaultdict(int)
        for day in self.days:
            for u in day.users:
                freq[u.name] += len(u.transactions)
        return dict(freq)

    def plot_user_transaction_frequency(self):
        freq = self.user_transaction_frequency()
        freq = dict(sorted(freq.items()))
        top = max(freq, key=freq.get)
        plt.figure(figsize=(10, 5))
        plt.bar(freq.keys(), freq.values(), color="steelblue")
        plt.xlabel("User ID")
        plt.ylabel("Number of Transactions")
        plt.title(f"U1: {top} is the Most Active User ({freq[top]} Transactions over 30 Days)")
        plt.tight_layout()
        self._save_and_show("U1_user_transaction_frequency.png")

    # U2: Total spend per user
    def user_total_spend(self) -> dict[str, float]:
        spend = defaultdict(float)
        for day in self.days:
            for u in day.users:
                spend[u.name] += u.total_spent
        return dict(spend)

    def plot_user_total_spend(self):
        spend = self.user_total_spend()
        spend = dict(sorted(spend.items()))
        top = max(spend, key=spend.get)
        plt.figure(figsize=(10, 5))
        plt.bar(spend.keys(), spend.values(), color="coral")
        plt.xlabel("User ID")
        plt.ylabel("Total Spend ($)")
        plt.title(f"U2: {top} is the Top Spender (${spend[top]:,.2f} over 30 Days)")
        plt.tight_layout()
        self._save_and_show("U2_user_total_spend.png")

    # U3: Number of active days per user (loyalty)
    def user_active_days(self) -> dict[str, int]:
        # Set per user ensures a day with multiple transactions still counts as one active day
        active = defaultdict(set)
        for day in self.days:
            for u in day.users:
                active[u.name].add(day.day)
        return {uid: len(days) for uid, days in active.items()}

    def plot_user_active_days(self):
        active = self.user_active_days()
        active = dict(sorted(active.items()))
        top = max(active, key=active.get)
        plt.figure(figsize=(10, 5))
        plt.bar(active.keys(), active.values(), color="mediumseagreen")
        plt.xlabel("User ID")
        plt.ylabel("Days Active")
        plt.title(f"U3: {top} is the Most Loyal User (Active on {active[top]}/30 Days)")
        plt.tight_layout()
        self._save_and_show("U3_user_active_days.png")

    # U4: Average spend per transaction per user
    def user_avg_spend_per_transaction(self) -> dict[str, float]:
        total_spend = defaultdict(float)
        total_trans = defaultdict(int)
        for day in self.days:
            for u in day.users:
                total_spend[u.name] += u.total_spent
                total_trans[u.name] += len(u.transactions)
        return {uid: total_spend[uid] / total_trans[uid] for uid in total_spend}

    def plot_user_avg_spend_per_transaction(self):
        avg = self.user_avg_spend_per_transaction()
        avg = dict(sorted(avg.items()))
        top = max(avg, key=avg.get)
        plt.figure(figsize=(10, 5))
        plt.bar(avg.keys(), avg.values(), color="mediumpurple")
        plt.xlabel("User ID")
        plt.ylabel("Avg Spend per Transaction ($)")
        plt.title(f"U4: {top} Spends the Most per Transaction (Avg ${avg[top]:,.2f})")
        plt.tight_layout()
        self._save_and_show("U4_user_avg_spend_per_transaction.png")

    # U5: Average basket size (items per transaction) per user
    def user_avg_basket_size(self) -> dict[str, float]:
        total_items = defaultdict(int)
        total_trans = defaultdict(int)
        for day in self.days:
            for u in day.users:
                for t in u.transactions:
                    total_items[u.name] += t.total_items
                total_trans[u.name] += len(u.transactions)
        return {uid: total_items[uid] / total_trans[uid] for uid in total_items}

    def plot_user_avg_basket_size(self):
        avg = self.user_avg_basket_size()
        avg = dict(sorted(avg.items()))
        top = max(avg, key=avg.get)
        plt.figure(figsize=(10, 5))
        plt.bar(avg.keys(), avg.values(), color="darkorange")
        plt.xlabel("User ID")
        plt.ylabel("Avg Items per Transaction")
        plt.title(f"U5: {top} Buys the Most Items per Transaction (Avg {avg[top]:.1f} Items)")
        plt.tight_layout()
        self._save_and_show("U5_user_avg_basket_size.png")

    # U6: User co-occurrence (users who appear on the same day)
    def user_cooccurrence(self) -> dict[tuple, int]:
        cooc = defaultdict(int)
        for day in self.days:
            # Unique user IDs for the day — a user with multiple transactions still counts once
            users_today = set(t.user_id for t in day.transactions)
            # Sort before combining so (U3, U7) and (U7, U3) always map to the same key
            for pair in itertools.combinations(sorted(users_today), 2):
                cooc[pair] += 1
        return dict(sorted(cooc.items(), key=lambda x: -x[1]))

    def plot_user_cooccurrence(self):
        cooc = self.user_cooccurrence()
        top15 = list(cooc.items())[:15]
        pairs = [f"{a}-{b}" for (a, b), _ in top15]
        counts = [c for _, c in top15]
        top_pair = f"{top15[0][0][0]}-{top15[0][0][1]}"
        plt.figure(figsize=(14, 5))
        plt.bar(pairs, counts, color="steelblue")
        plt.xlabel("User Pair")
        plt.ylabel("Days Appeared Together")
        plt.title(f"U6: '{top_pair}' Appear Together Most Often ({top15[0][1]} Days)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self._save_and_show("U6_user_cooccurrence.png")

    # ─────────────────────────────────────────────
    # ITEM ANALYSIS
    # ─────────────────────────────────────────────

    # I1: Item purchase frequency
    def item_frequency(self) -> dict[str, int]:
        freq = defaultdict(int)
        for day in self.days:
            for u in day.users:
                for t in u.transactions:
                    for item in t.items:
                        freq[item.name] += 1
        return dict(sorted(freq.items()))

    def plot_item_frequency(self):
        freq = self.item_frequency()
        top = max(freq, key=freq.get)
        plt.figure(figsize=(12, 5))
        plt.bar(freq.keys(), freq.values(), color="steelblue")
        plt.xlabel("Item")
        plt.ylabel("Times Purchased")
        plt.title(f"I1: Item '{top}' is the Most Purchased ({freq[top]} Times over 30 Days)")
        plt.tight_layout()
        self._save_and_show("I1_item_frequency.png")

    # I2: Item revenue contribution
    def item_revenue(self) -> dict[str, float]:
        revenue = defaultdict(float)
        for day in self.days:
            for u in day.users:
                for t in u.transactions:
                    for item in t.items:
                        revenue[item.name] += item.price
        return dict(sorted(revenue.items()))

    def plot_item_revenue(self):
        revenue = self.item_revenue()
        top = max(revenue, key=revenue.get)
        plt.figure(figsize=(12, 5))
        plt.bar(revenue.keys(), revenue.values(), color="coral")
        plt.xlabel("Item")
        plt.ylabel("Total Revenue ($)")
        plt.title(f"I2: Item '{top}' Generates the Most Revenue (${revenue[top]:,.2f} over 30 Days)")
        plt.tight_layout()
        self._save_and_show("I2_item_revenue.png")

    # I3: Item co-occurrence (bought together)
    def item_cooccurrence(self) -> dict[tuple, int]:
        cooc = defaultdict(int)
        for day in self.days:
            for u in day.users:
                for t in u.transactions:
                    # Sort names so (K, V) and (V, K) always produce the same tuple key
                    names = sorted([item.name for item in t.items])
                    for pair in itertools.combinations(names, 2):
                        cooc[pair] += 1
        return dict(sorted(cooc.items(), key=lambda x: -x[1]))

    def plot_item_cooccurrence(self):
        cooc = self.item_cooccurrence()
        top20 = list(cooc.items())[:20]
        pairs = [f"{a}-{b}" for (a, b), _ in top20]
        counts = [c for _, c in top20]
        top_pair = f"{top20[0][0][0]}-{top20[0][0][1]}"
        plt.figure(figsize=(14, 5))
        plt.bar(pairs, counts, color="mediumseagreen")
        plt.xlabel("Item Pair")
        plt.ylabel("Times Bought Together")
        plt.title(f"I3: '{top_pair}' is the Most Frequently Co-purchased Pair ({top20[0][1]} Times)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self._save_and_show("I3_item_cooccurrence.png")

    # I4: Top 6 items by number of days they were purchased
    def daily_staple_items(self) -> dict[str, int]:
        # Set per item ensures multiple purchases on the same day count as one day
        item_days = defaultdict(set)
        for day in self.days:
            for t in day.transactions:
                for item in t.items:
                    item_days[item.name].add(day.day)
        top6 = sorted(item_days.items(), key=lambda x: -len(x[1]))[:6]
        return {item: len(days) for item, days in top6}

    def plot_daily_staple_items(self):
        staples = self.daily_staple_items()
        top = next(iter(staples))
        plt.figure(figsize=(10, 5))
        plt.bar(staples.keys(), staples.values(), color="mediumseagreen")
        plt.xlabel("Item")
        plt.ylabel("Number of Days Purchased")
        plt.ylim(0, 32)
        for item, days in staples.items():
            plt.text(item, days + 0.3, str(days), ha="center", fontsize=10)
        plt.title(f"I4: '{top}' is the Most Consistent Item — Top 6 Items by Days Present")
        plt.tight_layout()
        self._save_and_show("I4_daily_staple_items.png")

    # I5: Average transaction value when each item is present
    def item_avg_transaction_value(self) -> dict[str, float]:
        # Measures basket value when the item is present, not the item's own price
        total = defaultdict(float)
        count = defaultdict(int)
        for day in self.days:
            for u in day.users:
                for t in u.transactions:
                    for item in t.items:
                        total[item.name] += t.total_price
                        count[item.name] += 1
        return dict(sorted({i: total[i] / count[i] for i in total}.items()))

    def plot_item_avg_transaction_value(self):
        avg = self.item_avg_transaction_value()
        top = max(avg, key=avg.get)
        plt.figure(figsize=(12, 5))
        plt.bar(avg.keys(), avg.values(), color="mediumpurple")
        plt.xlabel("Item")
        plt.ylabel("Avg Transaction Value ($)")
        plt.title(f"I5: Baskets with Item '{top}' Have the Highest Avg Value (${avg[top]:,.2f})")
        plt.tight_layout()
        self._save_and_show("I5_item_avg_transaction_value.png")

    # ─────────────────────────────────────────────
    # TRANSACTION ANALYSIS
    # ─────────────────────────────────────────────

    # T1: Number of transactions per day
    def transactions_per_day(self) -> dict[int, int]:
        return {day.day: day.num_transactions for day in self.days}

    def plot_transactions_per_day(self):
        tpd = self.transactions_per_day()
        peak = max(tpd, key=tpd.get)
        plt.figure(figsize=(12, 5))
        plt.bar(tpd.keys(), tpd.values(), color="steelblue")
        plt.xlabel("Day")
        plt.ylabel("Number of Transactions")
        plt.title(f"T1: Day {peak} is the Busiest Day ({tpd[peak]} Transactions)")
        plt.tight_layout()
        self._save_and_show("T1_transactions_per_day.png")

    # T2: Distribution of transaction values
    def transaction_values(self) -> list[float]:
        return [t.total_price for day in self.days for t in day.transactions]

    def plot_transaction_value_distribution(self):
        values = self.transaction_values()
        avg = sum(values) / len(values)
        plt.figure(figsize=(10, 5))
        plt.hist(values, bins=20, color="coral", edgecolor="black")
        plt.xlabel("Transaction Value ($)")
        plt.ylabel("Frequency")
        plt.title(f"T2: Most Transactions Cluster Around ${avg:,.2f} (Avg Transaction Value)")
        plt.tight_layout()
        self._save_and_show("T2_transaction_value_distribution.png")

    # T3: Average basket size per day
    def avg_basket_size_per_day(self) -> dict[int, float]:
        return {day.day: day.average_items_per_transaction for day in self.days}

    def plot_avg_basket_size_per_day(self):
        avg = self.avg_basket_size_per_day()
        peak = max(avg, key=avg.get)
        plt.figure(figsize=(12, 5))
        plt.plot(avg.keys(), avg.values(), marker="o", color="mediumseagreen")
        plt.xlabel("Day")
        plt.ylabel("Avg Items per Transaction")
        plt.title(f"T3: Day {peak} Has the Largest Avg Basket ({avg[peak]:.1f} Items per Transaction)")
        plt.tight_layout()
        self._save_and_show("T3_avg_basket_size_per_day.png")

    # T4: Daily revenue trend
    def daily_revenue(self) -> dict[int, float]:
        return {day.day: day.total_revenue for day in self.days}

    def plot_daily_revenue(self):
        revenue = self.daily_revenue()
        peak = max(revenue, key=revenue.get)
        plt.figure(figsize=(12, 5))
        plt.plot(revenue.keys(), revenue.values(), marker="o", color="darkorange")
        plt.xlabel("Day")
        plt.ylabel("Total Revenue ($)")
        plt.title(f"T4: Day {peak} Had the Highest Revenue (${revenue[peak]:,.2f}) over 30 Days")
        plt.tight_layout()
        self._save_and_show("T4_daily_revenue.png")

    # T5: Transaction value spread per day
    def transaction_values_per_day(self) -> dict[int, list[float]]:
        return {day.day: [t.total_price for t in day.transactions] for day in self.days}

    def plot_transaction_values_boxplot(self):
        data = self.transaction_values_per_day()
        days = list(data.keys())
        values = list(data.values())
        overall_max = max(v for day_vals in values for v in day_vals)
        plt.figure(figsize=(18, 6))
        plt.boxplot(values, labels=days)
        plt.xlabel("Day")
        plt.ylabel("Transaction Value ($)")
        plt.title(f"T5: Transaction Value Spread per Day — Max Single Transaction: ${overall_max:,.2f}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self._save_and_show("T5_transaction_values_boxplot.png")


if __name__ == "__main__":
    a = Analyser()

    print("=== USER ANALYSIS ===")
    a.plot_user_transaction_frequency()
    a.plot_user_total_spend()
    a.plot_user_active_days()
    a.plot_user_avg_spend_per_transaction()
    a.plot_user_avg_basket_size()
    a.plot_user_cooccurrence()

    print("=== ITEM ANALYSIS ===")
    a.plot_item_frequency()
    a.plot_item_revenue()
    a.plot_item_cooccurrence()
    a.plot_daily_staple_items()
    a.plot_item_avg_transaction_value()

    print("=== TRANSACTION ANALYSIS ===")
    a.plot_transactions_per_day()
    a.plot_transaction_value_distribution()
    a.plot_avg_basket_size_per_day()
    a.plot_daily_revenue()
    a.plot_transaction_values_boxplot()
