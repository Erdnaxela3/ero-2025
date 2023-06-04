from cost import VehicleT1Cost, VehicleT2Cost
from report import PlowReport

TIME_COEF = 0.6
MONEY_COEF = 0.4


def create_config(costs, eulerized, path, number_of_vehicules):
    r = PlowReport(costs)
    r.create_report(eulerized, path, number_of_vehicules)
    return r


def opti(time, money, eulerized, path, nbr_vehicules, type="T1"):
    if type == "T1":
        r = create_config(VehicleT1Cost(), eulerized, path, nbr_vehicules)
    elif type == "T2":
        r = create_config(VehicleT2Cost(), eulerized, path, nbr_vehicules)
    else:
        raise ValueError("Invalid Vehicle type. Expected T1 or T2.")

    operation_hours = r.report['operation_duration']
    total_cost = r.report['total_cost']

    indice = (TIME_COEF * (time - operation_hours) +
              MONEY_COEF * (money - total_cost) / money)
    return indice
