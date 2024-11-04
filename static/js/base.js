const addBlogContainer = document.getElementById("text-field-container");

addBlogContainer.addEventListener('click', function() {
    document.getElementById('add-blog-link').click();
});


// Delete blog in blog list view
function deleteBlog(id){
     document.getElementById('delete-blog-link-'+id).click();
}