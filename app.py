from flask import Flask,make_response,render_template, request, jsonify, json,jsonify
from flask import make_response, request, current_app, redirect, url_for, send_from_directory
import os,time,datetime
import  random
import mysql.connector

app = Flask(__name__)
numberOfQuestions = 5
qns = {
    "Pytania zamknięte": [
                ["s1p1","Nadawanie cech ludzkim bóstwom, zwierzętom i przedmiotom w sztuce to:",["Antropomorfizm","Abstrakcja","Antropogeneza","Ornamentowanie"],"Antropomorfizm"],
                ["s1p2","Abstrakcyjne dzieło sztuki to takie, które:",["przedstawia rzeczywistość, czarne plamy","przedstawia barwne plamy, linie, płaszczyzny, nie przedstawia rzeczywistości","nie przedstawia barw (pochodna nazwa od szkicu)","jest nudne, monotonne"],"przedstawia barwne plamy, linie, płaszczyzny, nie przedstawia rzeczywistości"],
                ["s1p3","Absydą nazwiemy:",["technikę malarską z użyciem farb temperowych","rodzaj rzeźby, przedstawiającej motywy rycerskie","zewnętrze architektoniczne w kształcie przybudówki, na planie koła, zwieńczone ćwierćkopułą","wnętrze architektoniczne w kształcie przybudówki, na planie półkola, zwieńczone półkopułą"],"wnętrze architektoniczne w kształcie przybudówki, na planie półkola, zwieńczone półkopułą"],
                ["s1p4","Najwyższa część ściany o ozdobnym charakterze znajdująca się nad gzymsem i zasłaniająca dach, nazywana jest:",["Attyką","Antarktyką","Bazyliką","Deformacją"],"Attyką"],
                ["s1p5","Bauhaus to:",["uczelnia artystyczna powstała w 1919 roku w Katowicach","uczelnia artystyczna powstała w 2000 roku w Warszawie","uczelnia artystyczna powstała w 1919 roku w Weimarze","ciekawy rodzaj dekorowania domów, od zewnątrz z wykorzystaniem betonu"],"uczelnia artystyczna powstała w 1919 roku w Weimarze"]
                ["s1p6","Podstawa kolumny, bądź filaru, to:",["baza","werniks","łuk","pilaster"],"baza"]
                ["s1p7","Podstawą rzeźby, budowli lub innych elementów architektonicznych nazywamy:",["Filarem","Cokołem","Frotażem","Freskiem"],"Cokołem"]
                ["s1p8","Chryzelefantyna, to:",["technika rzeźbiarska w nowożytności, która wykorzystywała kość słoniową i złoto oraz inne drogie materiały ","technika malarska w starożytności, która wykorzystywała farby z drobinami złota","technika rzeźbiarska w starożytności, która wykorzystywała ubogie materiały ","technika rzeźbiarska w starożytności, która wykorzystywała kość słoniową i złoto oraz inne drogie materiały "],"technika rzeźbiarska w starożytności, która wykorzystywała kość słoniową i złoto oraz inne drogie materiały "]
                ["s1p9","Dagerotypia, to najstarsza",["technika otrzymywania obrazu fotograficznego na posrebrzanej płytce pokrytej jodkiem srebra i odbijanej na szkle lub metalowej płytce, później także papierze. ","technika otrzymywania obrazu na pozłacanej płytce pokrytej jodkiem srebra i odbijanej na pleksi lub kamiennej płytce, później także na ścianie. ","technika malarska, wykorzystująca światło słoneczne","(nie ma poprawnej odpowiedzi)"],"technika otrzymywania obrazu fotograficznego na posrebrzanej płytce pokrytej jodkiem srebra i odbijanej na szkle lub metalowej płytce, później także papierze. "]
                ["s1p10","Ekspresja, to:",["sposób parzenia herbaty ekspresowej.","środki plastyczne, za pomocą których artysta wyraża swoje emocje, przeżycia. ","środki plastyczne, za pomocą których artysta nie wyraża swoich emocji, przeżyć. ","szybko namalowany obraz z wykorzystaniem farb akwarelowych"],"środki plastyczne, za pomocą których artysta wyraża swoje emocje, przeżycia. "]
                ["s1p11","Elewacją nazywamy:",["zewnętrzną ścianę budynku.","wewnętrzną ścianę budynku.","kładzenie płytek na podłodze w kuchni","malowanie ścian farbą matującą"],"zewnętrzną ścianę budynku."]
                ["s1p12","Działanie artystyczne polegające na stworzeniu sytuacji przestrzennej wokół widzów środkami plastycznymi, na przykład elementami scenografii, nazywamy:",["Freskiem","Environment'em","Iluminacją sceniczną","Uprzestrzennieniem"],"Environment'em"]
                ["s1p13","Ściana budowli z głównym wejściem, często wyróżniona poprzez zdobienie, to:",["Gzyms","Łuk","Impast","Fasada"],"Fasada"]
                ["s1p14","Filar, to:",["pionowy element architektoniczny, będący podporą lub pełniący funkcje ozdobną, o przekroju prostokątnym. ","poziomy element architektoniczny, będący podporą lub pełniący funkcje ozdobną, o przekroju prostokątnym. ","pionowy element architektoniczny, będący podporą lub pełniący funkcje ozdobną, o przekroju okrągłym. ","pionowy element architektoniczny, będący podporą lub pełniący funkcje ozdobną, o przekroju trójkątnym. "],"pionowy element architektoniczny, będący podporą lub pełniący funkcje ozdobną, o przekroju prostokątnym. "]
                ["s1p15","Fresk, to",["technika malarstwa ściennego, w której gips nanosi się na fragmenty mokrego tynku.","technika malarstwa ściennego, w której farbę nanosi się na wyschnięty tynk.","technika malarstwa ściennego, w której farbę nanosi się na fragmenty mokrego tynku.","technika rzeźbiarstwa ściennego, w której farbę nanosi się na fragmenty mokrego tynku."],"technika malarstwa ściennego, w której farbę nanosi się na fragmenty mokrego tynku."]
                ["s1p16","Z języka francuskiego - frottage, to:",["sposób otrzymywania rysunku poprzez pocieranie ołówkiem lub kredką papieru nałożonego na powierzchni o zróżnicowanej fakturze. ","sposób otrzymywania rysunku poprzez pocieranie ołówkiem lub kredką papieru nałożonego na powierzchni o niezróżnicowanej fakturze. ","otrzymanie obrazu poprzez chlapanie farbą o kontrastowym kolorze","nie istnieje coś takiego jak frotaż"],"sposób otrzymywania rysunku poprzez pocieranie ołówkiem lub kredką papieru nałożonego na powierzchni o zróżnicowanej fakturze. "]
                ["s1p17","Dekoracyjny pas poziomy, umieszczony w górnej części ściany, zawierający motywy dekoracyjne i ornamentalne, to:",["Ryza","Kapitel","Fryz","Absyda"],"Fryz"]
                ["s1p18","Gzyms, to:",["pionowa linia lub wysunięty pas na ścianie budynku.","pozioma linia lub wysunięty pas na ścianie budynku oddzielający kolejne kondygnacje.","kolumna z wieloma ornamentami o tematyce religijnej","rodzaj okna wykonanego z wielobarwnego szkła"],"pozioma linia lub wysunięty pas na ścianie budynku oddzielający kolejne kondygnacje."]
                ["s1p19","Iluminacja w sztukach plastycznych, to:",["duża, zwykła ilustracja ręcznie malowana","mała, zwykła ilustracja ręcznie malowana","miniaturowa ilustracja ręcznie malowana w księgach rękopiśmiennych","wielka ilustracja ręcznie malowana w księgach rękopiśmiennych. "],"miniaturowa ilustracja ręcznie malowana w księgach rękopiśmiennych"]
                ["s1p20","Sposób malowania, pozwalający zaakcentować trójwymiarowość w obrazie, to:",["Kontrast","Technika 3D","Iluzjonizm","Wielo-perspektywność"],"Iluzjonizm"]
                ["s1p21","Impast, to:",["sposób malowania rzadką farbą za pomocą pędzla","sposób malowania gęstą farbą za pomocą pędzla lub szpachelki","sposób rzeźbienia w niezastygniętym gipsie za pomocą szpachelki","sposób rzeźbienia w gipsie za pomocą dłut"],"sposób malowania gęstą farbą za pomocą pędzla lub szpachelki"]
                ["s1p22","Inicjał w plastyce, to:",["pierwsza litera imienia","ozdobna litera rozpoczynająca księgę lub jej rozdział, wyróżniająca się wielkością i kształtem. ","nieozdobna litera rozpoczynająca księgę lub jej rozdział, wyróżniająca się małą wielkością i kształtem. ","obrazek przedstawiający przedmiot, bądź istotę, której nazwa rozpoczyna się na pierwszą literę imienia artysty"],"ozdobna litera rozpoczynająca księgę lub jej rozdział, wyróżniająca się wielkością i kształtem. "]
                ["s1p23","Krąg zbudowany z ustawionych pionowo kamieni, często wokół miejsca kultu to:",["Święty Krąg Kamienny","Kromlech","Okrąg kamieni kultu","Krzemlech"],"Kromlech"]
                ["s1p24","Kapitel, to:",["górna, ozdobna część kolumny","dolna, nieozdobna część kolumny","środkowa, ozdobna część kolumny","świetnie udekorowana cała kolumna"],"górna, ozdobna część kolumny"]
                ["s1p25","Katedra, to:",["mało istotny kościół w diecezji","inaczej kaplica cmentarna","zwykły kościół umiejscowiony w ubogiej wsi ","główny kościół w diecezji"],"główny kościół w diecezji"]
                ["s1p26","Kolumnada, to:",["inaczej kolumna","rząd kolumn podtrzymujący arkady lub belkowanie","ozdobna część kolumny","element architektoniczny w zakończeniach okien i drzwi"],"rząd kolumn podtrzymujący arkady lub belkowanie"]
                ["s1p27","Kopuła, to:",["wewnętrzna część budowli","sklepienie czaszy wzniesione na planie pobocznym","sklepienie koliste czaszy wzniesione na planie centralnym","sklepienie półkoliste czaszy wzniesione na planie centralnym"],"sklepienie półkoliste czaszy wzniesione na planie centralnym"]
                ["s1p28","Nakładanie cienkiej warstwy przezroczystej barwy w celu uzyskania odcieni i waloru poszczególnych barw, to:",["Laminacja","Laserunek","Lakierowanie","Laserowanie"],"Laserunek"]
                ["s1p29","Łuk, to element architektoniczny w zakończeniach okien i drzwi, portalach, arkadach i absydach, przyjmujący różne kształty w zależności od stylu - na przykład półkolisty łuk NIE występował:",["w antyku rzymskim","w stylu romańskim","w stylu renesansowym","w gotyku"],"w stylu renesansowym"]
                ["s1p30","Zbiór mitów opowiadanych w danej społeczności lub literacko uporządkowany zbiór opowieści o bóstwach i istotach nadprzyrodzonych, a także nauka zajmująca się zbieraniem, analizą, klasyfikacją i interpretacją mitów, to:",["Mitologia","Mitoznawstwo","Filologia mitologiczna","Filozofia mityczna"],"Mitologia"]
                ["s1p31","Maswerk, to element dekoracji architektonicznej o ażurowej formie, kuty w kamieniu lub rzeźbiony w drewnie. Należy on do stylu:",["Romańskiego","Renesansowego","Rzymskiego","Gotyckiego"],"Gotyckiego"]
                ["s1p32","Mozaika, to technika plastyczna należąca do ___ , która polega na uzyskiwaniu obrazu poprzez układanie drobnych, szlifowanych kamyczków lub szkiełek, także ceramicznych. W lukę należy wpisać:",["rysunku","malarstwa","rzeźby","grafiki artystycznej"],"malarstwa"]
                ["s1p33","Ornament, to:",["motyw ozdobny, stosowany tylko w architekturze","motyw ozdobny, stosowany w architekturze i innych dziedzinach plastycznych.","motyw ozdobny, stosowany tylko w malarstwie","motyw ozdobny, stosowany tylko w rzeźbie"],"motyw ozdobny, stosowany w architekturze i innych dziedzinach plastycznych."]
                ["s1p34","Perspektywą nazywamy:",["sposób przedstawienia trójwymiarowych obiektów i przestrzeni nie na płaszczyźnie.","sposób przedstawienia jednowymiarowych obiektów i przestrzeni na płaszczyźnie.","sposób przedstawienia dwuwymiarowych obiektów i przestrzeni na płaszczyźnie.","sposób przedstawienia trójwymiarowych obiektów i przestrzeni na płaszczyźnie."],"sposób przedstawienia trójwymiarowych obiektów i przestrzeni na płaszczyźnie."]
                ["s1p35","Polichromia, to ___ dekoracja ścian budowli, rzeźb i przedmiotów użytkowych. W lukę należy wstawić:",["czarno-biała","wielobarwna","jednobarwna","bezbarwna"],"wielobarwna"]
                ["s1p36","Portyk, to:",["przedsionek budynku nieprzykryty dwuspadowym dachem, niewspartym na kolumnach. ","przedsionek budynku przykryty dwuspadowym dachem, wspartym na kolumnach. ","inaczej portal","inaczej parapet "],"przedsionek budynku przykryty dwuspadowym dachem, wspartym na kolumnach. "]
                ["s1p37","Politeizmem nazwiemy:",["wiarę w jednego boga","kult ku czci władcy","wiarę w wielu bogów, bóstw itp.","(nie ma poprawnej odpowiedzi)"],"wiarę w wielu bogów, bóstw itp."]
                ["s1p38","W świątyniach to część przeznaczona dla duchowieństwa, zawierająca ołtarz główny, usytuowany na przedłużeniu nawy głównej; inaczej chór. W opisie jest mowa o:",["prezbiterium","prozbiterium","prazbiterium","rozecie"],"prezbiterium"]
                ["s1p39","___, to okrągły motyw ozdobny najczęściej w układzie symetrycznym, wieloosiowym, przypominającym różę, wypełniającym okno; może być wypełniona witrażem. W lukę należy wpisać:",["Witraż wielobarwny","Rozetę","Okno","Szklaną balustradę"],"Rozetę"]
                ["s1p40","Inaczej nazywane jako sufit. Przybiera różne formy: kolebkowe lub krzyżowe. Jest to:",["Ściana","Sklepienie","Podłoga","Werniks"],"Sklepienie"]
                ["s1p41","Symetria, to:",["układ, w którym elementy leżące po obu stronach osi symetrii są różne.","układ, w którym elementy leżące po obu stronach osi symetrii są takie same lub bardzo podobne.","sztuka przedstawiania obrazów o tematyce sakralnej","inaczej asymetria"],"układ, w którym elementy leżące po obu stronach osi symetrii są takie same lub bardzo podobne."]
                ],
    "Pytania Prawda/Fałsz": [
                ["s2p1","W architekturze łuk wsparty na kolumnach lub filarach, występujący pojedynczo lub w ciągach, to arkada.",["Prawda","Fałsz"],"Prawda"],
                ["s2p2","Bazylika, to budowla na planie trójkąta o nieparzystej liczbie naw, z których główna jest niższa od bocznych.",["Prawda","Fałsz"],"Fałsz"],
                ["s2p3","Deformacja, to celowe zniekształcenie stosowane w sztuce dla podniesienia warstwy emocjonalnej.",["Prawda","Fałsz"],"Prawda"],
                ["s2p4","Faktura, to budowa powierzchni dzieła plastycznego.",["Prawda","Fałsz"],"Prawda"],
                ["s2p5","W sztukach plastycznych, hełmem nazywamy zwieńczenie wieży budowli, przyjmujące różnorodne kształty, w kolejnych epokach lub stylach architektonicznych.",["Prawda","Fałsz"],"Prawda"]
                ["s2p6","Sposoby przedstawiania i tematy, które nie zmieniały się przez 2000 lat trwania cywilizacji starożytnego Egiptu, to kanon.",["Prawda","Fałsz"],"Prawda"]
                ["s2p7","Kompozycja, to układ elementów na płaszczyźnie lub w przestrzeni.",["Prawda","Fałsz"],"Prawda"]
                ["s2p8","Kontrast, to zestawienie barw lub zjawisk o charakterze identycznym, które się pokrywają.",["Prawda","Fałsz"],"Fałsz"]
                ["s2p9","Kontur, to linia wyznaczająca granice płaszczyzny.",["Prawda","Fałsz"],"Prawda"]
                ["s2p10","Odezwa lub deklaracja programowa partii, organizacji lub grupy artystycznej, to manifest.",["Prawda","Fałsz"],"Prawda"]
                ["s2p11","Modelunek, to wydobywanie kształtu przedmiotu i jego bryły za pomocą waloru i światłocienia.",["Prawda","Fałsz"],"Prawda"]
                ["s2p12","Nawa, to część budowli sakralnej; pomieszczenie oddzielone od innych arkadami, ścianami lub kolumnami, wyróżniamy nawy główne, boczne i poprzeczne. Jest to:",["Prawda","Fałsz"],"Prawda"]
                ["s2p13","Pilaster, to łaski filar nieprzylegający do ściany budynku.",["Prawda","Fałsz"],"Fałsz"]
                ["s2p14","Portal, to ozdobne obramienie drzwi, składające się z otworu drzwiowego, tympanonu, przylegających kolumienek i dekoracji rzeźbiarskich.",["Prawda","Fałsz"],"Prawda"]
                ["s2p15","Werniks, to nieprzezroczysta płynna substancja żywiczna, służąca do powlekania powierzchni malowidła po jego wyschnięciu.",["Prawda","Fałsz"],"Fałsz"]
                ]

}

resultdatabase = mysql.connector.connect(
  host="mysql54.mydevil.net",
  user="m1086_admin",
  password="q29ivxIJFyNw95uONBfK",
  database="m1086_quiz"
)

dbcursor = resultdatabase.cursor()

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
    
@app.route('/ranking')
def ranking():
    dbcursor.execute("SELECT * FROM results ORDER BY `points` DESC")
    data = dbcursor.fetchall()
    return render_template('ranking.html', data=data)

@app.route("/result", methods=["POST"])
def result():
    sql = "INSERT INTO results (name, surname, points) VALUES (%s, %s, %s)"
    val = (request.json["name"], request.json['surname'], request.json['result'])
    dbcursor.execute(sql, val)
    resultdatabase.commit()
    print("done")
    return "done"


if __name__ == '__main__':
      app.run(debug=True)
