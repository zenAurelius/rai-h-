
#----------------------------------------------------------------------------------------------
def convert_season(x) :
    if x in ['12', '01', '02'] :
        return 0
    if x in ['03', '04', '05'] :
        return 1
    if x in ['06', '07', '08'] :
        return 2
    if x in ['09', '10', '11'] :
        return 3
    return 4 

