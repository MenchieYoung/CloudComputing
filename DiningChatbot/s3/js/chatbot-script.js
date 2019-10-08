var chatHistory = [];
var apigClient = apigClientFactory.newClient();
// var apigClient = apigClientFactory.newClient({
//   accessKey: '',
//   secretKey: '',
// });

function callChatbotLambda() {
  var inputText = document.getElementById('user-input-text').value.trim().toLowerCase();
  document.getElementById('user-input-text').value = "";

  if (inputText == "") {
    alert("Please enter some text");
    return false;
  } else {
    chatHistory.push("You: " + inputText);
    document.getElementById('chat-output').innerHTML = "";
    chatHistory.forEach((element) => {
      document.getElementById('chat-output').innerHTML += "<p>" + element + "</p>";
    });
    setTimeout(chatbotResponse, 500, inputText);
    return false;
  }
}

function chatbotResponse(inputText) {
  
  var params = {};
  var body = {
    "input": inputText
  };
  var additionalParams = {};

  apigClient.chatbotPost(params, body, additionalParams)
    .then((result) => {
      chatHistory.push("Bot: " + result.data.body);
      document.getElementById('chat-output').innerHTML = "";
      chatHistory.forEach((element) => {
        document.getElementById('chat-output').innerHTML += "<p>" + element + "</p>";
      });
    }).catch((err) =>{
      console.log(err);
    });
}









