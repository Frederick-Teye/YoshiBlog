$(document).ready(function() {
  function handleDetailViewLike() {
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
  }

  function handleListViewLike() {
    $(document).on('click', '.blog-like-section', function() {
      var $this = $(this);
      var pk = $this.data('id');
      var csrfToken = $this.data('csrf-token');
      let urlRoute = $this.data('href');

      $.ajax({
        type: 'POST',
        url: urlRoute,
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
  }

  handleDetailViewLike();
  handleListViewLike();  
});


const addBlogContainer = document.getElementById("text-field-container");

if (addBlogContainer) {
  addBlogContainer.addEventListener('click', function() {
    document.getElementById('add-blog-link').click();
  });
}


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
  const form = $(formObject);
  let urlRoute = $(formObject).data("href");
  let blog_pk = $(formObject).data("id");

  $.ajax({
      type: 'POST',
      url: urlRoute,
      data: $(form).serialize(),

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

