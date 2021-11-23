from datetime import datetime

class Account:
    """The Account class stores, adds, spends, and display balances for a user's transactions.
    """

    def __init__(self):
        """Inits Account with a sample set of transactions."""
        self.accounts = [
                            { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" },
                            { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
                            { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
                            { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
                            { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
                        ]


    def add_transaction(self, payer, points):
        """Adds a transaction to the self.accounts.

        Add a transaction into the memory formated as a dictionary.

        Args:
            payer(str): The name of the payer for a given transaction. 
            points(int): The amount of points added or spent by the payer.

        Returns:
            None
        """

        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        self.accounts.append({'payer': payer.upper(), 'points': int(points), 'timestamp': date})
        
        
    def _sort_transactions(self):
        """Sorts the transactions from the oldest points to be spent first based on the oldest transaction timestamp.

        Args: -

        Returns:
            Sorted list of transactions.
        """
        # the list of transactions are being sorted by the timestamp key. 
        # here the key prameter used with lambda can be used to sort on this value.
        # lastly, when the reverse is false the data is sorted in ascending order
        return sorted(self.accounts, key = lambda x : datetime.strptime(x['timestamp'], "%Y-%m-%dT%H:%M:%SZ"), reverse=False)
        
            
    def spend_points(self, points):
        """Spends payer points and adds withdrawall transactions to the account.

        Before points are spent we check if the balance is able to cover the points requested to be spent.

        Args:
            points(int): The amount of points added or spent by the payer.

        Returns:
            List of spend transactions.
        """

        assert points >= 0, 'Points must be a positive value.'

        available_balance = 0

        for pyr, pts in self.balance().items():
            available_balance += pts

        assert points <= available_balance, f"User attempting to spend more than total payer available balance. user only has {available_balance} points remaining. user requested to spend {points} points. Unable to process"    

        deducted_payer_points = {}
        
        for transaction in self._sort_transactions():

            if 0 == points:
                break

            payer_name = transaction['payer']
            payer_points = transaction['points']
            
            # checking/adding payer and points
            if payer_name not in deducted_payer_points:
                deducted_payer_points[payer_name] = 0

            
            if points > payer_points:
                # updating payer balance 
                deducted_payer_points[payer_name] -= payer_points
                # update the point balance
                points -= payer_points

            else:
                deducted_payer_points[payer_name] -= points
                points -= points 

        result = []

        for pyr, pts in deducted_payer_points.items():
            self.add_transaction(pyr, pts)
            result.append({"payer":pyr, "points":pts})

        return result


    def balance(self):
        """Displays the account balance.

        Args: -

        Returns:
            Dictionary of balance points after the spend
        """

        balance = {}
        
        for transaction in self._sort_transactions():

            payer_name = transaction['payer']
            payer_points = transaction['points']

            # checking/adding payer and points
            if payer_name not in balance:
                balance[payer_name] = payer_points
            else:
                balance[payer_name] += payer_points
        
        return balance