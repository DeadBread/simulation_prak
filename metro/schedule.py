import random

class Schedule(object):

    standard_wait_interval = 2
    peak_wait_interval = 1

    peak_go_interval = 6

    # assuming metro opens at 6:00
    # peak hour start at 8:00
    peak_hour_one_start = 2 * 60
    # ends at 11:00
    peak_hour_one_end = 5 * 60

    # second one starts at 18:00
    peak_hour_two_start = 12 * 60
    # ends at 21:00
    peak_hour_two_end = 15 * 60

    standard_delay_probability = 0.1
    peak_delay_probability = 0.3
    max_delay_time = 10



    def __init__(self, env, params):

        self.timer = 0

        self.env = env
        self.s_num = params.num_stations.get()
        self.t_num = params.num_trains.get()

        self.go_interval = params.go_time.get()
        self.wait_interval = params.stay_time.get()

        self.standard_wait_interval = params.stay_time.get()
        self.standard_go_interval = params.go_time.get()

        # self.standard_go_interval = params.go_time
        # self.standard_wait_interval = params.stay_time

        self.generator = random.SystemRandom

        self.train_interval = self.count_train_interval()
        self.initial_delay = self.train_interval

        self.delay_probability = Schedule.standard_delay_probability

    def count_train_interval(self):
        round_trip_time = self.s_num * 2 * self.standard_wait_interval +  self.go_interval * (self.s_num * 2 - 2)
        return round_trip_time / self.t_num

    def delay(self):
        # if self.generator.random(self) < self.delay_probability:
        if random.random() < self.delay_probability:
            return random.randint(1, Schedule.max_delay_time)
        else:
            return 0

    def start_peak(self, time):
        return time == Schedule.peak_hour_one_start or time == Schedule.peak_hour_two_start


    def end_peak(self, time):
        return time == Schedule.peak_hour_one_end or time == Schedule.peak_hour_two_end


    def run(self):
        try:
            while True:
                yield self.env.timeout(1)
                self.timer += 1

                if self.start_peak(self.timer):
                    self.delay_probability = Schedule.peak_delay_probability
                    self.wait_interval = Schedule.peak_wait_interval
                    self.go_interval = Schedule.peak_go_interval
                    self.train_interval = self.count_train_interval()

                if self.end_peak(self.timer):
                    self.delay_probability = Schedule.standard_delay_probability
                    self.wait_interval = self.standard_wait_interval
                    self.go_interval = self.standard_go_interval
                    self.train_interval = self.count_train_interval()
        except StopIteration():
            return 0




