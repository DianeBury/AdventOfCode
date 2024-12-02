def to_int_list(a_string: str, delimiter=" ") -> list:
    return [int(e) for e in a_string.split(delimiter)]


def process_input(input_name: str):
    with open(input_name, "r") as f:
        line = f.readline()
        seeds = [int(e) for e in line.split(" ")[1:]]

        seed_to_soil = []
        line = f.readline() # blank
        line = f.readline() # seed-to-soil map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            seed_to_soil.append(to_int_list(line))

        soil_to_fertilizer = []
        line = f.readline() # soil-to-fertilizer map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            soil_to_fertilizer.append(to_int_list(line))

        fertilizer_to_water = []
        line = f.readline() # fertilizer-to-water map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            fertilizer_to_water.append(to_int_list(line))

        water_to_light = []
        line = f.readline() # water-to-light map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            water_to_light.append(to_int_list(line))

        light_to_temperature = []
        line = f.readline() # light-to-temperature map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            light_to_temperature.append(to_int_list(line))

        temperature_to_humidity = []
        line = f.readline() # temperature-to-humidity map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            temperature_to_humidity.append(to_int_list(line))

        humidity_to_location = []
        line = f.readline() # humidity-to-location map:
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                break
            humidity_to_location.append(to_int_list(line))

    return seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, \
        water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location


def get_destination(x: int, mappings: list):
    for mapping in mappings:
        origin_start = mapping[1]
        destination_start = mapping[0]
        size = mapping[2]
        if origin_start <= x < origin_start + size:
            return destination_start + x - origin_start
    return x


def solve_1(input_name: str) -> int:
    seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, \
        water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = process_input(input_name)

    locations = {}

    for seed in seeds:
        soil = get_destination(seed, seed_to_soil)
        fertilizer = get_destination(soil, soil_to_fertilizer)
        water = get_destination(fertilizer, fertilizer_to_water)
        light = get_destination(water, water_to_light)
        temperature = get_destination(light, light_to_temperature)
        humidity = get_destination(temperature, temperature_to_humidity)
        location = get_destination(humidity, humidity_to_location)
        locations[seed] = location

    return min(locations.values())


def solve_2(input_name: str) -> int:
    seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, \
        water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = process_input(input_name)

    all_locations = []

    for i in range(len(seeds)//2):
        seed_start = seeds[2*i]
        seed_size = seeds[2*i+1]
        def get_mapped_interval(mappings, x_map):
            x_start, x_size = x_map
            for mapping in mappings:
                origin_start = mapping[1]
                destination_start = mapping[0]
                size = mapping[2]
                if origin_start <= x_start < origin_start + size:
                    fx_start = destination_start + x_start - origin_start
                    if origin_start <= x_start + x_size - 1 < origin_start + size:
                        return [[fx_start, x_size]]
                    else:
                        current_size = origin_start + size - 1 - x_start
                        left_size = x_size - current_size
                        return [[fx_start, current_size]] + \
                            get_mapped_interval(mappings, [x_start + current_size + 1, left_size])
            return [x_map]

        soil_mappings = get_mapped_interval(seed_to_soil, [seed_start, seed_size])

        fertilizers_mappings = []
        for mapping in soil_mappings:
            fertilizers_mappings.extend(get_mapped_interval(soil_to_fertilizer, mapping))

        water_mappings = []
        for mapping in fertilizers_mappings:
            water_mappings.extend(get_mapped_interval(fertilizer_to_water, mapping))

        light_mappings = []
        for mapping in water_mappings:
            light_mappings.extend(get_mapped_interval(water_to_light, mapping))

        temperature_mappings = []
        for mapping in light_mappings:
            temperature_mappings.extend(get_mapped_interval(light_to_temperature, mapping))

        humidity_mappings = []
        for mapping in temperature_mappings:
            humidity_mappings.extend(get_mapped_interval(temperature_to_humidity, mapping))

        locations_mappings = []
        for mapping in humidity_mappings:
            locations_mappings.extend(get_mapped_interval(humidity_to_location, mapping))

        all_locations.extend(locations_mappings)

    return min([e[0] for e in all_locations])


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
