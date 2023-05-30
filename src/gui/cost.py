class Cost:
    def __init__(self):
        self.costs = dict()

    def __str__(self):
        return '\n'.join(f"{key}: {value}" for key, value in self.costs.items())

    def __getitem__(self, key):
        return self.costs[key]

    def __setitem__(self, key, value):
        self.costs[key] = value


class DroneCost(Cost):
    def __init__(self, fix_cost, km_cost):
        super().__init__()
        self.costs['fix_cost'] = fix_cost
        self.costs['km_cost'] = km_cost


class PlowCost(Cost):
    def __init__(self, fix_cost, km_cost, h_cost,
                 overtime_h_cost, overtime_h_lim, speed):
        super().__init__()
        self.costs['fix_cost'] = fix_cost
        self.costs['km_cost'] = km_cost
        self.costs['h_cost'] = h_cost
        self.costs['overtime_h_cost'] = overtime_h_cost
        self.costs['overtime_h_lim'] = overtime_h_lim
        self.costs['speed'] = speed
