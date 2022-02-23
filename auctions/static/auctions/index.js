$('#postComment').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })


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

function placeBid(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText)
            respObj = JSON.parse(this.responseText)
            
            // sending a message to the user upon bidding.
            message = document.getElementById('bidMessage') || document.createElement('div')
            if (message.id != 'bidMessage') {
                message.id = 'bidMessage';
                message.innerText = respObj.bidMessage
                document.querySelector('button[name="submit"]').parentNode.append(message)
            }
            message.innerText = respObj.bidMessage
                if (this.response.winningBid){
                    document.querySelector('input[name="bid"]').value = parseFloat(respObj.winningBid)
                }
            }
        }
    
    xhttp.open('POST', 'bid', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('X-CSRFToken', csrftoken );
    
    // get the hidden input field to retrieve the auction_id
    let auction_id = document.querySelector('input[name="auction_id"]').value;
    let bid = parseFloat(document.querySelector('input[name="bid"]').value)
    
    xhttp.send(`auction_id=${auction_id}&bid=${bid}`);
}

function comment(event){
    let comment = document.getElementById('comment').value;
    if (comment === '') return;
    
    // get the hidden input field to retrieve the auction_id
    let auction_id = parseInt(document.querySelector('input[name="auction_id"]').value);
    // let commentDiv = event.target.parentNode.nextElementSibling.firstElementChild;
    let commentGroup = document.getElementById('commentGroup');
    let firstComment = commentGroup.firstElementChild.firstElementChild.nextElementSibling.firstElementChild;

    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200){
                respObj = JSON.parse(this.responseText)
                if (respObj.comment === 'valid'){              
                    if (firstComment.innerText === "There are no comments"){
                        firstComment.innerText = comment
                    } else {
                    let div = document.createElement('div');
                    div.className="card my-2 w-100"
                    div.innerHTML = `<div class="card-header">Be the first to comment</div>
                                        <div class="comment card-body my-2">
                                        <p class="card-text">${comment}</p>
                                        <h6 class="comment card-subtitle">${new Date().toDateString() }</h6>
                                    </div>`
                    commentGroup.insertBefore(div, commentGroup.firstElementChild)
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