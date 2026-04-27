from pydantic import BaseModel
from typing import List



class Item(BaseModel):
    name:str
    price:float

class Transaction(BaseModel):
    user_id:str
    day:int
    items:List[Item]
    
    @property
    def total_price(self)->float:
        return sum([item.price for item in self.items])

    @property
    def total_items(self)->int:
        return len(self.items)    




class User(BaseModel):
    name:str
    transactions:List[Transaction]

    @property
    def total_spent(self)->float:
        return sum([transaction.total_price for transaction in self.transactions])





class Day(BaseModel):
    day:int
    transactions:List[Transaction]
    users:List[User]
    num_transactions:int

    @property
    def total_revenue(self)->float:
        return sum([transaction.total_price for transaction in self.transactions])

    @property
    def total_items_sold(self)->int:
        return sum([transaction.total_items for transaction in self.transactions])

    @property
    def most_active_user(self)->str:
        user_activity = {}
        for transaction in self.transactions:
            uid = transaction.user_id
            if uid in user_activity:
                user_activity[uid] += 1
            else:
                user_activity[uid] = 1
        most_active = max(user_activity, key=user_activity.get)
        return most_active


    @property
    def most_popular_item(self)->str:
        item_frequency = {}
        for transaction in self.transactions:
            for item in transaction.items:
                if item.name in item_frequency:
                    item_frequency[item.name] += 1
                else:
                    item_frequency[item.name] = 1
        most_popular = max(item_frequency, key=item_frequency.get)
        return most_popular

    @property
    def average_transaction_value(self)->float:
        if self.num_transactions == 0:
            return 0.0
        return self.total_revenue / self.num_transactions

    @property
    def average_items_per_transaction(self)->float:
        if self.num_transactions == 0:
            return 0.0
        return self.total_items_sold / self.num_transactions

    @property
    def user_with_highest_spent(self)->str:
        user_spent = {}
        for transaction in self.transactions:
            uid = transaction.user_id
            if uid in user_spent:
                user_spent[uid] += transaction.total_price
            else:
                user_spent[uid] = transaction.total_price
        highest_spent_user = max(user_spent, key=user_spent.get)
        return highest_spent_user        

