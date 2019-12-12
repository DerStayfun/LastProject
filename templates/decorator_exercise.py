

def restrict_access(func):
    def wrapper(*args, **kwargs):
        name = args[0]
        if name.startswith("S"):
            result = "Access Denied"
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper

@restrict_access
def treasurebox(username):
    return f"Granted Access to {username}"

@restrict_access
def bank_safe(username):
    return f"Granted Access to rich bank safe to {username}"

if __name__ == '__main__':
    print(treasurebox("Stefan"))
    print(bank_safe("Paul"))