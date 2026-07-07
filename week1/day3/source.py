import warnings

def operation(a, b):
#    warnings.warn("operation function is deprecated, use addition", DeprecationWarning)
    return addition(a, b)

def addition(a, b):
    return a + b