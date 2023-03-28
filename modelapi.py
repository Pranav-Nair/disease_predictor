from flask import Blueprint,request,jsonify
import joblib
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

mlcore = Blueprint("mlcore",__name__,url_prefix="/predict")

@mlcore.post("/diabetese")
def predict_diabetese():
    glucose = request.json.get("glucose",None)
    bp = request.json.get("bp",None)
    skinthickness = request.json.get("skinthickness",None)
    height = request.json.get("height",None)
    weight = request.json.get("weight",None)
    age = request.json.get("age",None)
    insulin = request.json.get("insulin",None)
    fdac = request.json.get("fdac",None)
    sdac = request.json.get("sdac",0)
    tdac =request.json.get("tdac",0)
    if not glucose or not bp or not skinthickness or not height or not weight \
        or not age or insulin is None or fdac is None:
        return jsonify({"error":"mising fields","required fields":["glucose","bp",\
            "skinthickness","height","weight","age","insulin","fdac","sdac","tdac"]}),400
    try:
        glucose = int(glucose)
        bp = int(bp)
        skinthickness = int(skinthickness)
        height = float(height)
        weight = float(weight)
        age = int(age)
        insulin = int(insulin)
        fdac = int(fdac)
        sdac = int(sdac)
        tdac = int(tdac)
    except Exception as e:
        return jsonify({"error":"invalid value","msg":e}),400
    if glucose <= 0 or bp <= 0 or skinthickness <= 0 or height <= 0 or weight <= 0 or \
        age <= 0 or fdac < 0 or sdac < 0 or tdac < 0 or insulin <0:
        return jsonify({"error":"invalid values","non zero fields":["glucose","bp",\
            "skinthickness","height","weight","age","insulin<0","fdac","sdac","tdac","sdac","tdac"]}),400

    bmi = weight/(height**2)
    dpf = (0.07*fdac) + (0.02*sdac) + (0.01*tdac)
    data = [[glucose,bp,skinthickness,insulin,bmi,dpf,age]]
    model = joblib.load("models/diabetese.joblib")
    res = model.predict(data)
    result = "no"
    prevstrats = []
    f = open("preventions/diabetese.txt","r")
    prev = f.readlines()
    f.close()
    for line in prev:
        prevstrats.append(line.strip('\n'))
    if res == 1 :
        result = "yes"
        return jsonify({"result":result,"bmi":bmi,"diabetese pedigree function":dpf,\
            "prevention methods":prevstrats}),200
    else:
        return jsonify({"result":result,"bmi":bmi,"diabetese pedigree function":dpf,"prevention methods":prevstrats}),200



