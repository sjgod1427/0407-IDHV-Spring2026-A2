S20230030407 - Assignment 2
Introduction to Data and Human Values (IDHV)
=============================================

HOW TO RUN
----------

1. Install dependencies:
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install pydantic matplotlib

2. Ensure the project structure is intact (data/data.txt and plots/ must exist).

3. Run the analysis from inside the 0407_code/ folder:
   cd 0407_code
   python3 analysis.py

   This generates all 16 plots and saves them to the plots/ folder.


PROJECT STRUCTURE
-----------------

data/
  data.txt      Raw transaction data (30 days)
0407_code/
  model.py      Pydantic data models (Item, Transaction, User, Day)
  parser.py     Parses data.txt into model objects
  analysis.py   All 16 analysis tasks and visualizations
plots/          Output folder for saved chart images





NON-TRIVIAL TASKS AND FUNCTIONS USED
-------------------------------------

USER ANALYSIS (6 Tasks)
------------------------

U1 - Number of Transactions per User
    Function: user_transaction_frequency()

     In this function, we loop through each day and access day.users,
     which is a list containing User objects logged for that day. 
     The User object has information only about the transactions carried out by that user on that day. 
     We use the len(u.transactions) property, which is created in the User model to find the number of
     transactions made by each user on each day and then sum up these values using a defaultdict over 30 days.
     This will give us the total number of transactions made by each user over the 30-day period.

     Visualization: plot_user_transaction_frequency()
     A bar graph is produced with users on the x-axis and the number of transactions on the y-axis.

U2 - Total Amount Spent per User
    Function: user_total_spend()

    Here, we loop through day.users and access the u.total_spent property,
    which sums the total_price attribute of all transactions carried out by each user on that day.
    Then we add up the u.total_spent value over all 30 days to get each user’s total expenditure.

    Visualization: plot_user_total_spend()
    A bar graph shows the total amount spent by each user.

U3 - User Loyalty (Number of Active Days)
    Function: user_active_days()

    This function loops through each day's users and adds the corresponding day 
    in a set corresponding to that user. Since sets cannot have duplicate values, 
    if a user carries out multiple transactions on the same day, this is counted as only one day. 
    Thus, the cardinality of each user's set gives the number of unique days the user has been active.

    Visualization: plot_user_active_days()
    A bar graph displaying the number of active days per user.

U4 - Average Amount Spent per Transaction per User
    Function: user_avg_spend_per_transaction()

    This function has two running totals per user: total spend and total number of transactions carried out.
    These are obtained from the u.total_spent and len(u.transactions) attributes, respectively, in the User model, summed over 30 days.
    At the end of the loop, we calculate the average amount spent per transaction by dividing the total spend by the total number of transactions.

    Visualization: plot_user_avg_spend_per_transaction()
    A bar graph displaying the average spend per transaction per user.


U5 - Average Basket Size per User
     Function: user_avg_basket_size()

     The function goes through each user on each day and then goes through each transaction in u.transactions
     and finds the value of t.total_items for each transaction. The total_items field in the transaction class represents 
     the number of items in the transaction. The function calculates the average number of items obtained per visit for each 
     user by finding the sum of all transactions and dividing them by the total number of transactions.

     Visualization: plot_user_avg_basket_size()
     Displays the average number of items per transaction for each user using a bar graph.


U6 - User Co-occurrence (Users Active on the Same Day)
     Function: user_cooccurrence()

     For each day, we extract the set of unique user IDs from day.transactions.
     We then use itertools.combinations() on the sorted set to generate all possible
     pairs of users who were active on that day. The set is sorted before pairing so
     each pair always has a consistent key order, ensuring (U3, U7) and (U7, U3)
     are never counted as separate pairs. A defaultdict counts
     how many days each pair appeared together over the 30-day period. This is important to check
     as to see how many couples or people from same area come together.

     Visualization: plot_user_cooccurrence()
     A bar chart showing the top 15 user pairs ranked by the number of days they
     appeared together.


ITEM ANALYSIS (5 TASKS)
---------------------

