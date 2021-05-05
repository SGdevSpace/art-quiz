var nextSectionId = "Pytania zamknięte",currentSectionId = "Pytania zamknięte";
var numberOfQns = 0.0,correct=0.0;
var section_ans =[];
$("#results").hide();
var resCorrect;
function finish(){
	checkAnswers();
	 $("#questions").hide();
	 $("#results").show();
	 	$("#result_text").text('Wyniki quizu');
		 $("#myCanvas").attr('data-value',"[{ value: "+(numberOfQns-correct)+", color: '#e35656', label: 'Błędne odpowiedzi' }, { value: "+correct+", color: '#5be356', label: 'Poprawne odpowiedzi' }]");
			   $("#results_table tbody").find("tr").remove();
		   $.each(section_ans,function(index,val){
		   $("#results_table tbody").append("<tr><td>"+val.section+"</td><td>"+val.sectionCorrect+"/"+val.sectionTotal+"</td></tr>");
		   });

	$(document).trigger("redraw.bs.charts");


	

var ctx = document.getElementById("myChart").getContext("2d");

var data = {
    labels: [
        "Błędne odpowiedzi",
        "Poprawne odpowiedzi"
    ],
    datasets: [
        {
            data: [(numberOfQns-correct), correct],
            backgroundColor: [
                "#e35656",
                "#5be356"
            ]
        }]
};
var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options:{
    	borderWidth:0,
    	lineWidth:0,
    	cutoutPercentage:80,
    	strokeColor:"#252830"
    }
});

}

function checkAnswers() {
	var sectionCorrect=0,sectionTotal=0;
	$("#questions_container .qns_rows").each(function(){
		
		var correct_ans= $(this).find("#ans").text();
		var selected_ans = $('input[name=qns_'+$(this).prop('id')+']:checked', $(this)).val()
		if(correct_ans==selected_ans){
			correct = correct+1;
			sectionCorrect=sectionCorrect+1;
			resCorrect = resCorrect + 1;
		}
		sectionTotal=sectionTotal+1;
		numberOfQns=numberOfQns+1;
	});
	section_ans.push({'section':currentSectionId,'sectionCorrect':sectionCorrect,'sectionTotal':sectionTotal});
}

function loadSection() {
    if (nextSectionId == "Pytania zamknięte") {
        $("#instructions").hide();
        $("#questions").show();
    }else{
    checkAnswers();
}

        $.ajax({
            url: "/getQuestions/",
            type: "POST",
            data: { "sectionId": nextSectionId },
            success: function(data) {
                showOptions(data);
                
            },
            error: function(data) {
                alert("Nie pobrano pytań z serwera | Kod błędu: ERR01");
            }
        });

    

}

function showOptions(data){
	currentSectionId=nextSectionId;
	nextSectionId = data.next;
	$("#questions_container").empty();
	$.each(data.qns,function(key,qns){
		var qns_div= $("#qns_sample").clone().prop('id',qns[0]);
		qns_div.find("#qns_title").text(qns[1]);
		qns_div.find("#ans").text(qns[3]);
		qns_div.find("#choice_list").empty();
		$.each(qns[2],function(index,val){
			qns_div.find("#choice_list").append("<li ><input type='radio' value='"+val+"' name='qns_"+qns[0]+"''>"+val+"</radio></li>");	
		});

		
		qns_div.show();

		$("#questions_container").append(qns_div);
	});
	if(nextSectionId=="Finish"){
			$("#next_btn").hide();
			$("#finish_btn").show();
		}else{

			$("#next_btn").show();
			$("#finish_btn").hide();
		}
}

var imie, nazwisko;
function getStudentData () {
	imie = document.getElementById("input-imie").value;
	nazwisko =  document.getElementById("input-nazwisko").value;
}

function insertStudentData() {
	var submitDate = new Date;
	document.getElementById("result_text").innerText = "Wyniki quizu dla ucznia " + imie + " " + nazwisko;
	document.getElementById("submit_date").innerText = "Data przesłania: " + submitDate.getFullYear()+'-'+(submitDate.getMonth()+1)+'-'+submitDate.getDate() + " "+ submitDate.getHours() + ":" + submitDate.getMinutes() + ":" + submitDate.getSeconds();

	var results = {
		'name': imie,
		'surname': nazwisko,
		'result': correct
		}
	$.ajax({
		url: "/result",
		type: 'POST',
		contentType: "application/json",
		data: JSON.stringify(results),
		})
		.done(function(result){
			console.log(result)
		})
}
