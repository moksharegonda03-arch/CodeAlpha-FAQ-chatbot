function sendMessage(){

let msg=document.getElementById("message").value;

document.getElementById("chat").innerHTML += 
"<p><b>You:</b> "+msg+"</p>";

fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:msg
})
})

.then(response=>response.json())

.then(data=>{

document.getElementById("chat").innerHTML +=
"<p><b>Bot:</b> "+data.reply+"</p>";

});

}


function startVoice(){

let recognition = new webkitSpeechRecognition();

recognition.lang="en-US";

recognition.start();


recognition.onresult=function(event){

document.getElementById("message").value =
event.results[0][0].transcript;

}

}