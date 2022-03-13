import sys
from random import random
import matplotlib.pyplot as plt
import datetime


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
        if day in important_dates('bilibili',final_day):
            primogems_promotional = primogems_promotional + bili
        if day in important_dates('new_version',final_day):
            primogems_promotional = primogems_promotional + actualization
        if day in important_dates('banner_reset',final_day):
            primogems_promotional = primogems_promotional + bannerreset
        if Battle_Pass == True:
            if day in Battle_pass_important_dates(final_day):
                primogems_permanent = primogems_permanent + wish
            if Battle_Pass_Premium == True:
                if Count_BP > 0:
                    reward = wish
                    Count_BP = Count_BP - 1
                elif Count_BP == 0:
                    reward = 680
                    Count_BP = 4
                if day in Battle_pass_important_dates(final_day):
                    primogems_promotional = primogems_promotional + reward

        day += delta

    primogems_promotional = primogems_promotional + Currently_primos

    return [primogems_promotional, primogems_permanent]

def Battle_pass_important_dates(final_day):

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
                if week_count == num_weeks: #1
                    week_count = 0
                    important_date = start_date
                    Wishes = Wishes - 1

            if start_date.date() > datetime.date.today() and important_date != 0:
                list_of_important_dates.append(important_date.date())

        start_date += delta

    return list_of_important_dates

def important_dates(what,final_day):

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
            if week_count == num_weeks: #2
                week_count = 0
                important_date = start_date

        if start_date.date() > datetime.date.today() and important_date != 0:
            list_of_important_dates.append(important_date.date())

        start_date += delta

    return list_of_important_dates


