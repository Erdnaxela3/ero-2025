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
            vehicles[v_name] = {
                "path": [],
                "cost": 0,
                "dist": 0,
                "hours": 0
            }

        sub_paths = split_list(edge_path, n)
        for i in range(n):
            v_name = f"vehicle_{i}"
            for u, v, k in sub_paths[i]:
                try:
                    street_name = G[u][v][k]['name']
                except KeyError:
                    street_name = "no_name_highway?"
                street_length = G[u][v][k]['length'] / 1000
                vehicles[v_name]["path"].append(street_name)
                vehicles[v_name]["dist"] += street_length
                total_dist += street_length

        ot_lim = self.costs['overtime_h_lim']
        for i in range(n):
            v_name = f"vehicle_{i}"
            dist = vehicles[v_name]["dist"]
            hour = dist / self.costs['speed']
            ot_time = max(0, hour - ot_lim)
            ok_time = min(ot_lim, hour)
            ok_cost = ok_time * self.costs['h_cost']
            ot_cost = ot_time * self.costs['overtime_h_cost']
            h_cost = ok_cost + ot_cost
            km_cost = self.costs['km_cost'] * dist
            fix_cost = self.costs['fix_cost']
            total = fix_cost + h_cost + km_cost
            vehicles[v_name]["hours"] = ok_time + ot_time
            vehicles[v_name]["not_overtime_h"] = ok_time
            vehicles[v_name]["overtime_h"] = ot_time
            vehicles[v_name]["fix_cost"] = fix_cost
            vehicles[v_name]["km_cost"] = km_cost
            vehicles[v_name]["not_overtime_cost"] = ok_cost
            vehicles[v_name]["overtime_cost"] = ot_cost
            vehicles[v_name]["h_cost"] = h_cost
            vehicles[v_name]["cost"] = total

        ok_hour = sum(
            [vehicles[f"vehicle_{i}"]["not_overtime_h"] for i in range(n)])
        ok_cost = sum(
            [vehicles[f"vehicle_{i}"]["not_overtime_cost"] for i in range(n)])
        ot_hour = sum(
            [vehicles[f"vehicle_{i}"]["overtime_h"] for i in range(n)])
        ot_cost = sum(
            [vehicles[f"vehicle_{i}"]["overtime_cost"] for i in range(n)])

        self.report['cumul_fixed_cost'] = self.costs["fix_cost"] * n
        self.report['cumul_hours'] = total_dist / self.costs['speed']
        self.report['cumul_not_overtime_h'] = ok_hour
        self.report['cumul_overtime_h'] = ot_hour
        self.report['cumul_hour_cost'] = ok_hour + ot_hour
        self.report['cumul_not_overtime_cost'] = ok_cost
        self.report['cumul_overtime_cost'] = ot_cost
        self.report['cumul_km_cost'] = self.costs['km_cost'] * total_dist
        self.report['total_cost'] = self.report['cumul_fixed_cost'] + \
            self.report['cumul_hour_cost'] + self.report['cumul_km_cost']
        self.report['total_distance'] = total_dist
        self.report['n_visited_street'] = n_edges_visited
        self.report['avg_edge_length'] = total_dist / n_edges_visited

        dist_per_v = np.array(
            [vehicles[f"vehicle_{i}"]["dist"] for i in range(n)])
        hour_per_v = np.array(
            [vehicles[f"vehicle_{i}"]["hours"] for i in range(n)])

        self.report['distance_per_vehicle_std'] = np.std(dist_per_v)
        self.report['operation_duration'] = float(max(hour_per_v))

        self.report['vehicles'] = vehicles
        return self.report
