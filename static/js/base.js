$(document).ready(function() {
  $(document).on('click', '#detail-view-like', function() {
    var pk = $(this).data('id');
    var csrfToken = $(this).data('csrf-token');

    $.ajax({
      type: 'POST',
      url: $(this).data('href'),
      headers: {
        'X-CSRFToken': csrfToken
      },
      data: {
        "blog_id": pk,
      },
      success: function(data) {
        var id = "#blog_" + pk + "_detail_reaction_section";
        $(id).html(data);
      },
      error: function(rs, e) {
        console.log(rs.responseText);
      },
    });
  });
});


// like functionality for list view
$(document).ready(function() {
  $(document).on('click', '.blog-like-section', function() {
    var $this = $(this);
    var pk = $this.data('id');
    var csrfToken = $this.data('csrf-token');

    $.ajax({
      type: 'POST',
      url: pk + '/list_like/',
      headers: {
        'X-CSRFToken': csrfToken
      },
      data: {
        "blog_id": pk,
      },
      success: function(data) {
        var id = "#blog_" + pk + "_list_item_reaction_section";
        $(id).html(data)
      },
      error: function(rs, e) {
        console.log(rs.responseText);
      },
    });
  });
});


const addBlogContainer = document.getElementById("text-field-container");

addBlogContainer.addEventListener('click', function() {
    document.getElementById('add-blog-link').click();
});


// Delete blog in blog list view
// function deleteBlog(id){
//      document.getElementById('delete-blog-link-'+id).click();
// }


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
  var form = $("#comment-input-box-" + blog_pk);
  alert(form.serialize());
  $.ajax({
      type: 'POST',
      url: 'new_comment/',
      data: form.serialize(),

      success: function(data) {
        var commentSection = $('#comment-section-' + blog_pk);
        // Get the value of the data-has-comments attribute
        var hasComments = commentSection.data('has-comments');

        // Check if there are comments
        if (hasComments === true) {
            commentSection.prepend(data);
        } else {
            hasComments = true;
            commentSection.html(data);
        }
      },
      error: function(rs, e) {
        console.log(rs.responseText);
      },
    });
}

