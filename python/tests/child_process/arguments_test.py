try:
    import argparse

    if __name__ == '__main__':
        def get_args(*keys):
            parser = argparse.ArgumentParser()
            for key in keys:
                parser.add_argument(f'--{key}')

            args = vars(parser.parse_args())
            return [args.get(key) for key in keys]


        [working_directory, argument_value] = get_args("working_directory", "test_parameter")
        print(working_directory)
        print(argument_value)


except BaseException as e:
    print(e)
