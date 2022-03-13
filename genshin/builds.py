import matplotlib.pyplot as plt
import pandas as pd


#### Load data from characters
def loaddata(character_name):

    df = pd.read_csv("/home/rubenm/repos/genshin/genshin/Characters.csv")
    df1 = df.loc[df["Name"] == character_name]
    return df1

def adddatatodf(source,df1,hp=0,atk=0,deff=0,hpp=0,atkp=0,defp=0,edmg=0,fdmg=0,em=0,cr=0,cdmg=0,er=0,hp_=0,atk_=0,def_=0,hb=0):

    dictionary_of_stats = {"Name":source,"hp":hp,"atk":atk,"def":deff,"hpp":hpp,"atkp":atkp,"defp":defp,
                            "edmg":edmg,"fdmg":fdmg,"em":em,"cr":cr,"cdmg":cdmg,"er":er,"hp%":hp_,"atk%":atk_,"def%":def_,"hb":hb}

    df2 = df1.append(dictionary_of_stats,ignore_index=True)

    return df2

def getsumofstats(df2):

    suma = df2.sum()
    suma["Name"] = "final_stats"
    df3 = df2.append(suma,ignore_index=True)

    return df3

def singleattack(dict_stats,hability_dmg,basis='ATK',Elemental=True,Fisical=False,lvl=90,enemy_lvl=93,Enemy_RES=10):

    Enemy_DEF = (lvl+100)/(lvl+enemy_lvl+200)
    if Elemental == True:
        type_of_dmg = 'EDMG'
        Fisical=False
    elif Fisical == True:
        type_of_dmg = 'FDMG'
        Elemental = False

    DMG_of_an_attack = dict_stats[basis]*hability_dmg/100*(1+dict_stats[type_of_dmg]/100)*Enemy_DEF*(100-Enemy_RES)/100*(1+dict_stats['CDMG']/100)

    return DMG_of_an_attack
