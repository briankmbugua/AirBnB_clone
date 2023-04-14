#!/usr/bin/python3
# def my_function(*args):
#     for arg in args:
#         print(arg)
# my_function(1,2,3,4)

# def my_function(**kwargs):
#     for key, value in kwargs.items():
#         print(key, value)
# my_function(name='John',age=30)

def my_function(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, value)

my_function(1,2,3, name="jonn", age=30)
