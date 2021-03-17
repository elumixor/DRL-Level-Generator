def prompt(message):
    answer = input(f"{message} ")
    if answer == "y":
        return True

    if answer == "n" or answer == "":
        return False

    else:
        print("Invalid input")
        return False
