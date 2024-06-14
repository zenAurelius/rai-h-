import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import flatdict


cr_k=['numReunion', 'numOrdre', 'heureDepart', 'libelleCourt', 'montantPrix', 'parcours', 'distance', 'distanceUnit', 'corde', 'discipline', 'specialite', 'categorieParticularite', 'conditionSexe', 'nombreDeclaresPartants', 'grandPrixNationalTrot', 'numSocieteMere', 'montantTotalOffert', 'montantOffert1er', 'montantOffert2eme', 'montantOffert3eme', 'montantOffert4eme', 'montantOffert5eme', 'numCourseDedoublee', 'dureeCourse', 'hippodrome_codeHippodrome']
ch_k = ["nom","numPmu","age","sexe","race","statut","oeilleres","proprietaire","entraineur","deferre","driver","driverChange","robe_code","indicateurInedit","musique","nombreCourses","nombreVictoires","nombrePlaces","nombrePlacesSecond","nombrePlacesTroisieme","gainsParticipant_gainsCarriere","gainsParticipant_gainsVictoires","gainsParticipant_gainsPlace","gainsParticipant_gainsAnneeEnCours","gainsParticipant_gainsAnneePrecedente","nomPere","nomMere","ordreArrivee","jumentPleine","engagement","supplement","handicapDistance","poidsConditionMonteChange","tempsObtenu","reductionKilometrique","dernierRapportDirect_rapport","dernierRapportDirect_indicateurTendance","dernierRapportDirect_permutation","dernierRapportDirect_favoris","dernierRapportDirect_grossePrise","dernierRapportReference_rapport","dernierRapportReference_typeRapport","dernierRapportReference_indicateurTendance","dernierRapportReference_permutation","dernierRapportReference_favoris","dernierRapportReference_grossePrise","eleveur","allure","avisEntraineur"]

def get_race_data(date):
    url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}?meteo=true&specialisation=INTERNET"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)["programme"]
        return data
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None
    
def process_race_data(programme, date):
    
    reunion_data = programme["reunions"][0]
    race_data = reunion_data["courses"][0]
    cf = flatdict.FlatDict(race_data, delimiter="_")
    participants_url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R1/C1/participants?specialisation=INTERNET"
    response = requests.get(participants_url)
    if response.status_code == 200:
        participants_data = json.loads(response.content)["participants"]
        for p in participants_data:
            pf = flatdict.FlatDict(p, delimiter="_")
            for rk in cr_k:
                if 'cr_' + rk not in datas:
                    datas['cr_' + rk] = []
                datas['cr_' + rk].append(cf.get(rk,None))
            for ck in ch_k:
                if 'ch_' + ck not in datas:
                    datas['ch_' + ck] = []
                datas['ch_' + ck].append(pf.get(ck,None))
        print(datas)
        #print('","'.join(k_list))
    else:
        print(f"Error fetching participants for race : {response.status_code}")


def process_programme_data(programme, date):
    # Extract relevant information from the race data
    for reunion in programme["reunions"]:
        for course in reunion["courses"]:
            if course["discipline"] == 'ATTELE' :
                cf = flatdict.FlatDict(course, delimiter="_")
                participants_url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R{course['numReunion']}/C{course['numOrdre']}/participants?specialisation=INTERNET"
                response = requests.get(participants_url)

                if response.status_code == 200:
                    participants_data = json.loads(response.content)["participants"]
                    for p in participants_data:
                        pf = flatdict.FlatDict(p, delimiter="_")
                        for rk in cr_k:
                            if 'cr_' + rk not in datas:
                                datas['cr_' + rk] = []
                            datas['cr_' + rk].append(cf.get(rk,None))
                        for ck in ch_k:
                            if 'ch_' + ck not in datas:
                                datas['ch_' + ck] = []
                            datas['ch_' + ck].append(pf.get(ck,None))
                else:
                    print(f"Error fetching participants for race {course['nom']}: {response.status_code}")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Iterate over dates from 01012014 to 06062024
start_date = datetime(2013, 1, 1)
end_date = datetime(2014, 1, 1)


datas = {}
for date in daterange(start_date, end_date):
    date_str = date.strftime("%d%m%Y")
    print(date_str)
    race_data = get_race_data(date_str)
    if race_data:
        process_programme_data(race_data, date_str)
        #process_race_data(race_data, date_str)
df = pd.DataFrame(datas)
df.to_csv('./data/pmu2013.csv', index=False)


