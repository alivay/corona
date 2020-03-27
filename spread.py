import random
import matplotlib.pyplot as plt
import numpy as np


ASYMPTOMATIC = 0
MILD = 1
SEVERE = 2
CRITICAL = 3

VICTIM_SENIROTY = 0
VICTIM_TYPE = 1
VICTIM_COMPLIANCY = 2

NUM_DAYS = 120

general_compliance_level = 0

expentancy_dir = {
        0: 0.1,
        1: 0.15,
        2: 0.25,
        3: 0.25,
        4: 0.3,
        5: 0.4,
        6: 0.25,
        7: 0.25,
        8: 0.15,
        9: 0.13,
        10: 0.1,
        11: 0.05,
        12: 0.05,
        13: 0.01
}

def randomize_patient_type():
    temp = random.randint(1,100)
    if temp<30:
        type = ASYMPTOMATIC
    elif temp<30+56:
        type = MILD
    elif temp<30+56+10:
        type = SEVERE
    else:
        type = CRITICAL
    return type

def contagions(seniority):
    try:
        return expentancy_dir[seniority]
    except:
        return 0

def get_number_of_victims(seniority, victim_level_of_compliance):
    temp = random.uniform(0,1)
    #print("victim_level_of_compliance = {}, general_compliance_level = {}".format(victim_level_of_compliance, general_compliance_level))
    #exit(0)
    if victim_level_of_compliance<general_compliance_level:
        return 0
    elif temp<contagions(seniority):
        return 1
    else:
        return 0

def get_victim_level_of_compliance():
    return random.uniform(0,1)

state=0
day = 0
victim = [0, randomize_patient_type(), get_victim_level_of_compliance()]
victims_list = []
victims_list.append(victim)
history = []
dead = 0
while day < NUM_DAYS:
    number_of_known = sum(1 if (seniority>=5) else 0 for seniority, type, compliance in victims_list)
    number_of_hospitalized = sum(1 if (type == 2 or type == 3) else 0 for seniority,type,compliance in victims_list)
    number_of_critical = sum(1 if (type == 3) else 0 for seniority,type,compliance in victims_list)

    print("day {}: Number of Victims = {}, Number of known Victims = {}, Number of Hospitalized = {}, Number of Critical = {}, Number of Dead = {}".format(
        day, len(victims_list), number_of_known, number_of_hospitalized, number_of_critical, dead))
    history.append(number_of_known)


    if len(history) >= 2:
        if state == 0 and history[-1]-history[-2] >= 31:
            state=1
            general_compliance_level = 0.2
        if state == 1 and history[-1]-history[-2] >= 244:
            state=2
            general_compliance_level = 0.7

    next_victims_list = []
    for victim in victims_list:
        victim[VICTIM_SENIROTY] = victim[VICTIM_SENIROTY] + 1
        next_victims_list.append(victim)
        if victim[VICTIM_TYPE] != CRITICAL or victim[VICTIM_SENIROTY] != 27:
            new_victims = get_number_of_victims(victim[VICTIM_SENIROTY], victim[VICTIM_COMPLIANCY])
            for i in range(new_victims):
                new_victim = [0, randomize_patient_type(), get_victim_level_of_compliance()]
                next_victims_list.append(new_victim)
        else:
            dead = dead + 1
    victims_list = next_victims_list
    day = day + 1

print("history = {}".format(history))
new_knowns = np.diff(np.array(history))
print("new_knowns = {}".format(new_knowns))
for i in range(1,len(new_knowns)-1):
    print("new_known = {}, ratio = {}".format(new_knowns[i], new_knowns[i]/new_knowns[i-1]))

plt.xlabel('Days')
plt.ylabel('Victims')
plt.title('Corona Daily New Victims Chart (70% compliance')
plt.plot(new_knowns)
plt.show()

