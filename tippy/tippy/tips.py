# tippy/tippy/tips.py
class Check(object):
    def __init__(self, amount):
        '''Initialize a Check object, which holds the bill amount'''
        self.amount = amount

    def check_to_tip(self, tip_percent):
        '''Returns tuple with the tip amount and total bill after applying the tip'''
        tip = round(self.amount * tip_percent / 100, 2)
        total = self.amount + tip
        return tip, total

    def check_to_rtip(self, tip_percent):
        '''Returns tuple with the tip amount and total bill after adjusting the tip to
        ensure the total bill is a whole dollar amount'''
        tip, total = self.check_to_tip(tip_percent)
        f_total = int(total)
        if total == f_total:
            return tip, total
        n_total = float(f_total + 1)
        n_tip = round(tip + n_total - total, 2)
        return n_tip, n_total
