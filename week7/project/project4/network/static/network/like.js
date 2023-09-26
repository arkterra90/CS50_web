document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.post-like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', like);
    });

});



// Function to allow user to like or unlike a post.
function like(event) {

    event.preventDefault();

    // event.target gets the unique values of the post being liked.
    const postElement = event.target;

    const postId = postElement.getAttribute('data-post-id');
    const userId = postElement.getAttribute('data-user-id');

    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            postId: postId,
            userId: userId
        })
    })
        // Takes responce and alters button html accordingly.
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if (result.success === 'post liked') {
                postElement.textContent = 'Unlike'; 
            } else {
                if (result.success === 'post unliked') {
                    postElement.textContent = 'Like'; 
                }
            }
        });
 
        // Send AJAX call to likeCount to update the post like count
        // and then update the like count on UI.
        fetch('/likeCount', {
            method: 'POST',
            body: JSON.stringify({
                postId: postId,
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result);
        
                // Updates the post like count in the HTML element
                const postLikeCountElement = document.querySelector(`#postLikeCount-${postId}`);
                if (postLikeCountElement) {
                    postLikeCountElement.textContent = result.likeCount;
                }
            });
}