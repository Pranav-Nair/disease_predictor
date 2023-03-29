from flask import Blueprint , render_template,request,jsonify
import json
import requests
webapp = Blueprint("webapp",__name__)

@webapp.route("/diabetese")
def load_diabetese_page():
    return render_template("website/diabetese.html")

@webapp.route("/thyroid")
def load_thyroid_page():
    return render_template("website/thyroid.html")

@webapp.route("/heartdisease")
def load_heart_page():
    return render_template("website/heartdisease.html")

@webapp.post("/diabetese/submit")
def submit_diabetese_data():
    glucose = request.form.get("glucose",None,type=int)
    bp = request.form.get("bloodpressure",None,type=int)
    skinthickness = request.form.get("skinthickness",None,type=int)
    height = request.form.get("height",None,type=float)
    weight = request.form.get("weight",None,type=float)
    age = request.form.get("age",None,type=int)
    insulin = request.form.get("insulin",None,type=int)
    fdac = request.form.get("fdac",None,type=int)
    sdac = request.form.get("sdac",0,type=int)
    tdac =request.form.get("tdac",0,type=int)
    data = {
        "glucose":glucose,
        "bp":bp,
        "skinthickness":skinthickness,
        "height":height,
        "weight":weight,
        "age":age,
        "insulin":insulin,
        "fdac":fdac,
        "sdac":sdac,
        "tdac":tdac
    }
    resp = requests.put("http://localhost:5000/predict/diabetese",json=data)
    if resp.status_code>=400 and resp.status_code<=500:
        det_msg=""
        if resp.status_code == 500:
            det_msg="Server down try again later"
        if resp.status_code == 404:
            det_msg="Page not found"
        elif resp.status_code>=400 and resp.status_code<500:
            det_msg = "Please make sure you filled all fields with correct data"
        json = resp.json()
        err = json["error"]
        err = err.upper()
        return render_template("website/errors/error.html",response=resp.status_code,msg=err,det_msg=det_msg)
    res = resp.json()
    result = res['result']
    title = "Diabetese Prediction Result"
    preventions = res['prevention methods']
    bmi = res['bmi']
    dpf = res['diabetese pedigree function']
    bmi_element = "<tr><th>bmi</th><td>"+str(bmi)+"</td></tr>"
    dpf_element = "<tr><th>Diabetese Predegree Function</th><td>"+str(dpf)+"</td></tr>"
    add_info = bmi_element+dpf_element
    prevelements = ''''''
    for prev in preventions:
        item = "<li>" + prev + "</li>"
        prevelements+=item
    
    return render_template("website/results/result.html",result=result,title=title,preventions=prevelements,add_info=add_info),200

@webapp.post("/thyroid/submit")
def submit_thyroid_data():
    Age = request.form.get("Age",None,type=int)
    T3 = request.form.get("T3",None,type=float)
    TT4 = request.form.get("TT4",None,type=float)
    T4U = request.form.get("T4U",None,type=float)
    FTI = request.form.get("FTI",None,type=float)
    gender=request.form.get("gender",None,type=str)
    Sick_t=request.form.get("Sick_t",None,type=bool)
    Pregnant_t=request.form.get("Pregnant_t",None,type=bool)
    Thyroid_Surgery_t=request.form.get("Thyroid_Surgery_t",None,type=bool)
    Goitre_t=request.form.get("Goitre_t",None,type=bool)
    Tumor_t=request.form.get("Tumor_t",None,type=bool)
    data = {
        "Age":Age,
        "T3":T3,
        "TT4":TT4,
        "T4U":T4U,
        "FTI":FTI,
        "gender":gender,
        "Sick_t":Sick_t,
        "Pregnant_t":Pregnant_t,
        "Thyroid_Surgery_t":Thyroid_Surgery_t,
        "Goitre_t":Goitre_t,
        "Tumor_t":Tumor_t
    }
    
    resp = requests.put("http://localhost:5000/predict/thyroid",json=data)
    if resp.status_code>=400 and resp.status_code<=500:
        det_msg=""
        if resp.status_code == 500:
            det_msg="Server down try again later"
        if resp.status_code == 404:
            det_msg="Page not found"
        elif resp.status_code>=400 and resp.status_code<500:
            det_msg = "Please make sure you filled all fields with correct data"
        json = resp.json()
        err = json["error"]
        err = err.upper()
        return render_template("website/errors/error.html",response=resp.status_code,msg=err,det_msg=det_msg)
    res = resp.json()
    result = res['result']
    title = "Thyroid Prediction Result"
    preventions = res['prevention methods']
    prevelements = ''''''
    for prev in preventions:
        item = "<li>" + prev + "</li>"
        prevelements+=item
    
    return render_template("website/results/result.html",result=result,title=title,preventions=prevelements),200


@webapp.post("/heartdisease/submit")
def submit_heart_data():
    age = request.form.get("age",None,type=int)
    gender = request.form.get("gender",None,type=str)
    cp = request.form.get("cp",None,type=int)
    resrbps = request.form.get("restbps",None,type=float)
    chol = request.form.get("chol",None,type=float)
    fbs = request.form.get("fbs",None,type=bool)
    restecg = request.form.get("restecg",None,type=int)
    thalach = request.form.get("thalach",None,type=int)
    exang = request.form.get("exang",None,type=bool)
    oldpeak = request.form.get("oldpeak",None,type=float)
    slope = request.form.get("slope",None,type=int)
    ca = request.form.get("ca",None,type=int)
    thal = request.form.get("thal",None,type=int)

    data = {
	"age": age,
	"gender": gender,
	"cp":cp,
	"restbps": resrbps,
	"chol":chol,
	"fbs": fbs,
	"restecg": restecg,
	"thalach": thalach,
	"exang": exang,
	"oldpeak": oldpeak,
	"slope": slope,
	"ca": ca,
	"thal": thal
    }

    resp = requests.put("http://localhost:5000/predict/heartdisease",json=data)
    if resp.status_code>=400 and resp.status_code<=500:
        det_msg=""
        if resp.status_code == 500:
            det_msg="Server down try again later"
        if resp.status_code == 404:
            det_msg="Page not found"
        elif resp.status_code>=400 and resp.status_code<500:
            det_msg = "Please make sure you filled all fields with correct data"
        json = resp.json()
        err = json["error"]
        err = err.upper()
        return render_template("website/errors/error.html",response=resp.status_code,msg=err,det_msg=det_msg)
    res = resp.json()
    result = res['result']
    title = "Heart Disease Prediction Result"
    preventions = res['prevention methods']
    prevelements = ''''''
    for prev in preventions:
        item = "<li>" + prev + "</li>"
        prevelements+=item
    
    return render_template("website/results/result.html",result=result,title=title,preventions=prevelements),200

