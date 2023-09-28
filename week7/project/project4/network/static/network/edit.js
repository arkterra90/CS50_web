// Javascript allows user to edit a post and then updates the contents of the text.
// Hides and displays a pre-populated textarea based on user clicking edit.
// When "Save" is clicked the post is updated in the Database Model
// and the new text is displayed for the user.

document.addEventListener('DOMContentLoaded', function() {
    // Adds an event listener to all "Edit" buttons with class "edit-button"
    const editButtons = document.querySelectorAll('.edit-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Finds the corresponding userPost and editPost divs
            const postId = event.target.getAttribute('data-post-id');
            const userPostDiv = document.querySelector(`#post-${postId} .userPost`);
            const editPostDiv = document.querySelector(`#post-${postId} .editPost`);

            // Toggles the visibility of userPost and editPost divs
            userPostDiv.style.display = userPostDiv.style.display === 'none' ? 'block' : 'none';
            editPostDiv.style.display = editPostDiv.style.display === 'none' ? 'block' : 'none';
        });
    });

    // Adds an event listener to all "Save" buttons with class "save-button"
    const saveButtons = document.querySelectorAll('.save-button');

    saveButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Finds the corresponding userPost and editPost divs
            const postId = event.target.getAttribute('data-post-id');
            const userPostDiv = document.querySelector(`#post-${postId} .userPost`);
            const editPostDiv = document.querySelector(`#post-${postId} .editPost`);
            const postTextArea = document.querySelector(`#postTextArea-${postId}`);
            const postText = postTextArea.value;
            console.log(postText);

            fetch('/editPost', {
                method: 'POST',
                body: JSON.stringify({
                    postId: postId,
                    postText: postText
                })
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })
            
                const postTextElement = document.querySelector(`#post-text-${postId}`);
                postTextElement.textContent = postText;
            // Toggles the visibility of userPost and editPost divs
            userPostDiv.style.display = userPostDiv.style.display === 'none' ? 'block' : 'none';
            editPostDiv.style.display = editPostDiv.style.display === 'none' ? 'block' : 'none';
        });
    });
});
