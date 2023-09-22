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

    console.log(postId, userId);

    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            postId: postId,
            userId: userId
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result.success === 'post liked') {
                postElement.textContent = 'Unlike'; 
            } else {
                if (result.success === 'post unliked') {
                    postElement.textContent = 'Like'; 
                }
            }
        });
    
}