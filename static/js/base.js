$(document).ready(function () {
  // Detail View Like (AJAX)
  $(document).on("click", "#detail-view-like", function () {
    var pk = $(this).data("id");
    var csrfToken = $(this).data("csrf-token");
    $.ajax({
      type: "POST",
      url: $(this).data("href"),
      headers: { "X-CSRFToken": csrfToken },
      data: { blog_id: pk },
      success: function (data) {
        $("#blog_" + pk + "_detail_reaction_section").html(data);
      },
    });
  });

  // List View Like (AJAX)
  $(document).on("click", ".blog-like-section", function () {
    var pk = $(this).data("id");
    var csrfToken = $(this).data("csrf-token");
    $.ajax({
      type: "POST",
      url: $(this).data("href"),
      headers: { "X-CSRFToken": csrfToken },
      data: { blog_id: pk },
      success: function (data) {
        $("#blog_" + pk + "_list_item_reaction_section").html(data);
      },
    });
  });
});

// Shared Share Logic
$(document).on("click", ".share-btn a", function (e) {
  e.preventDefault();
  shareBlogPost($(this).data("title"), $(this).data("url"));
});

const addBlogContainer = document.getElementById("text-field-container");

if (addBlogContainer) {
  addBlogContainer.addEventListener("click", function () {
    document.getElementById("add-blog-link").click();
  });
}

window.addEventListener("resize", changeCommentFieldText);
const commentFieldText = document.getElementsByClassName("comment-text-field");
function changeCommentFieldText() {
  if (screen.width <= 390) {
    for (let i = 0; i < commentFieldText.length; i++) {
      commentFieldText[i].innerText = "Comment here...";
    }
  } else {
    for (let i = 0; i < commentFieldText.length; i++) {
      commentFieldText[i].innerText = "Write your comment here ...";
    }
  }
}

function submitCommentForm(formObject) {
  const form = $(formObject);
  const blog_pk = form.data("id");
  $.ajax({
    type: "POST",
    url: form.data("href"),
    data: form.serialize(),
    success: function (data) {
      const section = $("#comment-section-" + blog_pk);
      if (section.data("has-comments") === true) {
        section.prepend(data);
      } else {
        section.html(data).data("has-comments", true);
      }
      form.trigger("reset"); // Clear the box after posting
    },
  });
  return false;
}

function shareBlogPost(title, url) {
  if (navigator.share) {
    navigator.share({ title: title, url: url }).catch(console.error);
  } else {
    navigator.clipboard.writeText(url).then(() => alert("Link copied!"));
  }
}