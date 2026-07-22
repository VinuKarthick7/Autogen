from evolution.ab_testing import ABTesting

def main():
    ab = ABTesting()
    ab.create_experiment()
    print("Running experiments... [Mocked]")

if __name__ == "__main__":
    main()
