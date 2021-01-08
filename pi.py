import argparse
import datetime
import multiprocessing
import random
import sys
import time


def monte_carlo_pi_part(n):
    """Calculate the number of points in the unit circle

    :param n: number of points to simulate
    :return: number of points in the unit circle
    """
    count = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            count = count + 1
    return count


class BenchMarkCpuJob():
    def __init__(self, num_of_points):
        self._num_of_points = num_of_points

    def run(self):
        start_time = time.time()
        cpu_count = multiprocessing.cpu_count()
        print(f"Benchmark running on {cpu_count} CPUs")
        pool = multiprocessing.Pool(processes=cpu_count)

        num_of_points_list = [int(self._num_of_points / cpu_count) for i in range(cpu_count)]
        count = pool.map(monte_carlo_pi_part, num_of_points_list)
        result = sum(count) / (sum(num_of_points_list) * 1.0) * 4
        print(f"Estimated value of Pi is {result}")
        runtime = time.time() - start_time
        print(f"Time used: {datetime.timedelta(seconds=runtime)}s")


def parse_args(args):
    """Parse command line args
    """
    parser = argparse.ArgumentParser(
        description="Benchmark CPU")
    parser.add_argument("-n",
                        "--num_of_points",
                        help="Number of points for the Pi estimation",
                        default=10000,
                        type=int)
    parser.add_argument("-t",
                        "--times",
                        help="Number of times to run the Pi estimation",
                        default=1,
                        type=int)
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    for i in range(args.times):
        BenchMarkCpuJob(args.num_of_points).run()


if __name__ == '__main__':
    main()
