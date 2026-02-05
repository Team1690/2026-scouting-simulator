def calculate_error(observed: float, actual: float):
    if actual == 0:
        return 0 if observed == 0 else observed * 100
    return 100 * (observed - actual) / actual