@mlcore.get("/heartdisease")
def predict_heartissue():
    age = request.json.get("age",None)
    gender = request.json.get("gender",None)
    cp = request.json.get("cp","")
    resrbps = request.json.get("restbps",None)
    chol = request.json.get("chol",None)
    fbs = request.json.get("fbs",None)
    restecg = request.json.get("restecg",None)
    thalach = request.json.get("thalach",None)
    exang = request.json.get("exang",None)
    oldpeak = request.json.get("oldpeak",None)
    slope = request.json.get("slope",None)
    ca = request.json.get("ca",None)
    thal = request.json.get("thal",None)
    if not age or not gender or cp is None or not resrbps or fbs is None or restecg is None or \
        thalach is None or exang is None or oldpeak is None or slope is None or ca is None or thal is None or not chol:
        return jsonify({"error":"missing fields","fields required":["age", "gender","cp","restbps","chol","trestbps",\
            "fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]}),400
    
    if age <=0 or cp <0 or resrbps <=0 or fbs <0 or restecg <0 or thalach <=0 or oldpeak <0 \
        or slope <0 or ca <0 or thal <=0 or chol <=0: 
        return jsonify({"error":"invalid values","non zero fields":["age","restbps","thalach","thal","chol"], \
            "non negative fields":["cp","restecg","oldpeak","slope","ca"]}),400
    
    if gender not in ["male","fename"]:
        return jsonify({"error":"gener can only be [male,female]"}),400
    
    if gender == "male":
        gender = 1
    else:
        gender = 0
    
    if not isinstance(exang,bool):
        return jsonify({"error":"exang can be true or false"})
    
    if exang:
        exang =1
    else:
        exang = 0

    if fbs !=0 and fbs !=1:
        return jsonify({"error":"fbs can be 0 or 1"}),400

    if restecg > 2:
        return jsonify({"error":"restecg cannot cross 2"}),400
    
    if cp > 4:
        return jsonify({"error":"cp cannot be more than 4"}),400
    
    if slope > 3:
        return jsonify({"error":"slope cannot be more than 3"}),400
        
    if ca > 3:
        return jsonify({"error":"ca cannot be more than 3"}),400
    
    if thal > 7:
        return jsonify({"error":"thal cannot cross 7"}),400

    data = [[age,gender,cp,resrbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]]
    model = joblib.load("models/heart_disease.joblib")
    res = model.predict(data)
    result = "no"
    prevstrats = []
    if res == 1:
        result = "yes"
        f = open("preventions/heartissues.txt","r")
        prev = f.readlines()
        f.close()
        for line in prev:
            prevstrats.append(line.strip('\n'))
        return jsonify({"result":result,"prevention methods":prevstrats}),200
    else:
        return jsonify({"result":result}),200


@mlcore.get("/lungcancer")
def predictLungCancer():
    gender = request.json.get("gender",None)
    age = request.json.get("age",None)
    smoking = request.json.get("smoking",None)
    yellow_fingers = request.json.get("yellow_fingers",None)
    anxity = request.json.get("anxity",None)
    peer_pressure = request.json.get("peer_pressure",None)
    chronicDisease = request.json.get("chronic_disease",None)
    fatigue = request.json.get("fatigue",None)
    allergy = request.json.get("allergy",None)
    wheezing = request.json.get("wheezing",None)
    alchol = request.json.get("alchol",None)
    cough = request.json.get("cough",None)
    shortness_of_breath = request.json.get("shortness_of_breath",None)
    swallowing_difficulty = request.json.get("swallowing_difficulty",None)
    chest_pain = request.json.get("chest_pain",None)
    
    if not gender or not age or smoking is None or yellow_fingers is None or anxity is None or \
        peer_pressure is None or chronicDisease is None or fatigue is None or allergy is None or \
        wheezing is None or alchol is None or cough is None or shortness_of_breath is None or \
        swallowing_difficulty is None or chest_pain is None:

        return jsonify({"error":"missing fields","required fields":["gender","age","smoking","yellow_fingers",\
                                                                    "anxity","peer_pressure","chronic_disease","fatigue","allergy","wheezing","alchol","cough",\
                                                                        "shortness_of_breath","swallowing_difficulty","chest_pain"]}),400
    
    if gender not in ["male","female"]:
        return jsonify({"error":"gender can only be male or female"}),400
    
    if age <=0:
        return jsonify({"error":"age cannot be less than or equal to 0"}),400
    
    if not isinstance(smoking,bool):
        return jsonify({"error":"smoking can be true or false"})
    
    if not isinstance(yellow_fingers,bool):
        return jsonify({"error":"yellow_fingers can be true or false"})
    
    if not isinstance(anxity,bool):
        return jsonify({"error":"anxity can be true or false"})
    
    if not isinstance(peer_pressure,bool):
        return jsonify({"error":"peer_pressure can be true or false"})
    
    if not isinstance(chronicDisease,bool):
        return jsonify({"error":"chronic_disease can be true or false"})
    
    if not isinstance(fatigue,bool):
        return jsonify({"error":"fatigue can be true or false"})
    
    if not isinstance(allergy,bool):
        return jsonify({"error":"allergy can be true or false"})
    
    if not isinstance(wheezing,bool):
        return jsonify({"error":"wheezing can be true or false"})
    
    if not isinstance(alchol,bool):
        return jsonify({"error":"alchol can be true or false"})
    
    if not isinstance(cough,bool):
        return jsonify({"error":"cough can be true or false"})
    
    if not isinstance(shortness_of_breath,bool):
        return jsonify({"error":"shortness_of_breath can be true or false"})
    
    if not isinstance(swallowing_difficulty,bool):
        return jsonify({"error":"swallowing_difficulty can be true or false"})
    
    if not isinstance(chest_pain,bool):
        return jsonify({"error":"chest_pain can be true or false"})
    
    if gender == 'male':
        gender = 1
    else:
        gender = 0
    
    if smoking:
        smoking = 2
    else:
        smoking = 1

    if yellow_fingers:
        yellow_fingers = 2
    else:
        yellow_fingers = 1
    
    if anxity:
        anxity = 2
    else:
        anxity = 1
    
    if peer_pressure:
        peer_pressure = 2
    else:
        peer_pressure = 1

    if chronicDisease:
        chronicDisease = 2
    else:
        chronicDisease = 1

    if fatigue:
        fatigue = 2
    else:
        fatigue = 1

    if allergy:
        allergy = 2
    else:
        allergy = 1

    if wheezing:
        wheezing = 2
    else:
        wheezing = 1

    if alchol:
        alchol = 2
    else:
        alchol = 1

    if cough:
        cough = 2
    else:
        cough = 1

    if shortness_of_breath:
        shortness_of_breath = 2
    else:
        shortness_of_breath = 1

    if swallowing_difficulty:
        swallowing_difficulty = 2
    else:
        swallowing_difficulty = 1

    if chest_pain:
        chest_pain = 1
    else:
        chest_pain = 0
    
    data = [[gender,age,smoking,yellow_fingers,anxity,peer_pressure,chronicDisease,fatigue,allergy,wheezing,alchol,cough,shortness_of_breath,swallowing_difficulty,chest_pain]]
    model = joblib.load("models/lungcancer.joblib")
    res = model.predict(data)
    result = "no"
    prevstrats = []
    if res == "YES":
        result = "yes"
        f = open("preventions/lungcancer.txt","r")
        prev = f.readlines()
        f.close()
        for line in prev:
            prevstrats.append(line.strip('\n'))
        return jsonify({"result":result,"prevention methods":prevstrats}),200
    elif res == "NO":
        return jsonify({"result":result}),200


@mlcore.get("/thyroid")
def predict_thyroid():
    Age	=request.json.get("Age",None)
    T3=request.json.get("T3",None)
    TT4=request.json.get("TT4",None)
    T4U=request.json.get("T4U",None)
    FTI=request.json.get("FTI",None)
    gender=request.json.get("gender",None)
    Sick_t=request.json.get("Sick_t",None)
    Pregnant_t=request.json.get("Pregnant_t",None)
    Thyroid_Surgery_t=request.json.get("Thyroid_Surgery_t",None)
    Goitre_t=request.json.get("Goitre_t",None)
    Tumor_t=request.json.get("Tumor_t",None)


    
    if  gender is None or Age is None or \
        Sick_t is None or Pregnant_t is None or Thyroid_Surgery_t is None  or \
        TT4 is None or T3 is None or \
        T4U is None or Goitre_t is None or FTI is None or Tumor_t is None:
        
        return jsonify({"error":"missing fields","required fields":["gender","age",\
                                                                         "Sick_t","Pregnant_t","Thyroid_Surgery_t",\
                                                                         "TT4","T4U","T3","Goitre_t","FTI",\
                                                                             "Tumor_t"]}),400

    if gender not in ["male","female"]:
        return jsonify({"error":"gender can only be male or female"}),400 

    if not isinstance(Age,int):
            return jsonify({"error":"age must be an integer"}),400

        
    if not isinstance(T3,float):
            return jsonify({"error":"T3 must be an float"}),400

    if not isinstance(Sick_t,bool):   
            return jsonify({"error":"sick can be true or false"}),400   

    if not isinstance(Pregnant_t,bool):   
            return jsonify({"error":"pregnant can be true or false"}),400   

    if not isinstance(Thyroid_Surgery_t,bool):    
            return jsonify({"error":"thyroid_surgery can be true or false"}),400        


    if not isinstance(TT4,float):
            return jsonify({"error":"TT4 must be an float"}),400


    if not isinstance(T4U,float):
            return jsonify({"error":"T4U must be an float"}),400
    

    if not isinstance(FTI,float):
            return jsonify({"error":"FTI must be an float"}),400
    
    if not isinstance(Goitre_t,bool):
            return jsonify({"error":"Goitre can be true or false"}),400
    
    if not isinstance(Tumor_t,bool):
            return jsonify({"error":"Tumor can be true or false"}),400

    

    if gender == 'male':
        gender = 1
    else:
        gender = 0

    if Sick_t:
            sick = 1
    else:
            sick = 0

    if Pregnant_t:
            pregnant = 1
    else:
            pregnant = 0

    if Thyroid_Surgery_t:
            thyroid_surgery = 1
    else:
            thyroid_surgery = 0

    if Goitre_t:
            Goitre = 1
    else:
            Goitre = 0

    if Tumor_t:
            Tumor = 1
    else:
            Tumor = 0



    model = joblib.load("models/thyroid.joblib")
    data = [[Age,T3,TT4,T4U,FTI,gender,Sick_t,Pregnant_t,Thyroid_Surgery_t,Goitre_t,Tumor_t]]
    #return jsonify({"data":data}),200        
    prediction=model.predict((data))
    result="no"
    if prediction[0]==0:
            result="hyperthyroid"
            prevention=[]
            f = open("preventions/thyroid.txt","r")
            prev = f.readlines()
            f.close()
            for line in prev:
               prevention.append(line.strip('\n'))
            return jsonify({"result":result,"prevention methods":prevention}),200
    elif prediction[0]==1:
            result="hypothyroid"
            prevention=[]
            f = open("preventions/thyroid.txt","r")
            prev = f.readlines()
            f.close()
            for line in prev:
               prevention.append(line.strip('\n'))
            return jsonify({"result":result,"prevention methods":prevention}),200
    elif prediction[0]==2 or prediction[0]==3:
             result="negative"
             prevention=[]
             f = open("preventions/thyroid.txt","r")
             prev = f.readlines()
             f.close()
             for line in prev:
                prevention.append(line.strip('\n'))
             return jsonify({"result":result,"prevention methods":prevention}),200                      
    else:
        return jsonify({"result":result}),200

    








        


    
