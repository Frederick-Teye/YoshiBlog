const addBlogContainer = document.getElementById("text-field-container");

addBlogContainer.addEventListener('click', function() {
    document.getElementById('add-blog-link').click();
});


// Delete blog in blog list view
function deleteBlog(id){
     document.getElementById('delete-blog-link-'+id).click();
}


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
