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