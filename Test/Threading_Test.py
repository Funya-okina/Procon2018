import time
import threading


def function1():
    while True:
        print("function1")
        time.sleep(1)


def function2():
    while True:
        print("function2")
        time.sleep(0.5)


def function3():
    while True:
        print("function3")
        time.sleep(1)


if __name__ == "__main__":
    thread_1 = threading.Thread(target=function1)
    thread_2 = threading.Thread(target=function2)

    thread_1.start()
    thread_2.start()

