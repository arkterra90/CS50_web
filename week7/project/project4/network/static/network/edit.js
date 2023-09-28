document.addEventListener('DOMContentLoaded', function() {
    // Add an event listener to all "Edit" buttons with class "edit-button"
    const editButtons = document.querySelectorAll('.edit-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Find the corresponding userPost and editPost divs
            const postId = event.target.getAttribute('data-post-id');
            const userPostDiv = document.querySelector(`#post-${postId} .userPost`);
            const editPostDiv = document.querySelector(`#post-${postId} .editPost`);

            // Toggle the visibility of userPost and editPost divs
            userPostDiv.style.display = userPostDiv.style.display === 'none' ? 'block' : 'none';
            editPostDiv.style.display = editPostDiv.style.display === 'none' ? 'block' : 'none';
        });
    });

    // Add an event listener to all "Save" buttons with class "save-button"
    const saveButtons = document.querySelectorAll('.save-button');

    saveButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Find the corresponding userPost and editPost divs
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
            // Toggle the visibility of userPost and editPost divs
            userPostDiv.style.display = userPostDiv.style.display === 'none' ? 'block' : 'none';
            editPostDiv.style.display = editPostDiv.style.display === 'none' ? 'block' : 'none';
        });
    });
});
