_had_error = False


def report_error(line, msg, where=""):
    global _had_error
    print("Error: " + msg + "\n\t on line " + str(line) + "; " + where)
    _had_error = True


def clear_error():
    global _had_error
    _had_error = False


def had_error():
    return _had_error