def gold_num_prob(wishes, total_tries, currently_pitty, fifty_origin, Number_of_5stars):
    '''
    It returns a list with the probabilities of achieving different quantities of
    5 star characters and a promotional 5 stars character.

    wishes: integer
    total_tries: integer
    currently_pitty: integer
    fifty_origin: Bool
    Number_of_5stars: integer
    '''

    #Final vecttrd
    dens_prob = [0 for zero in range(0, 25)]
    dens_prob_Promotional_character = [0 for zero in range(0, Number_of_5stars+1)] # [quehacerconelvalor for valorquedevuelve in iterable]

    #Parameters
    prob_nonpitty = 0.006
    nonpitty_duration = 76
    prob_pitty = 0.3
    pitty_duration = 90
    prob_90 = 1

    #All tries 5 stars
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
        if Promotional_character >= Number_of_5stars:
            dens_prob_Promotional_character[Number_of_5stars] = dens_prob_Promotional_character[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_character[Promotional_character] = dens_prob_Promotional_character[Promotional_character] + 1



    return [dens_prob, dens_prob_Promotional_character]

def goldweapon_num_prob(wishes, total_tries, currently_pitty, fifty_origin, Number_of_5stars):
    '''
    It returns a list with the probabilities of achieving different quantities of
    5 star weapons and promotional 5 stars weapons, distinguised.

    wishes: integer
    total_tries: integer
    currently_pitty: integer
    fifty_origin: Bool
    Number_of_5stars: integer
    '''

    #Final vecttrd
    dens_prob = [0 for zero in range(0, 25)]
    dens_prob_Promotional_weapon1 = [0 for zero in range(0, Number_of_5stars+1)] # [quehacerconelvalor for valorquedevuelve in iterable]
    dens_prob_Promotional_weapon2 = [0 for zero in range(0, Number_of_5stars+1)] # [quehacerconelvalor for valorquedevuelve in iterable]
    dens_prob_Permanent_weapon = [0 for zero in range(0, 25)] # [quehacerconelvalor for valorquedevuelve in iterable]


    #Parameters
    prob_nonpitty = 0.007
    nonpitty_duration = 66
    prob_pitty = 0.3
    pitty_duration = 80
    prob_80 = 1

    #All tries 5 stars
    for n in range(total_tries+1):
        first_try = True
        tries = wishes
        GOLD_total = 0
        Promotional_weapon1 = 0
        Promotional_weapon2 = 0
        Permanent_weapon = 0
        fifty = fifty_origin
        count_epitomized_path = 0

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

            #Wish 80
            if not GOLD == True and tries > 0:
                GOLD_total = GOLD_total + 1
                tries = tries - 1
                GOLD = True

            #75/25 & 50/50
            if GOLD == True:
                if fifty == True:
                    luck_75 = random()

                    if luck_75 < 0.75000 or count_epitomized_path == 2:
                        fifty = True
                        luck_50 = random()

                        if luck_50 < 0.5000 or count_epitomized_path == 2:
                            Promotional_weapon1 = Promotional_weapon1 + 1
                            count_epitomized_path = 0
                        elif luck_50 >= 0.5000:
                            Promotional_weapon2 = Promotional_weapon2 + 1
                            count_epitomized_path = count_epitomized_path + 1
                    elif luck_75 >= 0.75000:
                        Permanent_weapon = Permanent_weapon + 1
                        count_epitomized_path = count_epitomized_path + 1
                        fifty = False

                elif fifty == False:
                    luck_50 = random()
                    if luck_50 < 0.5000 or count_epitomized_path == 2:
                        Promotional_weapon1 = Promotional_weapon1 + 1
                        count_epitomized_path1 = 0
                    elif luck_50 >= 0.5000:
                        Promotional_weapon2 = Promotional_weapon2 + 1
                        count_epitomized_path = count_epitomized_path + 1
                    fifty = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob[GOLD_total] = dens_prob[GOLD_total] + 1
        if Promotional_weapon1 >= Number_of_5stars:
            dens_prob_Promotional_weapon1[Number_of_5stars] = dens_prob_Promotional_weapon1[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_weapon1[Promotional_weapon1] = dens_prob_Promotional_weapon1[Promotional_weapon1] + 1

        if Promotional_weapon2 >= Number_of_5stars:
            dens_prob_Promotional_weapon2[Number_of_5stars] = dens_prob_Promotional_weapon2[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_weapon2[Promotional_weapon2] = dens_prob_Promotional_weapon2[Promotional_weapon2] + 1

        dens_prob_Permanent_weapon[Permanent_weapon] = dens_prob_Permanent_weapon[Permanent_weapon] + 1

    return [dens_prob, dens_prob_Promotional_weapon1, dens_prob_Promotional_weapon2, dens_prob_Permanent_weapon]

def purple_num_prob(wishes, total_tries, four_star_garanteed = True, pitty_4star = 0):

    prob_4star = 0.06
    dens_prob_4star_temporal_character = []
    dens_prob_4star_permanent_character = []

    #All tries 4 stars
    for n in range(total_tries):
        tries = wishes
        gotcha4star = False
        four_stars = 0
        temporal_4star = 0
        other_4star = 0

        while tries > 0:

            tries = tries - 1

            if pitty_4star < 10:
                if random() <= prob_4star:
                    pitty_4star = 0
                    gotcha4star = True
                else:
                    pitty_4star = pitty_4star + 1
                    gotcha4star = False

            elif pitty_4star == 10:
                four_stars = four_stars + 1
                gotcha4star = True
                pitty_4star = 0

            else:
                print('error in number of 4 star pitty')

            if gotcha4star == True:
                if random() <= 0.5 or four_star_garanteed == True:
                    temporal_4star = temporal_4star + 1
                    four_star_garanteed = False
                else:
                    other_4star = other_4star + 1
                    four_star_garanteed = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob_4star_temporal_character.append(temporal_4star)
        dens_prob_4star_permanent_character.append(other_4star)

    average_4star_temporal = sum(dens_prob_4star_temporal_character)/len(dens_prob_4star_temporal_character)
    average_4star_permanent = sum(dens_prob_4star_permanent_character)/len(dens_prob_4star_permanent_character)

    return [average_4star_temporal, average_4star_permanent]

def needeprimos(threshold, banner, desired_5star, pitty, fifty_fifty):

    prob_is_near_threshold = False
    step = 50
    wishes = 100
    num_iterations = 1
    tries = 10000
    error = 0.009
    toomuch = False
    tooless = False
    prob_old = 0

    if threshold >= 1:
        threshold = 0.98
        print('setting threshold to 100% of probabilities')

    while prob_is_near_threshold == False:

        if banner == 'character':
            prob = gold_num_prob(wishes, tries, pitty, fifty_fifty, desired_5star)[1][-1]/tries
        elif banner == 'weapon':
            prob = goldweapon_num_prob(wishes, tries, pitty, fifty_fifty, desired_5star)[1][-1]/tries

        if prob > threshold-error and prob < threshold+error:
            prob_is_near_threshold = True
            break
        elif prob > threshold-error:
            if tooless == True:
                num_iterations = num_iterations + 1
            wishes = wishes - step/num_iterations
            toomuch = True
            tooless = False
        elif prob < threshold+error:
            if toomuch == True:
                num_iterations = num_iterations + 1
            wishes = wishes + step/num_iterations
            toomuch = False
            tooless = True
        else:
            print('error')
        prob_old = prob

    return wishes
