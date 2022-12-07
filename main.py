import seaborn as sns

# f = open("SBER_211207_221207.txt", 'r')
f = open("PPX-TDG_211207_221207.txt", 'r')

print(f.readline())

max_ = 0
min = 2147483647
duration = 0


def print_transition_matrix(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end=' ')
        print()


def get_zone(price):
    zone = 0
    m = max_ - duration
    while m >= min:
        if m >= price:
            m -= duration
            zone += 1
        else:
            return zone


def get_outcomes_sum(outcomes):
    sum = 0
    for i in outcomes:
        sum += i
    return sum


def get_zone_limits(zone):
    return [max_ - (zone * duration), max_ - (zone * duration - 1)]


def get_most_probable_zone(outcomes):
    s = max(outcomes)
    return outcomes.index(s)


avg_prices = []

for line in f:
    high = float(line.split(',')[5])
    low = float(line.split(',')[6])

    avg = (high + low) / 2
    avg_prices.append(avg)

    if high > max_:
        max_ = high

    if low < min:
        min = low

zones_amount = 20
zones = []

duration = (max_ - min) / zones_amount

transition_matrix = [[0] * zones_amount for _ in range(zones_amount)]

m = max_ - duration
zone = 0
prev_zone = 0

# find zone of first element
while m >= min:
    if m >= avg_prices[0]:
        m -= duration
        zone += 1
    else:
        transition_matrix[zone][zone] += 1
        prev_zone = zone
        break

# rest prices
for price in avg_prices:
    m = max_ - duration
    zone = 0

    while m >= min:
        if m >= price:
            m -= duration
            zone += 1
        else:
            transition_matrix[prev_zone][zone] += 1
            prev_zone = zone
            break

print_transition_matrix(transition_matrix)

current_average_price = avg_prices[-1]
current_average_price_zone = get_zone(current_average_price)
print(current_average_price_zone)
print(current_average_price)

outcomes = transition_matrix[current_average_price_zone]

outcome_sum = get_outcomes_sum(outcomes)

for i in range(len(outcomes)):
    if outcomes[i] != 0:
        zone_limits = get_zone_limits(i)
        print(
            "Probability of price change to limits {} - {} in hour is {}".format(zone_limits[0], zone_limits[1],
                                                                                 outcomes[i] / outcome_sum))

print("Enter the number of hours for which you want to receive a prognosis: ")
hours = int(input())

for _ in range(hours):
    outcomes = transition_matrix[zone]
    next_zone = get_most_probable_zone(outcomes)
    transition_matrix[zone][next_zone] += 1
    zone = next_zone

print(zone)

zone_limits = get_zone_limits(zone)
print(
    "Most probable price in {} hours is between {} - {} RUB".format(hours, zone_limits[0], zone_limits[1]))
