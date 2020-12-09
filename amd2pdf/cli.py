def check_param(short, long, param):
    def f(idx, args, params):
        arg = args[idx]
        if arg.lower() in (short, long):
            try:
                value = args[idx + 1]
                params[param] = value
                return True, True
            except:
                raise Exception("%s/%s requires a value."%(short, long))
        return False, None
    return f


def check_bool_param(short, long, param):
    def f(idx, args, params):
        arg = args[idx]
        if arg in (short, long):
            params[param] = True
            return True, False
        return False, None
    return f
