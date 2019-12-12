import random

# Create a decorator called: chaosmachine
# it replaces all passed values with a random number between 1 and 100
# and then calls the original function

def chaosmachine(func):
    def wrapper(*args, **kwargs):
        return func(random.randint(0,100))
    return wrapper

@chaosmachine
def double_value(my_number):
    return my_number*2


if __name__ == '__main__':
    print(double_value(2))