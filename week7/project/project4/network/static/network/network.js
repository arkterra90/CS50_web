document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'followButton') {
        follow(event);
    }
});

function follow(event) {
    {
        event.preventDefault();
    

    const user_id = document.querySelector('#user_id').value;
    const ifFollower = document.querySelector('#followButton').textContent.trim() === 'Follow Me';
    const followButton = document.querySelector('#followButton');

    console.log(user_id, ifFollower)
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id,
            ifFollower: ifFollower
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            // Implement inner html change of button to reflect follow state.
            if (result.success === 'New Follow Created') {
                followButton.textContent = 'Unfollow Me';
            } else if (result.success === 'Already a follower') {
                followButton.textContent = 'Follow Me';
            }
        });

    };
}
