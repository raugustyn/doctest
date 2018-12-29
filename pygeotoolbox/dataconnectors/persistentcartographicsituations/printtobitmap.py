from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret


def uniq( seq ): 
    """ the 'set()' way ( use dict when there's no set ) """
    return list(set(seq))
    
def get_object_attrs( obj ):
    # code borrowed from the rlcompleter module ( see the code for Completer::attr_matches() )
    ret = dir( obj )
    ## if "__builtins__" in ret:
    ##    ret.remove("__builtins__")

    if hasattr( obj, '__class__'):
        ret.append('__class__')
        ret.extend( get_class_members(obj.__class__) )

        ret = uniq( ret )

    return ret   
    
situationParams = {
    "24": {
        "maxX": -860482.65614835,
        "maxY": -1105024.3645820732,
        "minY": -1105216.5268597424,
        "height": 1544,
        "minX": -860847.7255766749,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_21.png"
    },
    "25": {
        "maxX": -856615.3798204268,
        "maxY": -1092708.9946462773,
        "minY": -1092918.1217311982,
        "height": 1544,
        "minX": -857012.6789483584,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_22.png"
    },
    "26": {
        "maxX": -856615.3798204267,
        "maxY": -1092708.9946462773,
        "minY": -1092918.121731198,
        "height": 1544,
        "minX": -857012.6789483584,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_23a.png"
    },
    "27": {
        "maxX": -856683.7038398668,
        "maxY": -1092732.216644092,
        "minY": -1092889.0619577826,
        "height": 1544,
        "minX": -856981.6781858156,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_23b.png"
    },
    "20": {
        "maxX": -778543.0474936534,
        "maxY": -1116692.3424431388,
        "minY": -1117024.7259204057,
        "height": 1570,
        "minX": -779169.4497881245,
        "width": 2959,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_17.png"
    },
    "21": {
        "maxX": -767684.4842800389,
        "maxY": -990928.1986283335,
        "minY": -991137.3257132542,
        "height": 1544,
        "minX": -768081.7834079703,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_18.png"
    },
    "22": {
        "maxX": -741265.818540653,
        "maxY": -952539.8497544735,
        "minY": -952820.8378164497,
        "height": 1570,
        "minX": -741795.3622116806,
        "width": 2959,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_19.png"
    },
    "23": {
        "maxX": -717629.6885984503,
        "maxY": -968613.8280074926,
        "minY": -968773.3720765809,
        "height": 1570,
        "minX": -717930.3616997965,
        "width": 2959,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_20.png"
    },
    "28": {
        "maxX": -753312.6012770635,
        "maxY": -1107015.6467789463,
        "minY": -1107179.3183562895,
        "height": 1611,
        "minX": -753613.2743784097,
        "width": 2959,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_24.png"
    },
    "29": {
        "maxX": -806618.7244738567,
        "maxY": -989260.884143698,
        "minY": -989474.879571689,
        "height": 1579,
        "minX": -807019.6219423184,
        "width": 2959,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_25.png"
    },
    "04": {
        "maxX": -868684.0174803374,
        "maxY": -1058698.8704016684,
        "minY": -1059030.9528628145,
        "height": 1544,
        "minX": -869314.9069333449,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_04.png"
    },
    "08": {
        "maxX": -827719.5945552206,
        "maxY": -1060157.237530711,
        "minY": -1060314.082844402,
        "height": 1544,
        "minX": -828017.5689011691,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_07.png"
    },
    "119": {
        "maxX": -765942.7267683817,
        "maxY": -1202857.3051045747,
        "minY": -1203881.7738201786,
        "height": 968,
        "minX": -767363.0129422874,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/VyhlazeniLinieVodniTok.png"
    },
    "120": {
        "maxX": -665292.2439244847,
        "maxY": -981040.5534684438,
        "minY": -981753.3423940217,
        "height": 968,
        "minX": -666280.4285713086,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/generalizace_velikost_plocha.png"
    },
    "121": {
        "maxX": -701630.6552067427,
        "maxY": -1067552.2103717967,
        "minY": -1067872.3568454233,
        "height": 968,
        "minX": -702074.4946360881,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/SlouceniMalychPlochDoVetsi.png"
    },
    "122": {
        "maxX": -699258.8262443331,
        "maxY": -1071054.540032709,
        "minY": -1071822.8915694128,
        "height": 968,
        "minX": -700324.0408747622,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/BlokovaZastavbaSouvisla.png"
    },
    "123": {
        "maxX": -702526.8975080114,
        "maxY": -1076519.3625476707,
        "minY": -1077287.714084374,
        "height": 968,
        "minX": -703592.1121384406,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/NesouvislaZastavba.png"
    },
    "124": {
        "maxX": -817491.5175225347,
        "maxY": -1068378.2016840249,
        "minY": -1068547.5350175172,
        "height": 606,
        "minX": -817782.4020112565,
        "width": 1041,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//Droyda/Droyda_01.png"
    },
    "125": {
        "maxX": -817407.5920213701,
        "maxY": -1068434.6605979616,
        "minY": -1068678.064250224,
        "height": 882,
        "minX": -817848.864629043,
        "width": 1599,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//Droyda/Droyda_02.png"
    },
    "126": {
        "maxX": -817407.5920213701,
        "maxY": -1068434.6605979616,
        "minY": -1068678.064250224,
        "height": 882,
        "minX": -817848.864629043,
        "width": 1599,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//Droyda/Droyda_03.png"
    },
    "127": {
        "maxX": -817928.1786172934,
        "maxY": -1068467.3022738984,
        "minY": -1068641.1761554228,
        "height": 882,
        "minX": -818243.3989535264,
        "width": 1599,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//Droyda/Droyda_04.png"
    },
    "118": {
        "maxX": -584139.3016298994,
        "maxY": -1141166.7321851593,
        "minY": -1142447.3180796644,
        "height": 968,
        "minX": -585914.6593472816,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/RedukcePoctuOdsunJeskyne.png"
    },
    "59": {
        "maxX": -577839.730504059,
        "maxY": -1110334.1629111774,
        "minY": -1110567.5258779034,
        "height": 919,
        "minX": -578227.0812787605,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S7_Z_Budova_B_odvoz.png"
    },
    "58": {
        "maxX": -722935.3843670094,
        "maxY": -944974.3325645376,
        "minY": -945459.9283080946,
        "height": 919,
        "minX": -723741.4072338658,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S6_Z_TerenniRelief_L.png"
    },
    "55": {
        "maxX": -650479.3999822629,
        "maxY": -1057452.7283374926,
        "minY": -1058181.285540676,
        "height": 919,
        "minX": -651688.7058161183,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S3_Z_KomZelTrat_L.png"
    },
    "54": {
        "maxX": -559528.7798059438,
        "maxY": -1121514.8764337203,
        "minY": -1121810.2279737205,
        "height": 919,
        "minX": -560019.0231784611,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S2_Z_KomZelTrat_L.png"
    },
    "57": {
        "maxX": -787834.4119096188,
        "maxY": -1011740.7032400771,
        "minY": -1012234.9111182914,
        "height": 919,
        "minX": -788654.7297482874,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S5_Z_KomSilnice_L.png"
    },
    "56": {
        "maxX": -506876.9617950617,
        "maxY": -1052235.1401592032,
        "minY": -1052519.2699533096,
        "height": 919,
        "minX": -507348.5785961634,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S4_Z_KomSilnice_L.png"
    },
    "51": {
        "maxX": -562400.5002704441,
        "maxY": -1079072.3022404346,
        "minY": -1079427.8167404348,
        "height": 919,
        "minX": -562990.6059711248,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/Z_KomZelezTrat_L_S2_soubeh_zeleznic.jpg"
    },
    "50": {
        "maxX": -554017.4102908326,
        "maxY": -1100083.9645988322,
        "minY": -1100317.3275655583,
        "height": 919,
        "minX": -554404.7610655341,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/Z_KomZelezTrat_L_S1_deleni_zeleznice.jpg"
    },
    "53": {
        "maxX": -537685.6544445172,
        "maxY": -1154768.1048496836,
        "minY": -1155252.8224857857,
        "height": 919,
        "minX": -538490.219772469,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S1_Z_KomZelTrat_L.png"
    },
    "52": {
        "maxX": -668147.6400160955,
        "maxY": -1127305.0399649423,
        "minY": -1127505.8591165808,
        "height": 919,
        "minX": -668480.9724854819,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/Z_KomZelezTrat_L_S3_vlecka.jpg"
    },
    "115": {
        "maxX": -558508.4113948356,
        "maxY": -1140294.1605000724,
        "minY": -1141318.6292156754,
        "height": 968,
        "minX": -559993.2560311916,
        "width": 1403,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/odsun_silnice2x_hranice.png"
    },
    "114": {
        "maxX": -542107.4823735586,
        "maxY": -1125028.462369932,
        "minY": -1126309.0482644371,
        "height": 968,
        "minX": -543963.5381690037,
        "width": 1403,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/odsun_silnice_stupne.png"
    },
    "88": {
        "maxX": -476434.3866702181,
        "maxY": -1104724.1540903521,
        "minY": -1104938.784519613,
        "height": 1584,
        "minX": -476778.9806927395,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_44.png"
    },
    "89": {
        "maxX": -717330.0109220712,
        "maxY": -957357.6218016655,
        "minY": -957518.5946236111,
        "height": 1584,
        "minX": -717588.4564389623,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_45.png"
    },
    "111": {
        "maxX": -786698.5884211248,
        "maxY": -989676.6561970855,
        "minY": -990217.7850051018,
        "height": 1584,
        "minX": -787567.3829965199,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_ZM25_11.png"
    },
    "110": {
        "maxX": -552138.2236773025,
        "maxY": -1100203.9210450836,
        "minY": -1100539.281090804,
        "height": 1584,
        "minX": -552676.6518374921,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_10b.png"
    },
    "113": {
        "maxX": -559072.0411679298,
        "maxY": -1140993.8525244566,
        "minY": -1142018.3212400607,
        "height": 968,
        "minX": -560492.3273418355,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/odsun_silnice2x_hranice2.png"
    },
    "112": {
        "maxX": -829532.676358353,
        "maxY": -1070109.7883566658,
        "minY": -1070324.4187859262,
        "height": 1584,
        "minX": -829877.2703808743,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_ZM25_12.png"
    },
    "82": {
        "maxX": -852933.6913433261,
        "maxY": -1066742.6477158659,
        "minY": -1066957.2781451263,
        "height": 1584,
        "minX": -853278.2853658474,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_38.png"
    },
    "83": {
        "maxX": -807571.7483940751,
        "maxY": -976532.0157391337,
        "minY": -976800.3037757097,
        "height": 1584,
        "minX": -808002.4909222268,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_39.png"
    },
    "80": {
        "maxX": -795453.7359627268,
        "maxY": -1135578.6452228893,
        "minY": -1135981.077277753,
        "height": 1584,
        "minX": -796099.8497549543,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_36.png"
    },
    "81": {
        "maxX": -780977.6915870976,
        "maxY": -1009076.3268576537,
        "minY": -1009290.9572869143,
        "height": 1584,
        "minX": -781322.2856096189,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_37.png"
    },
    "86": {
        "maxX": -723464.7505818272,
        "maxY": -1034110.0246410312,
        "minY": -1034445.3846867513,
        "height": 1584,
        "minX": -724003.1787420169,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_42.png"
    },
    "87": {
        "maxX": -437478.6223495655,
        "maxY": -1131382.2650000257,
        "minY": -1131470.8262733552,
        "height": 1584,
        "minX": -437620.80948268215,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_43.png"
    },
    "84": {
        "maxX": -809965.1909459624,
        "maxY": -977517.3620278287,
        "minY": -977678.3348497745,
        "height": 1584,
        "minX": -810223.6364628533,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_40.png"
    },
    "85": {
        "maxX": -723384.3832335926,
        "maxY": -1033966.8186254525,
        "minY": -1034302.1786711726,
        "height": 1584,
        "minX": -723922.8113937823,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_41.png"
    },
    "03": {
        "maxX": -871373.8159892333,
        "maxY": -1059527.0803199185,
        "minY": -1059788.4891760694,
        "height": 1544,
        "minX": -871870.4398991477,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_03.png"
    },
    "07": {
        "maxX": -871250.6277213764,
        "maxY": -1057978.5369551391,
        "minY": -1058286.489440704,
        "height": 1544,
        "minX": -871835.6751053898,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_06b.png"
    },
    "108": {
        "maxX": -660555.2681107376,
        "maxY": -1163005.2633058978,
        "minY": -1163407.695360762,
        "height": 1584,
        "minX": -661201.3819029651,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_9b.png"
    },
    "109": {
        "maxX": -552138.2236773025,
        "maxY": -1100203.9210450836,
        "minY": -1100539.281090804,
        "height": 1584,
        "minX": -552676.6518374921,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_10a.png"
    },
    "102": {
        "maxX": -796080.5770599734,
        "maxY": -1129774.70743965,
        "minY": -1130051.552433635,
        "height": 1584,
        "minX": -796525.0579773379,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_56.png"
    },
    "103": {
        "maxX": -763953.5156553667,
        "maxY": -976576.6020026401,
        "minY": -976979.0340575041,
        "height": 1584,
        "minX": -764599.6294475944,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_57.png"
    },
    "100": {
        "maxX": -810394.2304049409,
        "maxY": -1060737.724281967,
        "minY": -1061140.1563368307,
        "height": 1584,
        "minX": -811040.3441971687,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_55a.png"
    },
    "101": {
        "maxX": -810394.2304049409,
        "maxY": -1060737.724281967,
        "minY": -1061140.1563368307,
        "height": 1584,
        "minX": -811040.3441971687,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_55b.png"
    },
    "106": {
        "maxX": -805493.9953298661,
        "maxY": -1044142.8924328331,
        "minY": -1044332.9959380401,
        "height": 1584,
        "minX": -805799.2108194884,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_60.png"
    },
    "107": {
        "maxX": -660555.2681107376,
        "maxY": -1163005.2633058978,
        "minY": -1163407.695360762,
        "height": 1584,
        "minX": -661201.3819029651,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_9a.png"
    },
    "104": {
        "maxX": -580636.587711171,
        "maxY": -1142919.1937635003,
        "minY": -1143305.486202752,
        "height": 1584,
        "minX": -581256.7889844469,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_58.png"
    },
    "105": {
        "maxX": -741788.3033829712,
        "maxY": -1045044.1559729739,
        "minY": -1045833.145050952,
        "height": 1553,
        "minX": -743080.5309674264,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_59.png"
    },
    "39": {
        "maxX": -820298.6007460416,
        "maxY": -1027150.0566013269,
        "minY": -1027359.1836862478,
        "height": 1544,
        "minX": -820695.8998739731,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_2b.png"
    },
    "38": {
        "maxX": -880054.2217851063,
        "maxY": -1038943.8845045109,
        "minY": -1039597.4066448886,
        "height": 1544,
        "minX": -881295.7815598926,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_2a.png"
    },
    "33": {
        "maxX": -764846.8815206263,
        "maxY": -1029918.2851346621,
        "minY": -1030575.7760329777,
        "height": 1553,
        "minX": -765923.7378410056,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_29.png"
    },
    "32": {
        "maxX": -765249.0701562567,
        "maxY": -1029156.5270261082,
        "minY": -1029682.5197447607,
        "height": 1553,
        "minX": -766110.5552125601,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_28.png"
    },
    "31": {
        "maxX": -765422.3725861949,
        "maxY": -1029053.6039035955,
        "minY": -1029579.5966222476,
        "height": 1553,
        "minX": -766283.8576424983,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_27.png"
    },
    "30": {
        "maxX": -809729.8624187171,
        "maxY": -990044.461171218,
        "minY": -990239.5552628008,
        "height": 1553,
        "minX": -810098.2644407502,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_26.png"
    },
    "37": {
        "maxX": -875691.1875536251,
        "maxY": -1044178.7110420843,
        "minY": -1044387.8381270049,
        "height": 1544,
        "minX": -876088.4866815567,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_1.png"
    },
    "36": {
        "maxX": -884916.2894596121,
        "maxY": -1064288.1614299663,
        "minY": -1064891.8290171623,
        "height": 1611,
        "minX": -885879.464222888,
        "width": 2570,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_32.png"
    },
    "35": {
        "maxX": -764742.8370814672,
        "maxY": -1029950.0441395628,
        "minY": -1030431.5867693152,
        "height": 1553,
        "minX": -765531.5205837176,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_31.png"
    },
    "34": {
        "maxX": -765618.7214623449,
        "maxY": -1030013.5070012304,
        "minY": -1030495.0496309828,
        "height": 1553,
        "minX": -766407.4049645953,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_30.png"
    },
    "60": {
        "maxX": -632738.9225180149,
        "maxY": -1187238.5409900458,
        "minY": -1187665.867022365,
        "height": 919,
        "minX": -633448.2255920687,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S8_Z_KomSilnice_L.png"
    },
    "61": {
        "maxX": -625703.0675152921,
        "maxY": -1013409.6781432205,
        "minY": -1013847.8291553992,
        "height": 919,
        "minX": -626430.3385831262,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S9_Z_StavebniObjekt_B.png"
    },
    "62": {
        "maxX": -776352.2061231885,
        "maxY": -1127819.135256236,
        "minY": -1128233.28258725,
        "height": 919,
        "minX": -777039.6343460962,
        "width": 1525,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S10_Z_KomSilnice_L.png"
    },
    "63": {
        "maxX": -730153.6255995493,
        "maxY": -1044325.9752248463,
        "minY": -1044655.4747636234,
        "height": 878,
        "minX": -730788.000156412,
        "width": 1691,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S11_Z_KomSilnice_L.png"
    },
    "64": {
        "maxX": -712588.2724876041,
        "maxY": -1049191.5681061784,
        "minY": -1049446.1754326294,
        "height": 878,
        "minX": -713036.327017604,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S12_Z_KomSilnice_L.png"
    },
    "65": {
        "maxX": -568491.2608330501,
        "maxY": -1107824.630957131,
        "minY": -1108111.0620145223,
        "height": 878,
        "minX": -568995.3183344023,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S13_Z_KomSilnice_L.png"
    },
    "66": {
        "maxX": -641536.9738107322,
        "maxY": -1114699.640273683,
        "minY": -1114905.5587884304,
        "height": 878,
        "minX": -641899.3464283216,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S14_Z_KomSilnice_L.png"
    },
    "67": {
        "maxX": -784924.2085601175,
        "maxY": -1003980.7365817674,
        "minY": -1004306.9684842313,
        "height": 878,
        "minX": -785498.3070503963,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S15_Z_KomSilnice_L.png"
    },
    "68": {
        "maxX": -560832.2838485333,
        "maxY": -1121114.946867544,
        "minY": -1121350.7354767965,
        "height": 878,
        "minX": -561247.2214544956,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S16_Z_StavebniObjekt_B.png"
    },
    "69": {
        "maxX": -751473.0384764282,
        "maxY": -1121311.5172562958,
        "minY": -1121778.163739532,
        "height": 878,
        "minX": -752294.2366471057,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S17_Z_KomSilnice_L.png"
    },
    "02": {
        "maxX": -871655.4630150503,
        "maxY": -1059376.6315282243,
        "minY": -1059585.758613145,
        "height": 1544,
        "minX": -872052.7621429818,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_02.png"
    },
    "06": {
        "maxX": -871250.6277213764,
        "maxY": -1057978.5369551391,
        "minY": -1058286.489440704,
        "height": 1544,
        "minX": -871835.6751053898,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_06a.png"
    },
    "99": {
        "maxX": -640553.357482286,
        "maxY": -1197165.9020637071,
        "minY": -1197388.2166730107,
        "height": 1584,
        "minX": -640910.288630162,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_54.png"
    },
    "98": {
        "maxX": -640213.3178653293,
        "maxY": -1196538.346942857,
        "minY": -1197116.364927046,
        "height": 1584,
        "minX": -641141.3388498065,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_53.png"
    },
    "91": {
        "maxX": -440543.8380657517,
        "maxY": -1126088.7277304553,
        "minY": -1126357.0157670318,
        "height": 1584,
        "minX": -440974.58059390343,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_47.png"
    },
    "90": {
        "maxX": -624533.9864135103,
        "maxY": -1159445.4483006203,
        "minY": -1159579.592318908,
        "height": 1584,
        "minX": -624749.3576775861,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_46.png"
    },
    "93": {
        "maxX": -440941.9371292586,
        "maxY": -1122678.7341235736,
        "minY": -1123014.094169294,
        "height": 1584,
        "minX": -441480.36528944824,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_49.png"
    },
    "92": {
        "maxX": -547331.6936685375,
        "maxY": -1188777.5150848695,
        "minY": -1189162.4846048087,
        "height": 1584,
        "minX": -547949.7709648503,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_48.png"
    },
    "95": {
        "maxX": -721705.2867685427,
        "maxY": -1030906.9556520213,
        "minY": -1031443.5317251736,
        "height": 1584,
        "minX": -722566.7718248462,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_51.png"
    },
    "94": {
        "maxX": -475208.3154723493,
        "maxY": -1085061.3139647434,
        "minY": -1085463.7460196076,
        "height": 1584,
        "minX": -475854.4292645769,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_50.png"
    },
    "97": {
        "maxX": -596493.7249620465,
        "maxY": -1167569.3939377195,
        "minY": -1168374.2580474461,
        "height": 1584,
        "minX": -597785.9525465016,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_52b.png"
    },
    "96": {
        "maxX": -596493.7249620465,
        "maxY": -1167569.3939377195,
        "minY": -1168374.2580474461,
        "height": 1584,
        "minX": -597785.9525465016,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_52a.png"
    },
    "11": {
        "maxX": -826805.600662292,
        "maxY": -1061166.4843257752,
        "minY": -1061689.3020380784,
        "height": 1544,
        "minX": -827798.848482121,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_10.png"
    },
    "10": {
        "maxX": -825104.6318390669,
        "maxY": -1061295.806789282,
        "minY": -1061568.7053065544,
        "height": 1544,
        "minX": -825623.0837792696,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_09.png"
    },
    "13": {
        "maxX": -737749.4154912205,
        "maxY": -959285.0099310583,
        "minY": -959611.7710012469,
        "height": 1544,
        "minX": -738370.1953786138,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_12.png"
    },
    "12": {
        "maxX": -826073.4523101179,
        "maxY": -1061446.2303691085,
        "minY": -1061969.0480814108,
        "height": 1544,
        "minX": -827066.7001299468,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_11.png"
    },
    "15": {
        "maxX": -779585.9083307786,
        "maxY": -1106565.2974811622,
        "minY": -1106783.9098975537,
        "height": 1544,
        "minX": -780001.2276683969,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_13B.png"
    },
    "14": {
        "maxX": -779495.2321817854,
        "maxY": -1106534.5571182624,
        "minY": -1106861.3181884512,
        "height": 1544,
        "minX": -780116.0120691784,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_13a.png"
    },
    "17": {
        "maxX": -768705.508517038,
        "maxY": -1120450.3072893939,
        "minY": -1120607.1526030845,
        "height": 1544,
        "minX": -769003.4828629865,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_15a.png"
    },
    "16": {
        "maxX": -779551.567196647,
        "maxY": -1106586.3374881772,
        "minY": -1106795.4645730979,
        "height": 1544,
        "minX": -779948.8663245786,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_14.png"
    },
    "19": {
        "maxX": -766575.7240680623,
        "maxY": -961828.7216669322,
        "minY": -962220.8349511587,
        "height": 1544,
        "minX": -767320.6599329341,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_16.png"
    },
    "18": {
        "maxX": -768548.3855929802,
        "maxY": -1120376.4669514638,
        "minY": -1120684.3427725597,
        "height": 1544,
        "minX": -769133.2873300217,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_15b.png"
    },
    "117": {
        "maxX": -852880.2937982824,
        "maxY": -990979.4216225239,
        "minY": -991747.7731592268,
        "height": 968,
        "minX": -853945.5084287118,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/redukce poctu_vysilac_kota.png"
    },
    "116": {
        "maxX": -795522.3974579215,
        "maxY": -987302.2815120243,
        "minY": -988582.8674065296,
        "height": 968,
        "minX": -797297.7551753038,
        "width": 1342,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM50/redukce poctu_zeleznice.png"
    },
    "48": {
        "maxX": -749611.8558970004,
        "maxY": -1142598.780306101,
        "minY": -1143179.8064681536,
        "height": 1584,
        "minX": -750544.7065792702,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_8a.png"
    },
    "49": {
        "maxX": -749611.8558970004,
        "maxY": -1142598.780306101,
        "minY": -1143179.8064681536,
        "height": 1584,
        "minX": -750544.7065792702,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_8b.png"
    },
    "46": {
        "maxX": -825744.557210087,
        "maxY": -997167.2888464412,
        "minY": -997690.1065587433,
        "height": 1544,
        "minX": -826737.805029916,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_6.png"
    },
    "47": {
        "maxX": -749568.0859058494,
        "maxY": -1142576.6329085403,
        "minY": -1143649.7850548453,
        "height": 1584,
        "minX": -751291.0560184562,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_7.png"
    },
    "44": {
        "maxX": -819473.9834831231,
        "maxY": -1023503.8222248632,
        "minY": -1023765.2310810143,
        "height": 1544,
        "minX": -819970.6073930376,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_5a.png"
    },
    "45": {
        "maxX": -819473.9834831231,
        "maxY": -1023503.8222248632,
        "minY": -1023765.2310810143,
        "height": 1544,
        "minX": -819970.6073930376,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_5b.png"
    },
    "42": {
        "maxX": -823663.7270520634,
        "maxY": -1017166.4264910321,
        "minY": -1017427.8353471835,
        "height": 1544,
        "minX": -824160.3509619778,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_4a.png"
    },
    "43": {
        "maxX": -823663.7270520634,
        "maxY": -1017166.4264910321,
        "minY": -1017427.8353471835,
        "height": 1544,
        "minX": -824160.3509619778,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_4b.png"
    },
    "40": {
        "maxX": -823012.5198022838,
        "maxY": -1026164.851158606,
        "minY": -1026556.9644428323,
        "height": 1544,
        "minX": -823757.4556671557,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_3a.png"
    },
    "41": {
        "maxX": -823012.5198022838,
        "maxY": -1026164.851158606,
        "minY": -1026556.9644428323,
        "height": 1544,
        "minX": -823757.4556671557,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM25/Situace_3b.png"
    },
    "01": {
        "maxX": -794609.6521233179,
        "maxY": -1173246.930906189,
        "minY": -1173643.0153910608,
        "height": 1544,
        "minX": -795362.1324655291,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_01.png"
    },
    "05": {
        "maxX": -870934.9353988231,
        "maxY": -1056925.8905806777,
        "minY": -1057163.781766513,
        "height": 1544,
        "minX": -871386.8804957996,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_05.png"
    },
    "09": {
        "maxX": -826789.2670750319,
        "maxY": -1061012.9036953596,
        "minY": -1061232.167247671,
        "height": 1544,
        "minX": -827205.823439089,
        "width": 2933,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_08.png"
    },
    "77": {
        "maxX": -745102.0023683802,
        "maxY": -1074665.2562861748,
        "minY": -1075000.616331895,
        "height": 1584,
        "minX": -745640.4305285701,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_33.png"
    },
    "76": {
        "maxX": -655020.8356202017,
        "maxY": -1131570.534797398,
        "minY": -1131794.1337698102,
        "height": 878,
        "minX": -655414.3220680945,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S24_Z_StavebniObjekt_B.png"
    },
    "75": {
        "maxX": -668774.0907904019,
        "maxY": -1129969.4497678436,
        "minY": -1130266.8420292947,
        "height": 878,
        "minX": -669297.437670429,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S23_Z_StavebniObjekt_B.png"
    },
    "74": {
        "maxX": -669212.8297277215,
        "maxY": -1130143.4716711587,
        "minY": -1130286.4246005046,
        "height": 878,
        "minX": -669464.3963596132,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S22_Z_StavebniObjekt_B.png"
    },
    "73": {
        "maxX": -597419.6153863233,
        "maxY": -1160550.4035344676,
        "minY": -1161141.362584477,
        "height": 878,
        "minX": -598459.5771309129,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S21_Z_StavebniObjekt_B.png"
    },
    "72": {
        "maxX": -556115.9118231457,
        "maxY": -1113003.118098567,
        "minY": -1113608.4605698192,
        "height": 878,
        "minX": -556853.740280099,
        "width": 1070,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S20_Z_KomSilnice_L.png"
    },
    "71": {
        "maxX": -726885.9762930004,
        "maxY": -995834.8962292518,
        "minY": -996189.9054185696,
        "height": 878,
        "minX": -727510.7166635259,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S19_Z_KomSilnice_L.png"
    },
    "70": {
        "maxX": -624590.0394469452,
        "maxY": -1041937.1907152446,
        "minY": -1042609.3941991082,
        "height": 878,
        "minX": -625772.9740475522,
        "width": 1545,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//TomasSituace/S18_Z_Vegetace_L.png"
    },
    "79": {
        "maxX": -743129.776770125,
        "maxY": -1054333.8772912123,
        "minY": -1055004.5973826526,
        "height": 1584,
        "minX": -744206.6330905043,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_35.png"
    },
    "78": {
        "maxX": -729005.2816737538,
        "maxY": -1026564.033398945,
        "minY": -1027028.3780776344,
        "height": 1584,
        "minX": -729750.7975878626,
        "width": 2544,
        "imageFileName": "C:/ms4w/Apache/htdocs/Generalizace/SituaceData//ZM10/Situace_34.png"
    }
}


