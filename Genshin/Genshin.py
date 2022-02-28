import sys
from random import random
import matplotlib.pyplot as plt
import datetime


def Battle_pass_important_dates():

    start_date = datetime.datetime.strptime('16022022',"%d%m%Y")
    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    list_of_important_dates = []
    week_count = 0
    Actualization_week = 0

    num_weeks = 1
    week_day = 5
    Wishes = 5

    while start_date.date() <= end_date:
        if start_date.weekday() == 2:
            Actualization_week = Actualization_week + 1
            if Actualization_week == 7:
                Wishes = 5
                Actualization_week = 0

        if Wishes > 0:
            important_date = 0
            if start_date.weekday() == week_day:
                week_count = week_count + 1
                if week_count == num_weeks:
                    week_count = 0
                    important_date = start_date
                    Wishes = Wishes - 1

            if start_date.date() > datetime.date.today() and important_date != 0:
                list_of_important_dates.append(important_date.date())

        start_date += delta

    return list_of_important_dates

def important_dates(what):

    start_date = datetime.datetime.strptime('16022022',"%d%m%Y")
    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    list_of_important_dates = []
    week_count = 0
    Wishes = 0

    if what == 'new_version':
        num_weeks = 7
        week_day = 2
    elif what == 'banner_reset':
        num_weeks = 4
        week_day = 2
    elif what == 'Battle_Pass':
        num_weeks = 1
        week_day = 5
        Wishes = 5
    elif what == 'bilibili':
        num_weeks = 7
        week_day = 4
        start_date = start_date - datetime.timedelta(days=12)

    while start_date.date() <= end_date:
        important_date = 0
        if start_date.weekday() == week_day:
            week_count = week_count + 1
            if week_count == num_weeks:
                week_count = 0
                important_date = start_date

        if start_date.date() > datetime.date.today() and important_date != 0:
            list_of_important_dates.append(important_date.date())

        start_date += delta

    return list_of_important_dates

def datesMatrix(final_day,Currently_primos,Battle_Pass=True,Battle_Pass_Premium=True,events=True):

    if final_day.date() < datetime.date.today():
        raise ValueError("You tried a past date")

    primogems_promotional = 0
    primogems_permanent = 0
    if events:
        diary = 221
    else:
        diary = 150
    abyss = 600
    paimons_bargains = 800
    bili = 300
    actualization = 600
    bannerreset = 20
    wish = 160
    Count_BP = 4

    dates_of_new_versions = []
    dates_of_banner_reset = []

    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    day = datetime.date.today()+delta

    while day <= end_date:
        primogems_promotional = primogems_promotional + diary
        if str(day).split("-")[-1] == "01" or str(day).split("-")[-1] == "16" :
            primogems_promotional = primogems_promotional + abyss
        if str(day).split("-")[-1] == "01":
            primogems_promotional = primogems_promotional + paimons_bargains
            primogems_permanent = primogems_permanent + paimons_bargains
        if day in important_dates('bilibili'):
            primogems_promotional = primogems_promotional + bili
        if day in important_dates('new_version'):
            primogems_promotional = primogems_promotional + actualization
        if day in important_dates('banner_reset'):
            primogems_promotional = primogems_promotional + bannerreset
        if Battle_Pass == True:
            if day in Battle_pass_important_dates():
                primogems_permanent = primogems_permanent + wish
            if Battle_Pass_Premium == True:
                if Count_BP > 0:
                    reward = wish
                    Count_BP = Count_BP - 1
                elif Count_BP == 0:
                    reward = 680
                    Count_BP = 4
                if day in Battle_pass_important_dates():
                    primogems_promotional = primogems_promotional + reward

        day += delta

    print('promotional banner = ' + str((primogems_promotional + Currently_primos)))
    print('permanent banner = ' + str(primogems_permanent))

    
def gold_num_prob(wishes, total_tries, currently_pitty, fifty_origin):
    '''
    It returns a list with the probabilities of achieving different quantities of
    5 star characters and a promotional 5 stars character.

    wishes: integer
    total_tries: integer
    currently_pitty: integer
    fifty_origin: Bool
    '''

    #Final vecttrd
    dens_prob = [0 for zero in range(0, 30)]
    dens_prob_Promotional_character = [0 for zero in range(0, 6)] # [quehacerconelvalor for valorquedevuelve in iterable]

    #Parameters
    prob_nonpitty = 0.006
    nonpitty_duration = 76
    prob_pitty = 0.3
    pitty_duration = 89
    prob_90 = 1

    #All tries
    for n in range(total_tries):
        first_try = True
        tries = wishes
        GOLD_total = 0
        Promotional_character = 0
        fifty = fifty_origin

        while tries > 0:
            GOLD = 0

            start_point = 1

            if first_try == True:
                start_point = currently_pitty
                first_try = False

            #Nonpitty
            for tirada in range(start_point,nonpitty_duration):
                luck = random()
                tries = tries - 1
                #print('tirada_nonpitty')

                if luck <= prob_nonpitty:
                    GOLD_total = GOLD_total + 1
                    GOLD = True
                    break

                elif tries <= 0:
                    break

                else:
                    continue

            #Pitty
            if not GOLD == True and tries > 0:

                for tirada in range(nonpitty_duration,pitty_duration):
                    luck = random()
                    tries = tries - 1

                    if luck <= prob_pitty:
                        GOLD_total = GOLD_total + 1
                        GOLD = True
                        break

                    elif tries <= 0:
                        break

                    else:
                        continue

            #Wish 90
            if not GOLD == True and tries > 0:
                GOLD_total = GOLD_total + 1
                tries = tries - 1
                GOLD = True

            #50/50
            if GOLD == True:
                if fifty == True:
                    luck_50 = random()

                    if luck_50 < 0.50000:
                        fifty = True
                        Promotional_character = Promotional_character + 1
                    elif luck_50 >= 0.50000:
                        fifty = False

                elif fifty == False:
                    Promotional_character = Promotional_character + 1
                    fifty = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob[GOLD_total] = dens_prob[GOLD_total] + 1
        if Promotional_character >= 5:
            dens_prob_Promotional_character[5] = dens_prob_Promotional_character[5] + 1
        else:
            dens_prob_Promotional_character[Promotional_character] = dens_prob_Promotional_character[Promotional_character] + 1

    return dens_prob, dens_prob_Promotional_character
