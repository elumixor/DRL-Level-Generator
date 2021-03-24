import pickle


class A: ...


def run_function(Class):
    class Top: ...

    # print(pickle.dumps(Top))
    # print(pickle.dumps(Top()))
    print(pickle.dumps(Class))
    print(pickle.dumps(Class()))


if __name__ == "__main__":
    class Kek: ...


    print(pickle.dumps(A))
    print(pickle.dumps(A()))
    print(pickle.dumps(Kek))
    print(pickle.dumps(Kek()))


    class Lol: ...


    run_function(Lol)
