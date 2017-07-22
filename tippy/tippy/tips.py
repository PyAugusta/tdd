# tippy/tippy/tips.py
class Check(object):
    def __init__(self, amount):
        '''Initialize a Check object, which holds the bill amount'''
        if isinstance(amount, int):
            self._amount = round(float(amount), 2)
        elif isinstance(amount, float):
            self._amount = round(amount, 2)
        else:
            raise TypeError('amount must be either an integer or float')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self.__init__(value)

    def check_to_tip(self, tip_percent):
        '''Returns tuple with the tip amount and total bill after applying the tip'''
        if not isinstance(tip_percent, int) and not isinstance(tip_percent, float):
            raise TypeError('tip percent must be either an integer or float')
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
