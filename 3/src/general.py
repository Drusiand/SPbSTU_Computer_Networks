from collections import Counter


class General:
    def __init__(self, _id, is_traitor=False):
        self.id = _id
        self.other_generals = []
        self.orders = []
        self.is_traitor = is_traitor

    def __call__(self, m, order):
        self.om_algorithm(commander=self,
                          m=m,
                          order=order,
                          )

    @staticmethod
    def next_order(is_traitor, order, i):
        if is_traitor:
            if i % 2 == 0:
                return "ATTACK" if order == "RETREAT" else "RETREAT"
        return order

    def om_algorithm(self, commander, m, order):
        if m < 0:
            self.orders.append(order)
        elif m == 0:
            for i, l in enumerate(self.other_generals):
                l.om_algorithm(
                    commander=self,
                    m=(m - 1),
                    order=self.next_order(self.is_traitor, order, i)
                )
        else:
            for i, l in enumerate(self.other_generals):
                if l is not self and l is not commander:
                    l.om_algorithm(
                        commander=self,
                        m=(m - 1),
                        order=self.next_order(self.is_traitor, order, i)
                    )

    @property
    def decision(self):
        c = Counter(self.orders)
        return c.most_common()