I1 - Number of Times Items Are Purchased
     Function: item_frequency()

     The first operation here iterates over day.users,
     followed by the iteration over the transactions of each user,
     and the last iteration over the items contained in the current transaction, 
     incrementing the count of the appropriate item via its name, item.name.
     A defaultdict is used so that all item counts start off at zero. 
     The measure shows how many times each item was purchased throughout all 260 transactions.

     Visualization: plot_item_frequency()
     It produces a bar chart with items plotted against their purchase frequency.

I2 - Total Revenue Earned from Items
     Function: item_revenue()

     It works exactly as I1, with the only difference that in addition to just counting the occurrences, 
     we also sum the item's price for each occurrence. As the prices of the items remain constant, 
     we can compute the overall revenue earned per each item over 30 days.

     Visualization: plot_item_revenue()
     A bar chart displaying revenue earned from each item.

I3 - Co-occurrence (When Purchased Together)
     Function: item_cooccurrence()

     For each transaction, we consider each of the items in t.items and produce all possible pairs using the itertools.combinations() function. 
     All pairs are alphabetically sorted, so that e.g., (K, V) is considered to be the same pair as (V, K). We sum the frequency of each pair among all transactions.

     Visualization: plot_item_cooccurrence()
     A bar chart showing the top 20 pairs of items purchased together.

I4 - Day Coverage (Consistency of Buying Items)
     Function: daily_staple_items()

     Here we keep track of days each item is purchased on. 
     To do this, we maintain a per-item set. Then we iterate over day.transactions and day.day to record the day numbers of the days when each item occurs. 
     After iterating, we rank the items based on their day set cardinality and select the top six items.

     Visualization: plot_daily_staple_items()
     It produces a bar chart that visualizes the six most frequent items by the number of days on which they appeared,
     with the corresponding numbers displayed above each bar.

I5 - Average Basket Price with Item
     Function: item_avg_transaction_value()

     In this task we record t.total_price for all the transactions that contain a certain item and then divide it by the number of such transactions. 
     This measure does not reflect the actual price of the item but the value of the whole basket when the item occurs in it.

     Visualization: plot_item_avg_transaction_value()
     A bar chart of average basket value, grouped by item.


TRANSACTION ANALYSIS (5 Tasks)
---------------------------------

  T1 – Transactions per day
       Function: transactions_per_day()

       The function applies a dictionary comprehension where key is the day and
       value is its number of transactions, day.num_transactions. Since the day
       model already stores this count (parsed from the data file header),
       there is no additional loop required.

       Visualization: plot_transactions_per_day()
       Plots a bar graph with days as x axis and number of transactions as y axis.


  T2 – Transactions' values distribution
       Function: transaction_values()

       This function returns an array containing 260 values of t.total_price for all
       transactions across all 30 days. It uses a two-level list comprehension over
       self.days and day.transactions to collect every transaction value directly
       from the Day object, without going through day.users.

       Visualization: plot_transaction_value_distribution()
       Plots histogram showing how transaction values are distributed among bins


  T3 – Average basket size per day
       Function: avg_basket_size_per_day()

       The function returns a dict where each key is the number of the day and
       its value corresponds to the day.average_items_per_transaction that has
       been defined as a property in the Day model, being calculated by dividing
       the number of total_items with the number of transactions.

       Visualization: plot_avg_basket_size_per_day()
       Creates a line graph showing average basket sizes for 30 days


  T4 – Trendline for total daily revenue
       Function: daily_revenue()

       The function uses the day.total_revenue property defined in the Day class
       to calculate total_revenue per day which is simply the sum of all transaction
       values. The function returns day.total_revenue values for all days from 1 to 30.

       Visualization: plot_daily_revenue()
       Shows total revenue per day by creating a line graph for 30 days.


  T5 – Spread of transactions' values per day (box plots)
       Function: transaction_values_per_day()

       The function returns an array of values where each element of the array is
       a list of values corresponding to the values of transactions per each day.
       In other words, each transaction's total price is being extracted from every
       day. As a result, 30 sets of transaction values will be created. 

       Visualization: plot_transaction_values_boxplot()
       Draws a box plot with one box per day across all 30 days.


OUTPUT
------

All plots are saved as PNG files in the plots/ folder with names
matching the task codes (e.g., U1_user_transaction_frequency.png).
