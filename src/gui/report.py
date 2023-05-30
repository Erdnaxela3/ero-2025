import json


class Report:
    def __init__(self, costs):
        self.report = costs.costs
        self.costs = costs.costs

    def clear_report(self):
        self.report = self.costs

    def save(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.report, outfile, indent=4)

    def __getitem__(self, key):
        return self.report[key]

    def __setitem__(self, key, value):
        self.report[key] = value


class DroneReport(Report):
    def __init__(self, costs):
        super().__init__(costs)

    def create_report(self, G, node_path):
        self.clear_report()
        total_dist = 0
        n_edges_visited = len(node_path) - 1
        street_path = []
        for i in range(n_edges_visited):
            u, v = node_path[i], node_path[i+1]
            try:
                street_name = G[u][v][0]['name']
            except KeyError:
                street_name = "no_name_highway?"
            street_length = G[u][v][0]['length'] / 1000
            street_path.append(street_name)
            total_dist += street_length
        self.report['cumul_fix_cost'] = self.costs["fix_cost"]
        self.report['cumul_flight_cost'] = self.costs['km_cost'] * total_dist
        self.report['total_cost'] = self.report['cumul_fix_cost'] + \
            self.report['cumul_flight_cost']
        self.report['total_distance'] = total_dist
        self.report['n_visited_street'] = n_edges_visited
        self.report['avg_edge_length'] = total_dist / n_edges_visited
        self.report['path'] = street_path
        return self.report


class PlowReport(Report):
    def __init__(self, costs, n=1):
        super().__init__(costs)
        self.n = n

    def create_report(self, G, node_path, n=1):
        self.clear_report()
        total_dist = 0
        n_edges_visited = len(node_path) - 1
        step = round(n_edges_visited / min(n, n_edges_visited))

        vehicles = {}
        for i in range(n):
            v_name = f"vehicle_{i}"
            vehicles[v_name] = {}
            vehicles[v_name]["path"] = []
            vehicles[v_name]["cost"] = 0
            vehicles[v_name]["dist"] = 0
            vehicles[v_name]["hours"] = 0

        for turn in range(step):
            for i in range(turn, n_edges_visited, step):
                v_name = f"vehicle_{(i - turn) % n}"
                print(v_name, i, turn, n, (i - turn) % n)
                u, v = node_path[i], node_path[i+1]
                try:
                    street_name = G[u][v][0]['name']
                except KeyError:
                    street_name = "no_name_highway?"
                street_length = G[u][v][0]['length'] / 1000
                vehicles[v_name]["path"].append(street_name)
                vehicles[v_name]["dist"] += street_length
                total_dist += street_length

        cumul_cost_h = 0
        for i in range(n):
            v_name = f"vehicle_{i}"
            dist = vehicles[v_name]["dist"]
            hour = dist / self.costs['speed']
            ot_lim = self.costs['overtime_h_lim']
            h_cost = min(ot_lim, hour) * self.costs['h_cost'] + max(
                0, hour - ot_lim) * self.costs['overtime_h_cost']
            km_cost = self.costs['km_cost'] * dist
            total = self.costs['fix_cost'] + h_cost + km_cost
            vehicles[v_name]["cost"] = total
            vehicles[v_name]["hours"] = hour
            cumul_cost_h += h_cost

        self.report['cumul_fixed_cost'] = self.costs["fix_cost"] * n
        self.report['cumul_hours'] = total_dist / self.costs['speed']
        self.report['cumul_hour_cost'] = cumul_cost_h
        self.report['cumul_km_cost'] = self.costs['km_cost'] * total_dist
        self.report['total_cost'] = self.report['cumul_fixed_cost'] + \
            self.report['cumul_hour_cost'] + self.report['cumul_km_cost']
        self.report['total_distance'] = total_dist
        self.report['n_visited_street'] = n_edges_visited
        self.report['avg_edge_length'] = total_dist / n_edges_visited

        self.report['vehicles'] = vehicles
        return self.report
