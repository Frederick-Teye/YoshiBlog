document.addEventListener('DOMContentLoaded', function() {
    const editCommentModal = document.getElementById('editCommentModal');

    if (editCommentModal) {
        editCommentModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const hrefAttributeValue = button.getAttribute('data-bs-href');

            fetch(hrefAttributeValue)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.text();
                })
                .then(data => {
                    document.getElementById("commentModelBody").innerHTML = data;
                })
                .catch(error => {
                    console.log('Error:', error);
                });
        });
    }
});

function submitLike(commentLikeButtonObject) {
    const likeButton = commentLikeButtonObject;
    const commentId = likeButton.getAttribute('data-id');
    const csrftoken = likeButton.getAttribute('data-csrf-token');
    const url = likeButton.getAttribute('data-href');

    fetch(url, {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not okay ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        document.getElementById("comment-reaction-" + commentId).innerHTML = data;
    })
    .catch(error => {
        console.log("Error: " + error);
    });

}

$(document).ready(function() {
    $('.no-scrollbars').on('keyup keypress', function() {
        $(this).height(0);
        $(this).height(this.scrollHeight);
    });
});