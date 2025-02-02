$(document).ready(function() {
  $(document).on('click', '#detail-view-like', function() {
    let nextHref = window.location.href;
    window.location.href = "/accounts/login/?next=" + nextHref + "#detail-view-like";
  });
});

// like functionality for list view
$(document).ready(function() {
  $(document).on('click', '.blog-like-section', function() {
    let pk = $(this).data('id');
    let nextHref = window.location.href;    
    let blogReactionId = "#blog_" + pk + "_list_item_reaction_section";
    window.location.href = "/accounts/login/?next=" + nextHref + blogReactionId;
  });
});


const addBlogContainer = document.getElementById("text-field-container");

addBlogContainer.addEventListener('click', function() {
    let nextHref = window.location.href;
    window.location.href = "/accounts/login/?next=" + nextHref;
});



window.addEventListener("resize", changeCommentFieldText);
const commentFieldText = document.getElementsByClassName('comment-text-field');
function changeCommentFieldText() {
    if (screen.width <= 390){
        for (let i = 0; i < commentFieldText.length; i++){
            commentFieldText[i].innerText = "Comment here...";
        }
    } else {
        for (let i = 0; i < commentFieldText.length; i++){
            commentFieldText[i].innerText = "Write your comment here ...";
        }
    }
}


function submitCommentForm(formObject){
    let nextHref = window.location.href;
    window.location.href = "/accounts/login/?next=" + nextHref;
}


document.addEventListener('DOMContentLoaded', function() {
    const editCommentModal = document.getElementById('editCommentModal');

    if (editCommentModal) {
        let nextHref = window.location.href;
        window.location.href = "/accounts/login/?next=" + nextHref;
    }
});

function submitLike(commentLikeButtonObject) {
    let nextHref = window.location.href;
    window.location.href = "/accounts/login/?next=" + nextHref;
}

$(document).ready(function() {
    $('.no-scrollbars').on('keyup keypress', function() {
        $(this).height(0);
        $(this).height(this.scrollHeight);
    });
});
