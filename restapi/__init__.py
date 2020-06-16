from flask import Flask,request,jsonify
from pymongo import MongoClient
from mongoengine_jsonencoder import MongoEngineJSONEncoder
import pandas as pd
app = Flask(__name__) #플라스크 객체 생성
app.json_encoder = MongoEngineJSONEncoder
app.config['JSON_AS_ASCII'] = False #인코딩


#client = MongoClient("mongodb://14.32.18.97:27017/")
client = MongoClient("14.32.18.97",27017,username='Project',password='bit')
print(client)

@app.route('/environments/<language>')
def environments(language):
    return jsonify({"language":language})

@app.route('/message/<int:message_id>')
def get_message(message_id):
    return "message id: " + message_id

@app.route("/upjong",methods=['POST'])
def upjong():
    my_db = client['Project']
    mycol = my_db['allSang']
    value = request.get_json()
    print(value)
    my_doc = list(mycol.find({"class":value.get('classes')},{"_id":0}))
    print(my_doc)

    client.close()#mongoDB닫는것.

    return jsonify(my_doc)


@app.route("/instar",methods=['POST'])
def instar():
    json = request.get_json()
    word = json.get('word')
    print(word)
    insta = []
    my_db = client['Project']
    mycol = my_db[word]
    num = json.get('num')
    my_doc1 = mycol.find()
    i=0
    for i in range(int(num)):
        q={data:json.get('date'+str(i))}
        print("a")
        print(q)
        my_doc = mycol.find(q,{"_id":0,"tags":1})
        for z in my_doc:
            print(z)
            for j in range(len(z['tags'])):
                insta.append(z['tags'][j])
        print(insta)
        q.clear()
    df = pd.DataFrame(insta, columns=['tags'])
    tag =df['tags'].value_counts().to_frame()
    top10 = tag.head(10)
    print(top10)
        


    a=[]
    for qwe in range(len(top10.index)):
        b ={"tag":top10.index[qwe],"count":str(top10['tags'][qwe])}
        a.append(b)

    print(a)
    client.close()
    return jsonify(a)



@app.route("/mongoTest",methods=['POST'])
def mongoTest():
    my_db = client['test']
    mycol = my_db['test']
    name = request.get_json()

    my_doc = list(mycol.find({},{"_id":0}))

    client.close()
    return jsonify(my_doc)

@app.route("/yearchui",methods=['POST'])
def yearchui():
    my_db = client['Project']
    mycol = my_db['yearchui2020']
    dong = request.get_json()

    my_doc = list(mycol.find({"행정동명":dong.get("dong")},{"_id":0,"m2019예측":1,"m2020예측":1,"상권_코드_명":1}))

    for i in range(len(my_doc)):
                    print(i)

    print(my_doc)
    client.close()
    return jsonify(my_doc)

@app.route("/server_info")
def server_json():

    data ={"server_name":"0.0.0.0","server_port":"8000"}

    return jsonify(data)

