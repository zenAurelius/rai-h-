import pandas as pd

'''
Remets le fichier en propre, tel qu'il devrait sortir du scrapper (bon nom de colonnes + pas de colonnes calculées)
TODO : mettre à jour le scrapper
'''
full = pd.read_csv("./data/full.csv")
full.rename(columns={ 'NOM_CHEVAL':'CH_NOM','REFERENCE':'CR_REF','NOM_COURSE':'CR_NOM','LIEUX':'CR_LIEUX','CONDUCTEUR':'CO_NOM','REUNION':'CR_REUNION','TYPE_COURSE':'CR_TYPE','DATE_COURSE':'CR_DATE',
                    'HEURE':'CR_HEURE','DISTANCE':'CR_DISTANCE','PRIX':'CR_PRIX','NB_PARTANT':'CR_PARTANT','RESULTAT_COURSE':'CR_RESULTAT','NUM_COURSE':'CR_NUMERO','SEXE_CHEVAL':'CH_SEXE','AGE_CHEVAL':'CH_AGE',
                    'POIDS':'CH_POIDS','CORDE':'CH_CORDE','NUM_PARTICIPATION':'CH_NUMERO','ENTRAINEUR':'EN_NOM','OEILLERE':'CH_OEILLERE','COTE':'CH_COTE','CHT_CO':'DCH_CO','CHT_EN':'DCH_EN',
                    'CHT_HA':'DCH_HA','CHT_PO':'DCH_PO','CO_TX_HIT':'CO_TX_GAGNE','DELTA_DISTANCE':'CH_RECUL','EST_GAGNANT':'TG_GAGNANT','EST_PLACE':'TG_PLACE','FER':'CH_FER','GAIN_G':'TG_GAIN_G',
                    'GAIN_P':'TG_GAIN_P','GAIN_S':'TG_GAIN_S','HANDICAP':'CH_HANDICAP','MUSIQUE':'CH_MUSIQUE','RESULTAT':'CH_RESULTAT','SEASON':'CR_SAISON'}, inplace=True)
full = full.drop(columns=['TX_HIT_CO', 'CO_ELO', 'CH_HANDICAP', 'CH_RESULTAT', 'ID'])

full.to_csv('./data/full_rename.csv', index=False)