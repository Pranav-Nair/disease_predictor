from flask import Blueprint,request,jsonify
import joblib
mlcore = Blueprint("mlcore",__name__,url_prefix="/predict")

@mlcore.get("/diabetese")
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
    if res == 1 :
        result = "yes"
        f = open("preventions/diabetese.txt","r")
        prev = f.readlines()
        f.close()
        for line in prev:
            prevstrats.append(line.strip('\n'))
        return jsonify({"result":result,"bmi":bmi,"diabetese pedigree function":dpf,\
            "prevention methods":prevstrats}),200
    else:
        return jsonify({"result":result,"bmi":bmi,"diabetese pedigree function":dpf}),200



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

    
