def get_variables(file_path):
    variable_set = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            variable = line.strip()
            variable_set.add(variable)

    return list(variable_set)

