f = open("PPX-TDG_211206_221206f (1).txt", 'r')

print(f.readline())

max_ = 0
min_ = 2147483647
duration = 0
zones_amount = 100
zones = []


def print_matrix(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end=' ')
        print()


def get_zone(price):
    zone = 0
    m = max_ - duration
    while m >= min_:
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


# def occurrence_to_transition_matrix(matrix):
#     transition_matrix = []
#
#     for row in matrix:
#         sum_ = 0
#         for i in row:
#             if i != 0:
#                 sum_ += i
#
#         nrow = []
#         for i in row:
#             nrow.append(i / sum_)
#         transition_matrix.append(nrow)
#
#     return transition_matrix


avg_prices = []

for line in f:
    high = float(line.split(',')[5])
    low = float(line.split(',')[6])

    avg = (high + low) / 2
    avg_prices.append(avg)

    if high > max_:
        max_ = high

    if low < min_:
        min_ = low

duration = (max_ - min_) / zones_amount

occurrence_matrix = [[0] * zones_amount for _ in range(zones_amount)]

m = max_ - duration
zone = 0
prev_zone = 0

# find zone of first element
while m >= min_:
    if m >= avg_prices[0]:
        m -= duration
        zone += 1
    else:
        occurrence_matrix[zone][zone] += 1
        prev_zone = zone
        break

# rest prices
for price in avg_prices:
    m = max_ - duration
    zone = 0

    while m >= min_:
        if m >= price:
            m -= duration
            zone += 1
        else:
            occurrence_matrix[prev_zone][zone] += 1
            prev_zone = zone
            break

print(print_matrix(occurrence_matrix))

current_average_price = avg_prices[-1]
current_average_price_zone = get_zone(current_average_price)

print("Zone duration: {}".format(duration))
print("Current average price zone: {}".format(current_average_price_zone))
print("Current average price : {} ".format(current_average_price))

outcomes = occurrence_matrix[current_average_price_zone]

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
    outcomes = occurrence_matrix[zone]
    next_zone = get_most_probable_zone(outcomes)
    occurrence_matrix[zone][next_zone] += 1
    zone = next_zone

print(zone)

zone_limits = get_zone_limits(zone)
print(
    "Most probable price in {} hours is between {} - {} RUB".format(hours, zone_limits[0], zone_limits[1]))
