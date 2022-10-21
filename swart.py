import sys
from time import sleep

from interpreter.maker import make_dart, make_swift


def main(*args, **kwargs):
    try:
        input_filename = sys.argv[1]
    except IndexError:
        print("No input file as the first argument!")
        return -1

    prev_src = ""

    while True:
        try:
            try:
                with open(input_filename, "r") as file:
                    src = file.read()
                    if src == prev_src:
                        sleep(1)
                        continue
                    prev_src = src
            except (FileExistsError, FileNotFoundError):
                print("Input file not found")

            if "--swift-target" in sys.argv:
                try:
                    swift_target_filename = sys.argv[sys.argv.index("--swift-target") + 1]
                    with open(swift_target_filename, "w") as swift_file:
                        swift_file.write(make_swift(src))
                except (IndexError, FileNotFoundError):
                    print("--swift-target argument requires a valid path")

            if "--dart-target" in sys.argv:
                try:
                    dart_target_filename = sys.argv[sys.argv.index("--dart-target") + 1]
                    with open(dart_target_filename, "w") as dart_file:
                        dart_file.write(make_dart(src))
                except (IndexError, FileNotFoundError):
                    print("--dart-target argument requires a valid path")

            if "-l" not in sys.argv:
                break

            sleep(1)
        except AssertionError as exc:
            print(exc)
            sleep(1)
            continue


if __name__ == "__main__":
    main()
