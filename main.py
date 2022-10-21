from interpreter.maker import make_dart, make_swift


def main(filename="main_screen.swart"):
    with open(filename, "r") as file:
        src = file.read()

    print(make_swift(src))
    print(make_dart(src))


if __name__ == '__main__':
    main()
