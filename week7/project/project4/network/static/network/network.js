document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'followButton') {
        follow(event);
    }
});

function follow(event) {
    console.log("Follow Button Logged");
}
