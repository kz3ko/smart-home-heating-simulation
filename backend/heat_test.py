from time import sleep

# Maksymalna moc grzewcza grzejnia to 1500

heater_power = 1709

def count_thermal_conductivity(lambda_d: float, s: float, delta_t: float, t: int) -> float:
    return lambda_d * s * delta_t * t


def count_temperature_difference(q: float, lambda_d: float, s: float, t: int) -> float:
    return q / (s * t * lambda_d)


def count_specific_heat(delta_q: float, delta_t: float, m: float = 1) -> float:
    return delta_q / (m * delta_t)


d = 0.3  # [m]
lambda_ = 0.8
lambda_d_ = lambda_ / d

h = 190 * 1.5 / 100  # [m]
w = 120 * 1.5 / 100  # [m]
s_ = h * w
print(f'Powierzchnia pomieszczenia: {s_}')

t_source = 21.6
t_target = 12
delta_t_ = t_source - t_target

t_ = 60  # [s] -> 1 minute

while not t_source - 0.25 <= t_target <= t_source + 0.25:
    print(f'Temperature źródła: {t_source} Temperatura celu: {t_target}')
    thermal_conductivity = round(count_thermal_conductivity(lambda_d_, s_, delta_t_, t_), 2)
    print(f'Przewodność cieplna: {thermal_conductivity}')
    to_heat = thermal_conductivity if thermal_conductivity < heater_power else heater_power
    t_target += count_temperature_difference(to_heat, lambda_d_, s_, t_)
    delta_t_ = t_source - t_target
    sleep(1)
