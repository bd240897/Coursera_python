from contracts import contract

@contract
def f(n: int) -> int:
    return n

x = int(input("Enter positive number, please: "))
assert x > 0, "Value should be positive!"