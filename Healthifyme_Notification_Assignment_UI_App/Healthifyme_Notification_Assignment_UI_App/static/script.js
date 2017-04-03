
function showInputs() {
    if (document.getElementById('notification').checked) {
        document.getElementById('ResponseText').innerHTML = ""
        document.getElementById('NotificationBlock').style.display = 'block';
        document.getElementById('NotificationIdBlock').style.display = 'none';
        document.getElementById('QueryBlock').style.display = 'none';
    }
    else if(document.getElementById('queryradiobutton').checked){
        document.getElementById('ResponseText').innerHTML = ""
        document.getElementById('NotificationBlock').style.display = 'none';
        document.getElementById('NotificationIdBlock').style.display = 'block';
        document.getElementById('QueryBlock').style.display = 'block';
    }
    else {
        document.getElementById('ResponseText').innerHTML = ""
        document.getElementById('NotificationBlock').style.display = 'block';
        document.getElementById('NotificationIdBlock').style.display = 'none';
        document.getElementById('QueryBlock').style.display = 'block';
    }
}

function makeRestRequest(){
    if (document.getElementById('notification').checked) {
        if(!validate('notification'))
            return;
        var url="http://127.0.0.1:8000/put_notification/"
        var data = {
          "header": document.getElementById('header').value,
          "content": document.getElementById('content').value,
          "image_url": document.getElementById('imgurl').value
        }
        sendAJAXRequest(url, data, "Created the Notification! The ID for further usage :- ");
        resetInput();
    }
    else if(document.getElementById('queryradiobutton').checked){
        if(!validate('query'))
            return;
        var url="http://127.0.0.1:8000/put_query/"
        var data = {
          "notification_id": document.getElementById('noteid').value,
          "query": document.getElementById('query').value,
          "timestamp": document.getElementById('timestamp').value
        }
        sendAJAXRequest(url, data, "Created the Query! The ID for further usage :- ");
        resetInput();
    }
    else {
        if(!validate('both'))
            return;
        var url="http://127.0.0.1:8000/put_notification/"
        var data = {
          "header": document.getElementById('header').value,
          "content": document.getElementById('content').value,
          "image_url": document.getElementById('imgurl').value
        }
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", url, true);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                document.getElementById('ResponseText').innerHTML = "Created the Notification! The ID for further usage :- " + response.id;
                var url="http://127.0.0.1:8000/put_query/"
                var data = {
                  "notification_id": response.id,
                  "query": document.getElementById('query').value,
                  "timestamp": document.getElementById('timestamp').value
                }
                sendAJAXRequest(url, data, "Created the Query! The ID for further usage :- ");
                resetInput();
                return;
            }
            else if(xhttp.readyState == 4 && (xhttp.status == 400 || xhttp.status == 404)){
                alert(xhttp.responseText);
                return;
            }
        }
        xhttp.send(JSON.stringify(data));
    }
}

function validate(input_selection){
    if(input_selection === 'notification'){
        header = document.getElementById('header').value
        if(header.length < 20 || header.length > 150){
            alert("Invalid Header length. Please check constraints.")
            return false;
        }
        content = document.getElementById('content').value
        if(content.length < 20 || content.length > 300){
            alert("Invalid Content length. Please check constraints.")
            return false;
        }
        imgurl = document.getElementById('imgurl').value
        if(!ValidURL(imgurl)){
            alert("Invalid Image URL. Please check constraints.")
            return false;
        }
    }
    else if(input_selection === 'query'){
        notificationId = document.getElementById('noteid').value
        if(!validateNumber(notificationId)){
            alert("Invalid Notification ID. Please check constraints.")
            return false;
        }
        query = document.getElementById('query').value
        if(query.length == 0){
            alert("Invalid Query. Please check constraints.")
            return false;
        }
        timestamp = document.getElementById('timestamp').value
        if(timestamp.length == 0){
            alert("Invalid Timestamp. Please check constraints.")
            return false;
        }
    }
    else{
        header = document.getElementById('header').value
        if(header.length < 20 || header.length > 150){
            alert("Invalid Header length. Please check constraints.")
            return false;
        }
        content = document.getElementById('content').value
        if(content.length < 20 || content.length > 300){
            alert("Invalid Content length. Please check constraints.")
            return false;
        }
        imgurl = document.getElementById('imgurl').value
        if(!ValidURL(imgurl)){
            alert("Invalid Image URL. Please check constraints.")
            return false;
        }
        query = document.getElementById('query').value
        if(query.length == 0){
            alert("Invalid Query. Please check constraints.")
            return false;
        }
        timestamp = document.getElementById('timestamp').value
        if(timestamp.length == 0){
            alert("Invalid Timestamp. Please check constraints.")
            return false;
        }
    }
    return true;
}

function ValidURL(str) {
   var a  = document.createElement('a');
   a.href = str;
   return (a.host && a.host != window.location.host);
}

function validateNumber(inputtxt)
{
    var numbers = /^[0-9]+$/;
    if(inputtxt.match(numbers))
        return true;
    return false;
}

function sendAJAXRequest(url, data, output_message){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var response = JSON.parse(xhttp.responseText);
            document.getElementById('ResponseText').innerHTML = output_message + response.id;
            return response.id;
        }
        else if(xhttp.readyState == 4 && (xhttp.status == 400 || xhttp.status == 404)){
            alert(xhttp.responseText);
            return -1;
        }
    }
    xhttp.send(JSON.stringify(data));
}

function resetInput(){
    document.getElementById('header').value = "";
    document.getElementById('content').value = "";
    document.getElementById('imgurl').value = "";
    document.getElementById('noteid').value = "";
    document.getElementById('query').value = "";
    document.getElementById('timestamp').value = "";
}