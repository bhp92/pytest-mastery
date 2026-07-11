def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by Zero")
    return a/b

def slow_batch_process(items):
    """Pretend this hits a real queue/DB — expensive to run."""
    import time
    time.sleep(0.3)     # stands in for real I/O latency
    return sum(items)