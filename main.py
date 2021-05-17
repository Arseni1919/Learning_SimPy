import simpy
import random
import statistics

wait_times = []

class Theater:
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.usher = simpy.Resource(env, num_ushers)
        self.server = simpy.Resource(env, num_servers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))


def go_to_movies(env, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))

    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))

    # Moviegoer heads into the theater
    wait_times.append(env.now - arrival_time)


def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)
    moviegoer = 0
    # there are 3 moviegoers already waiting in line before the opening
    for _ in range(3):
        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))

    while True:
        yield env.timeout(12 / 60)  # Wait a bit before generating a new person

        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))


# def get_average_wait_time(wait_times):
#     average_wait = statistics.mean(wait_times)


def calculate_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def main():
    # Setup
    random.seed(42)
    # num_cashiers, num_servers, num_ushers = get_user_input()
    num_cashiers = 1
    num_servers = 1
    num_ushers = 1
    # Run the simulation
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)

    # View the results
    mins, secs = calculate_wait_time(wait_times)
    print(
      "Running simulation...",
      f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )


if __name__ == '__main__':
    # num_cashiers = input("Input # of cashiers working: ")
    # num_servers = input("Input # of servers working: ")
    # num_ushers = input("Input # of ushers working: ")
    main()
# def clock(env, name, tick):
#      while True:
#          print(name, env.now)
#          yield env.timeout(tick)
#
# env = simpy.Environment()
# env.process(clock(env, 'fast', 0.5))
# env.process(clock(env, 'slow', 1))
# env.run(until=2)
