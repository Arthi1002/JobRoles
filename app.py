from flask import Flask, redirect, url_for, request,jsonify
import joblib
import pandas as pd
import json
app = Flask(__name__)
dataset = pd.read_csv("jobroles.csv")

@app.route('/jobroles',methods = ['POST'])
def jobroles():
   if request.method == 'POST':
        inputskills=[]
        output=[]
       
        '''return "hello"'''
        json_data =request.json
        #print (json_data['Employee']['Skills'][3]['Skillname'])
        for i in range (0,len(json_data['Employee']['Skills'])):
            inputskills.append(json_data['Employee']['Skills'][i]['Skillname'])
        #print(inputskills)
        inputskills=set(inputskills)
        for i in range(0,len(list(set(dataset["JobRole"])))):
            dictt= {}
            dfn= dataset.loc[dataset['JobRole'] == list(set(dataset["JobRole"]))[i]]
            jobskills=dfn['Skill']
            #print(jobskills)
            #job_list = jobskills.tolist()
            #print(job_list)
           
            intersect=inputskills.intersection(jobskills)
            common=list(intersect)
            print(common)
            score= len(common)/len(jobskills)
            print(score)
            if score>=0.2 :
                dictt["common skills"]=common
                dictt["job name"]=list(set(dataset["JobRole"]))[i]
                dictt["Score"]=score
                output.append(dictt)
                output  = sorted(output, key=lambda k: k['Score'], reverse=True)
        return jsonify(response=output)
           
           
           

if __name__ == '__main__':
   app.run(debug = True)
