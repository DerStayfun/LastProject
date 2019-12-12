import time
import random

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("'{}' was running for: {} seconds".format(func.__name__, time.time() - start))
        return result
    return wrapper


@timeit
def time_waster(wait_seconds):
    time.sleep(wait_seconds)
    return "Done"


@timeit
def other_time_waster():
    return


def new_time_waster():
    time.sleep(2)

def measured_time_waster():
    print("Start")
    start = time.time()
    new_time_waster()
    elapsed = time.time()-start
    print("End", round(elapsed, 2))

def random_time_waster():
    time.sleep(random.random()*3)

if __name__ == '__main__':
    #time_waster(1)
    measured_time_waster()

    random_time_waster()

    #viel viele Zeilen Code
    measured_time_waster()