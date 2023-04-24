// function to close the comment box
function closeCommentBox() {
    var commentBox = document.getElementById("overlay");
    commentBox.classList.add("hidden");
}

// Close the comment box if the user clicks outside of it
window.onclick = function(event) {
    var commentBox = document.getElementById("overlay");
    if (event.target == commentBox) {
        commentBox.classList.add("hidden");
    }
}

// function that will resize the textarea
function resize(element){
    element.style.height = "auto";
    element.style.height = element.scrollHeight + "px";

}
// function that will preview the images
function previewImages(id,image) {
    const preview = document.querySelector(`#${id}`);
    const input = document.querySelector(`#${image}`);
    const files = document.querySelector(`#${image}`).files;
    preview.innerHTML = "";
    if (files && files.length > 0) {
        const file = files[0]; // assuming only one file is selected
        if (file.type.match(/^image\//)) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const image = new Image();
            image.title = file.name;
            image.src = event.target.result;
            image.classList.add("max-w-xs", "max-h-xs", "shadow-lg");
            const removeButton = document.createElement("button");
            removeButton.innerText = "X";
            removeButton.classList.add("absolute", "top-1", "left-1","px-2" ,"text-white", "bg-red-400", "rounded-full", "hover:bg-red-600", "focus:outline-none","transition", "duration-300", "ease-in-out", "transform", "hover:-translate-y-1", "hover:scale-110", "active:scale-95", "active:translate-y-0");
            removeButton.onclick = function() {
                preview.removeChild(image);
                preview.removeChild(removeButton);
                input.value = "";
            };
            preview.appendChild(image);
            preview.appendChild(removeButton);
        };
        reader.readAsDataURL(file);
        } else {
        alert("Please select a valid image file.");
        }
    }
}

// function that will like the post onclcik
function like(element, id){
    //send a request to the server
    fetch(`/like/${id}`)
    .then(response => {
        if (response.ok) {
            // Request succeeded, handle the response
            response.json();
            //get the heart of the div that called the function
            const heart = element.querySelector('i');
            //change the color of the heart of the div that called the function
            element.classList.toggle("text-rose-400");
            heart.classList.toggle("fa-regular");
            heart.classList.toggle("fa-solid");
            //get the number of likes
            var likes = element.querySelector('span');
            //change the number of likes
            if(element.classList.contains("text-rose-400")){
                likes.innerHTML = parseInt(likes.innerHTML) + 1;
            }else{
                likes.innerHTML = parseInt(likes.innerHTML) - 1;
            }
        } 
        else {
        // Request failed, throw an error
        throw new Error("Error");
        }
    })
    .catch(error => {
        return alert("Please log in first");
    });
}
// function to repost the post
function repost(element, id){
    //send a request to the server
    fetch(`/repost/${id}`)
    .then(response => {
        if (response.ok) {
            // Request succeeded, handle the response
            response.json();
            //get the repost of the div that called the function
            const repost = element.querySelector('i');
            //change the color of the repost of the div that called the function
            element.classList.toggle("text-emerald-500");
            //get the number of reposts
            var reposts = element.querySelector('span');
            //change the number of reposts
            if(element.classList.contains("text-emerald-500")){
                reposts.innerHTML = parseInt(reposts.innerHTML) + 1;
            }else{
                reposts.innerHTML = parseInt(reposts.innerHTML) - 1;
            }
        } 
        else {
        // Request failed, throw an error
        throw new Error("Error");
        }
    })
    .catch(error => {
        return alert("Please log in first");
    });
}
// function to delete the post
function deleting(post_id){
    fetch(`/delete/${post_id}`)
    .then(response => {
        if (response.ok) {
            // Request succeeded, handle the response
            return response.json();
        }
        else {
            // Request failed, throw an error
            throw new Error("Error");
        }
    })
    .then(data => {
        //get the post that called the function
        const post = document.querySelector(`#post${post_id}`);
        //remove the post
        post.remove();
        alert(data.message);
    })
    .catch(error => {
        return alert(error.message);
    });
}

// function to show options
function showOptions(element){
    //get the options of the div that called the function
    const options = element.querySelector('#optionsBox');
    //show the options
    options.classList.toggle("hidden");
    window.addEventListener('click', function(e) {
        // check if clicked element is outside of the options box
        if (!options.contains(e.target) && !element.contains(e.target)) {
            // hide the options box
            options.classList.add("hidden");
        }
    });
}
// function to show the edit box
function editing(post_id){
    const editBox = document.querySelector(`#editPost${post_id}`);
    const post = document.querySelector(`#post${post_id}`);
    editBox.classList.toggle("hidden");
    post.classList.toggle("hidden");
}

//function to bookmatk the post
function bookmark(element,post_id){
    fetch(`/bookmark/${post_id}`)
    .then (response =>{
        if (response.ok){
            // request succeded, handle the request
            return response.json();
        }
        else{
            // request failed, throw an Error
            throw new Error("Error");
        }
    })
    .then(data =>{
        alert(data.message);
        element.querySelector('i').classList.toggle("fa-regular");
        element.querySelector('i').classList.toggle("fa-solid");
    })
    .catch(error =>{
        return alert(error.message);
    });
}
// function to adjust the color of bookmark icon
function adjustBookmark(element){
    element.classList.toggle("text-blue-400");
    var bookmarks = element.querySelector('span');
    if(element.classList.contains("text-blue-400")){
        bookmarks.innerHTML = parseInt(bookmarks.innerHTML) + 1;
    }else{
        bookmarks.innerHTML = parseInt(bookmarks.innerHTML) - 1;
    }
}

// quick function to focus on the reply area
function reply(){
    document.getElementById('reply_area').focus();
}

// function to follow the user
function follow(element, username){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/profile/${username}`,{
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            // Request succeeded, handle the response
            response.json();
            window.location.reload();
        } 
        else {
        // Request failed, throw an error
        throw new Error("Error");
        }
    })
    .catch(error => {
        return alert("Please log in first");
    });
}

// function to edit profile
function edit_profile(){
    const editBox = document.querySelector('.edit_overlay');
    editBox.classList.toggle("hidden");
}