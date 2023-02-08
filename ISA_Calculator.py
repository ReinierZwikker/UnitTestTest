#  --- Constants ---
gravity_sea_level = 9.80665  # m/s2
gas_constant = 287.0  # J/kgK

#  --- Sea level values ---

temperature_sea_level = 288.15  # K
pressure_sea_level = 101325  # Pa
density_sea_level = 1.225  # rho

# Layer LUT
layer_boundaries = [0, 11000, 20000, 32000, 47000, 51000, 71000, 86000]
layer_gradients = [-0.0065, 0, 0.0010, 0.0028, 0, -0.0028, -0.0020]


class HeightError(Exception):
    pass


class MenuError(Exception):
    pass


def temperature_kelvin_to_celsius(temperature_local):
    return temperature_local - 273.15


def temperature_celsius_to_kelvin(temperature_local):
    return temperature_local + 273.15


def ceiling(value, ceiling_value):
    if value <= ceiling_value:
        return value
    if value > ceiling_value:
        return ceiling_value


def calculate_temperature(temperature_start, gradient, height_start, height_end):
    return temperature_start + gradient * (height_end - height_start)


def calculate_new_pressure(pressure_start, temperature_start, temperature_end, gradient, height_start, height_end):
    if gradient != 0:
        return pressure_start * (temperature_end / temperature_start) ** (-gravity_sea_level / (gradient * gas_constant))
    if gradient == 0:
        return pressure_start * 2.71828 ** (-(gravity_sea_level / (gas_constant * temperature_start)) * (height_end - height_start))



def calculate_density(pressure_local, temperature_local):
    return pressure_local / (gas_constant * temperature_local)


def correct_units(input_value, unit):
    input_value = int(input_value)
    unit = int(unit)
    if unit == 1:
        return input_value
    if unit == 2:
        return input_value / 3.281
    if unit == 3:
        return (input_value * 100) / 3.281
    else:
        raise MenuError


def calculate_isa(height_input):
    current_temperature = temperature_sea_level
    current_pressure = pressure_sea_level
    if height_input <= 0 or height_input > 86000:
        raise HeightError
    for layer_i in range(1, len(layer_boundaries)):
        if height_input > layer_boundaries[layer_i - 1]:
            local_height = ceiling(height_input, layer_boundaries[layer_i])
            old_temperature = current_temperature
            current_temperature = calculate_temperature(old_temperature, layer_gradients[layer_i - 1],
                                                        layer_boundaries[layer_i - 1], local_height)
            current_pressure = calculate_new_pressure(current_pressure, old_temperature, current_temperature,
                                                      layer_gradients[layer_i - 1], layer_boundaries[layer_i - 1],
                                                      local_height)

    current_density = calculate_density(current_pressure, current_temperature)

    rounded_pressure = round(current_pressure, 3)
    rounded_temperature = round(current_temperature, 3)
    rounded_density = round(current_density, 5)

    return rounded_pressure, rounded_temperature, rounded_density


def main():
    try:
        print("*** ISA Calculator ***\n")
        print("1. Calculate ISA for altitude in meters\n2. Calculate ISA for altitude in feet\n3. Calculate ISA for "
              "altitude in FL\n")
        unit_choice = int(input("Enter your choice: "))
        if unit_choice <= 0 or unit_choice > 3:
            raise MenuError
        height = int(input("Height: "))
        height = correct_units(height, unit_choice)
        pressure, temperature, density = calculate_isa(height)
        print(" Pressure:", pressure, "\n Temperature: ", temperature, "\n Density: ", density)
    except HeightError:
        print("ERROR: Height is too high or too low")
    except ValueError:
        print("ERROR: You entered a wrong type of value")
    except MenuError:
        print("ERROR: That is not a valid option")


if __name__ == '__main__':
    main()
