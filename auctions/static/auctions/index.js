function addToWatchList(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            respObj = JSON.parse(this.responseText)
            
            document.getElementById('watchCount').innerText = respObj.total;
        }
    }
    xhttp.open('POST', 'watchCount', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('X-CSRFToken', csrftoken );
    
    let auction_id = parseInt(document.querySelector('input[name="auction_id"]').value);
    
    xhttp.send(auction_id);
}