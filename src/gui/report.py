import json
import numpy as np


class Report:
    def __init__(self, costs):
        self.report = costs.costs
        self.costs = costs.costs

    def clear_report(self):
        self.report = self.costs

    def save(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.report, outfile, indent=4, ensure_ascii=False)

    def __getitem__(self, key):
        return self.report[key]

    def __setitem__(self, key, value):
        self.report[key] = value


class DroneReport(Report):
    def __init__(self, costs):
        super().__init__(costs)

    def create_report(self, G, edge_path):
        self.clear_report()
        total_dist = 0
        n_edges_visited = len(edge_path)
        street_path = []
        for u, v, k in edge_path:
            try:
                street_name = G[u][v][k]['name']
            except KeyError:
                street_name = "no_name_highway?"
            street_length = G[u][v][k]['length'] / 1000
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

def split_list(lst, n):
    avg = len(lst) // n
    remainder = len(lst) % n
    result = []
    i = 0
    for _ in range(n):
        sublist_size = avg + 1 if remainder > 0 else avg
        result.append(lst[i:i+sublist_size])
        i += sublist_size
        remainder -= 1
    return result

class PlowReport(Report):
    def __init__(self, costs, n=1):
        super().__init__(costs)
        self.n = n

    def create_report(self, G, edge_path, n=1):
        self.clear_report()
        total_dist = 0
        n_edges_visited = len(edge_path)

        vehicles = {}
        for i in range(n):
            v_name = f"vehicle_{i}"
            vehicles[v_name] = {}
            vehicles[v_name]["path"] = []
            vehicles[v_name]["cost"] = 0
            vehicles[v_name]["dist"] = 0
            vehicles[v_name]["hours"] = 0

        sub_paths = split_list(edge_path, n)
        for i in range(n):
            v_name = f"vehicle_{i}"
            for u,v,k in sub_paths[i]:
                try:
                    street_name = G[u][v][k]['name']
                except KeyError:
                    street_name = "no_name_highway?"
                street_length = G[u][v][k]['length'] / 1000
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

        dist_per_v = np.array([vehicles[f"vehicle_{i}"]["dist"] for i in range(n)])
        self.report['distance_per_vehicle_std'] = np.std(dist_per_v)

        self.report['vehicles'] = vehicles
        return self.report