def getImageParams(fileName):
    fileName = os.path.normpath(fileName)
    dirName = os.path.split(fileName)[0]
    situationId = dirName[dirName.rfind("_")+1:]
    if situationId in situationParams:
        params = situationParams[situationId]
        maxX = params["maxX"]
        maxY = params["maxY"]
        minY = params["minY"]
        height = params["height"]
        minX = params["minX"]
        width = params["width"]
        imageFileName = params["imageFileName"]
    else:
        minX = minY = maxX = maxY = width = height = imageFileName = None

    return (situationId, minX, minY, maxX, maxY, width, height, imageFileName)
    
def getVisibleLayersIds():
    result = []
    layers = iface.mapCanvas().layers()
    for layer in layers:
        result.append(layer.id())
    
    return result
        
    
def doPrint(minX, minY, maxX, maxY, width, height, fileName):
	#print "\t\tSaving map..."

	#print "\t\t\tCreating image object"
	img = QImage(QSize(width, height), QImage.Format_ARGB32_Premultiplied)
	color = QColor(255, 255, 255)
	img.fill(color.rgb())

	#print "\t\t\tCreating painter"
	p = QPainter()
	p.begin(img)
	p.setRenderHint(QPainter.Antialiasing)

	#print "\t\t\tCreating renderer"
	render = QgsMapRenderer()

	if False:
		layers = [iface.activeLayer().id()]
	else:
		#layers = qgis.utils.iface.legendInterface().layers()
		layers = QgsMapLayerRegistry.instance().mapLayers().keys()
        layers = getVisibleLayersIds()
    #lst = []
    #for layer in layers:
        #lst.append(layer)
        #print "Layer:", layer.name

	print "\t\tLayer set:\n\t\t\t", "\n\t\t\t".join(layers)
	render.setLayerSet(layers)

	#print "\t\t\tSetting extent"
	if False:
		rect = QgsRectangle(render.fullExtent())
	else:
		rect = QgsRectangle(minX, minY, maxX, maxY)
	#rect.scale(1.1)
	#render.setExtent(rect)
	#print "\t\t\tExtent:", rect.asWktCoordinates()

	#print "\t\t\tSetting output size"
	render.setOutputSize(img.size(), img.logicalDpiX())

	# do the rendering
	render.render(p)

	p.end()

	#print "\t\t\tSaving image"
	img.save(fileName, "png")
	print "\tDone.\n"
    
    
def printSituationsToFiles(rootDirectory, qgisProjectFileName, outputDirectory, layerGroupsToSave):
    project = QgsProject.instance()
    print "processing projects"
    projectFileNames = getQGISProjectsInPath(rootDirectory, qgisProjectFileName)
    for projectFileName in projectFileNames:
        (situationId, minX, minY, maxX, maxY, width, height, imageFileName) = getImageParams(projectFileName)
        print "\tReading", projectFileName[len(rootDirectory):]
        print "\t\tid:", situationId
        print "\t\tArea:", minX, minY, maxX, maxY, width, height
        project.read(QFileInfo(projectFileName))
    
        printFileName = outputDirectory + "Situation_" + situationId + ".png"
        print "\t\tPrinting to file", printFileName
        doPrint(minX, minY, maxX, maxY, width, height, printFileName)
    print "Done"    
    
printSituationsToFiles(
    rootDirectory="C:/ms4w/Apache/htdocs/Generalizace/TB04CUZK001_TestDataSets_Daniela/",
    qgisProjectFileName="Kompozice.qgs",
    outputDirectory = "c:/temp/",
    layerGroupsToSave = {
        "Input": "_input",
        "Tomas": "_tomas"
    }
)