import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import flatdict


cr_k=['numReunion', 'numOrdre', 'heureDepart', 'libelleCourt', 'montantPrix', 'parcours', 'distance', 'distanceUnit', 'corde', 'discipline', 'specialite', 'categorieParticularite', 'conditionSexe', 'nombreDeclaresPartants', 'grandPrixNationalTrot', 'numSocieteMere', 'montantTotalOffert', 'montantOffert1er', 'montantOffert2eme', 'montantOffert3eme', 'montantOffert4eme', 'montantOffert5eme', 'numCourseDedoublee', 'dureeCourse', 'hippodrome_codeHippodrome']
ch_k = ["nom","numPmu","age","sexe","race","statut","oeilleres","proprietaire","entraineur","deferre","driver","driverChange","robe_code","indicateurInedit","musique","nombreCourses","nombreVictoires","nombrePlaces","nombrePlacesSecond","nombrePlacesTroisieme","gainsParticipant_gainsCarriere","gainsParticipant_gainsVictoires","gainsParticipant_gainsPlace","gainsParticipant_gainsAnneeEnCours","gainsParticipant_gainsAnneePrecedente","nomPere","nomMere","ordreArrivee","jumentPleine","engagement","supplement","handicapDistance","poidsConditionMonteChange","tempsObtenu","reductionKilometrique","dernierRapportDirect_rapport","dernierRapportDirect_indicateurTendance","dernierRapportDirect_permutation","dernierRapportDirect_favoris","dernierRapportDirect_grossePrise","dernierRapportReference_rapport","dernierRapportReference_typeRapport","dernierRapportReference_indicateurTendance","dernierRapportReference_permutation","dernierRapportReference_favoris","dernierRapportReference_grossePrise","eleveur","allure","avisEntraineur"]


'''
    GET RACE DATA
'''
def get_race_data(date):
    url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}?meteo=true&specialisation=INTERNET"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)["programme"]
        return data
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None
    
'''
    GET PARTICIPANTS DATA
'''
def get_participants_data(course, date):
    url = f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R{course['cr_numReunion']}/C{course['cr_numOrdre']}/participants?specialisation=INTERNET"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)["participants"]
        return data
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None

'''
PROCESS PARTICIPANTS DATA
'''
def process_participants_data(race, participants):
    flatted = []
    for p in participants:
        pf = flatdict.FlatDict({'ch':p}, delimiter="_")
        flatted.append(pf)
        n = len(list(datas.items())[0][1])
        for kc, vc in pf.items():
            if kc not in datas:
                datas[kc] = [None for i in range(n)]
    for p in flatted :
        for k,v in datas.items():
            if k.startswith('cr_'):
               v.append(race.get(k, None)) 
            if k.startswith('ch_'):
                v.append(p.get(k, None))

'''
PROCESS PROGRAMME DATA :
'''   
def process_programme_data(programme, date):
    for reunion in programme["reunions"]:
        flatraces = []
        flatmeteo = {}
        if "meteo" in reunion :
            flatmeteo = flatdict.FlatDict({'cr':reunion["meteo"]}, delimiter="_")
        for course in reunion["courses"]:
            if course["discipline"] == 'ATTELE' :
                cf = flatdict.FlatDict({'cr':course}, delimiter="_")
                cf = dict(cf, **flatmeteo);
                flatraces.append(cf)
                for kr, vr in cf.items():
                    if kr not in datas:
                        datas[kr] = []

        for c in flatraces:
            participants = get_participants_data(c, date)
            if participants:
                process_participants_data(c, participants)
                

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



# Iterate over dates from 01012014 to 06062024
start_date = datetime(2014, 1, 1)
end_date = datetime(2015, 1, 1)

filename = 'pmu2014'

datas = {}
chunk = 3
c_chunk = 0
n_chunk = 0

for date in daterange(start_date, end_date):
    c_chunk += 1
    date_str = date.strftime("%d%m%Y")
    print(date_str)
    race_data = get_race_data(date_str)
    if race_data:
        process_programme_data(race_data, date_str)
    if c_chunk > chunk and datas :
        n_chunk += 1
        df = pd.DataFrame(datas)
        df.to_csv(f'./data/{filename}_{n_chunk}.csv', index=False)
        datas = {}
        c_chunk = 0
        df = None


df = pd.DataFrame(datas)
df.to_csv(f'./data/{filename}_{n_chunk}.csv', index=False)


