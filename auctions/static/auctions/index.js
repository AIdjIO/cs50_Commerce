function addToWatchList(id = null){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
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

function bid(event){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText)
            respObj = JSON.parse(this.responseText)
            
            // sending a message to the user upon bidding.
            message = document.getElementById('message') || document.createElement('div')
            if (message.id != 'message') {
                message.id = 'message';
                message.innerText = respObj.message
                document.querySelector('button[name="submit"]').parentNode.append(message)
            }
            message.innerText = respObj.message
            }
        }
    
    xhttp.open('POST', 'bid', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('X-CSRFToken', csrftoken );
    
    // get the hidden input field to retrieve the auction_id
    let auction_id = document.querySelector('input[name="auction_id"]').value;
    let bid = document.querySelector('input[name="bid"]').value
    
    xhttp.send(`auction_id=${auction_id}&bid=${bid}`);
}

function comment(event){
    let comment = document.querySelector('textarea').value;
    if (comment === '') return;
    
    // get the hidden input field to retrieve the auction_id
    let auction_id = parseInt(document.querySelector('input[name="auction_id"]').value);
    let commentDiv = event.target.parentNode.nextElementSibling.firstElementChild;

    console.log(commentDiv)
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200){
                respObj = JSON.parse(this.responseText)
                if (respObj.comment === 'valid'){              
                    if (commentDiv.innerText === "There are no comments"){
                        commentDiv.innerText = comment
                    } else {
                    let div = document.createElement('div');
                    div.className="comment"
                    div.innerText = comment
                    commentDiv.parentNode.insertBefore(div, commentDiv)
                    }
                }
            }
        }    
    xhttp.open('POST', 'comment', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('X-CSRFToken', csrftoken );
    
    data = `auction_id=${auction_id}&comment=${comment}`
    xhttp.send(data);
}