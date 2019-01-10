
def verify_int_input(var):
    if not isintance(var, int):
        raise ValueError("Input maximum results returned variable must be of type int")
    if var < 1 or var > 100:
        return 10
    else:
        return var

