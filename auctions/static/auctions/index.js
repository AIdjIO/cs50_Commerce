function addToWatchList(id = null){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText)
            respObj = JSON.parse(this.responseText)
            // set the count in watchlist button
            document.getElementById('watchCount').innerText = respObj.total;


            // change the heart from solid or regular if listing in watchlist
            searchString = respObj.spanClass == 'far'? 'fas' : 'far';
            regexp = new RegExp(searchString, 'g')

            // replace class for heart icon from solid to regular and vice-versa
            // depending on whether the listing is added or removed from the watchlist
            let els = [].slice.apply(document.getElementsByClassName("fa-heart"));
            for (var i = 0; i < els.length; i++) {
                els[i].className = els[i].className.replace(regexp, respObj.spanClass);
            }
        }
    }
    xhttp.open('POST', 'updateWatchList', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('X-CSRFToken', csrftoken );
    
    // get the hidden input field to retrieve the auction_id
    let auction_id = parseInt(id) || parseInt(document.querySelector('input[name="auction_id"]').value);
    
    xhttp.send(auction_id);
}