from flask import Blueprint , render_template,request,jsonify
import json
import requests
webapp = Blueprint("webapp",__name__)

@webapp.route("/diabetese")
def load_diabetese_page():
    return render_template("website/diabetese.html")

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


