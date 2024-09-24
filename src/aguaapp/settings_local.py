print(1)
try:
    print(2)
    from aguaapp.settings import *
    print(3)
except ImportError as e:
    pass
print(4)