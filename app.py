from flask import Flask,make_response,render_template, request, jsonify, json,jsonify
from flask import make_response, request, current_app, redirect, url_for, send_from_directory
import os,time,datetime
import  random

app = Flask(__name__)
numberOfQuestions = 5
qns = {
    "Pytania zamknięte": [
                ["s1p1","Nadawanie cech ludzkim bóstwom, zwierzętom i przedmiotom w sztuce to:",["Antropomorfizm","Abstrakcja","Antropogeneza","Ornamentowanie"],"Antropomorfizm"],
                ["s1p2","Abstrakcyjne dzieło sztuki to takie, które:",["przedstawia rzeczywistość, czarne plamy","przedstawia barwne plamy, linie, płaszczyzny, nie przedstawia rzeczywistości","nie przedstawia barw (pochodna nazwa od szkicu)","jest nudne, monotonne"],"przedstawia barwne plamy, linie, płaszczyzny, nie przedstawia rzeczywistości"],
                ["s1p3","Absydą nazwiemy:",["technikę malarską z użyciem farb temperowych","rodzaj rzeźby, przedstawiającej motywy rycerskie","zewnętrze architektoniczne w kształcie przybudówki, na planie koła, zwieńczone ćwierćkopułą","wnętrze architektoniczne w kształcie przybudówki, na planie półkola, zwieńczone półkopułą"],"wnętrze architektoniczne w kształcie przybudówki, na planie półkola, zwieńczone półkopułą"],
                ["s1p4","Najwyższa część ściany o ozdobnym charakterze znajdująca się nad gzymsem i zasłaniająca dach, nazywana jest:",["Attyką","Antarktyką","Bazyliką","Deformacją"],"Attyką"],
                ["s1p5","Bauhaus to:",["uczelnia artystyczna powstała w 1919 roku w Katowicach","uczelnia artystyczna powstała w 2000 roku w Warszawie","uczelnia artystyczna powstała w 1919 roku w Weimarze","ciekawy rodzaj dekorowania domów, od zewnątrz z wykorzystaniem betonu"],"uczelnia artystyczna powstała w 1919 roku w Weimarze"]
                ],
    "Pytania Prawda/Fałsz": [
                ["s2p1","W architekturze łuk wsparty na kolumnach lub filarach, występujący pojedynczo lub w ciągach, to arkada.",["Prawda","Fałsz"],"Prawda"],
                ["s2p2","Bazylika, to budowla na planie trójkąta o nieparzystej liczbie naw, z których główna jest niższa od bocznych.",["Prawda","Fałsz"],"Fałsz"],
                ["s2p3","Deformacja, to celowe zniekształcenie stosowane w sztuce dla podniesienia warstwy emocjonalnej.",["Prawda","Fałsz"],"Prawda"],
                ["s2p4","Faktura, to budowa powierzchni dzieła plastycznego.",["Prawda","Fałsz"],"Prawda"],
                ["s2p5","W sztukach plastycznych, hełmem nazywamy zwieńczenie wieży budowli, przyjmujące różnorodne kształty, w kolejnych epokach lub stylach architektonicznych.",["Prawda","Fałsz"],"Prawda"]
                ]

}

@app.route('/getQuestions/',methods=['POST'])
def getQuestions():
    sectionId = request.form['sectionId']
    
    sections = ["Pytania zamknięte","Pytania Prawda/Fałsz"]

    questions =  random.sample(qns[sectionId],numberOfQuestions)

    if sections.index(sectionId)==len(sections)-1:
        Next = "Finish"
    else:
        Next = sections[sections.index(sectionId)+1]

    return jsonify(qns=questions,next=Next)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
      app.run()