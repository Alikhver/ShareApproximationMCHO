f = open("KER.PA.csv", 'r')

f.readline()

max_ = 0
min_ = 2147483647
Zones_amount = 4
Degree = 3
duration = 0
zones = []
profitabilities = []
avgs = []

s = f.readline().split(',')
prev_price = (float(s[3]) + float(s[2])) / 2


def find_profitability_zone(p):
    counter = 0

    m = max_ - duration
    while m >= min_:
        if p <= m:
            counter += 1
            m -= duration
        else:
            return counter
    return counter - 1


def get_average_zone_profitability(zone):
    return (max_ - (zone * duration) + max_ - ((zone + 1) * duration)) / 2


for line in f:
    high = float(line.split(',')[2])
    low = float(line.split(',')[3])

    avg = (high + low) / 2
    avgs.append(avg)
    profitability = (avg - prev_price) / prev_price
    profitabilities.append(profitability)
    prev_price = avg

    if profitability > max_:
        max_ = profitability

    if profitability < min_:
        min_ = profitability

duration = (max_ - min_) / Zones_amount

print("Profitabilities: {}".format(profitabilities))

zones = [find_profitability_zone(p) for p in profitabilities]
print("Zones: {}".format(zones))

occurences = {}
sequences = {}
probabilities = {}

for i in range(len(zones) - Degree):
    sequence = tuple(zones[j] for j in range(i, i + Degree + 1))
    zone = tuple(sequence[:-1])
    if sequence in occurences.keys():
        occurences[sequence] = occurences[sequence] + 1
    else:
        occurences[sequence] = 1

    if zone in sequences.keys():
        sequences[zone] += 1
    else:
        sequences[zone] = 1

print(occurences)
print(sequences)

for o in occurences:
    sequence = tuple(o[:-1])
    probabilities[o] = occurences[o] / sequences[sequence]
    print("{} - {}".format(o, probabilities[o]))

last_sequence = [i for i in zones[-Degree:]]
print(last_sequence)

printed = 0
for i in range(Zones_amount + 1):
    last_sequence.append(i)
    prob_sequence = tuple(j for j in last_sequence)
    if prob_sequence in probabilities.keys():
        prob = probabilities[prob_sequence]
        print("Probability of next sequence to be {} is {}. Profitability for next week: {}".format(prob_sequence, prob,
                                                                                                    get_average_zone_profitability(
                                                                                                        i)))
        printed += 1
    last_sequence.pop()
if printed == 0:
    print("No probability for future week due to absence of previous records for {} sequence".format(last_sequence))