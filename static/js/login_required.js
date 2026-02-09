$(document).ready(function () {
  function handleDetailViewLike() {
    $(document).on("click", "#detail-view-like", function () {
      let nextHref = window.location.href;
      window.location.href =
        "/accounts/login/?next=" + nextHref + "#detail-view-like";
    });
  }

  function handleListViewLike() {
    $(".blog-like-section").click(function () {
      let pk = $(this).data("id");
      let nextHref = window.location.href;
      let blogReactionId = "#blog_" + pk + "_list_item_reaction_section";
      window.location.href =
        "/accounts/login/?next=" + nextHref + blogReactionId;
    });
  }

  function autoExpandTextArea() {
    $(".no-scrollbars").on("keyup keypress", function () {
      $(this).height(0);
      $(this).height(this.scrollHeight);
    });
  }

  handleDetailViewLike();
  handleListViewLike();
  autoExpandTextArea();
});

const addBlogContainer = document.getElementById("text-field-container");

if (addBlogContainer) {
  addBlogContainer.addEventListener("click", function () {
    let nextHref = window.location.href;
    window.location.href = "/accounts/login/?next=" + nextHref;
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
  let nextHref = window.location.href;
  let blog_pk = formObject.getAttribute("data-id");
  let formId = "#comment-input-box-" + blog_pk;
  window.location.href = "/accounts/login/?next=" + nextHref + formId;
  return false; // Prevent form submission
}

function submitLike(commentLikeButtonObject) {
  let nextHref = window.location.href;
  let commentIdInDatabase = commentLikeButtonObject.getAttribute("data-id");
  let commentIdInHtml = "#comment-reaction-" + commentIdInDatabase;
  window.location.href = "/accounts/login/?next=" + nextHref + commentIdInHtml;
}

// Function to share the blog post
function shareBlogPost(title, url) {
  if (navigator.share) {
    navigator
      .share({
        title: title,
        url: url,
      })
      .catch(console.error);
  } else {
    // Fallback: copy to clipboard
    navigator.clipboard
      .writeText(url)
      .then(function () {
        alert("Link copied to clipboard: " + url);
      })
      .catch(function (err) {
        console.error("Failed to copy:", err);
        // Fallback: open a new window or something
        window.open(
          "mailto:?subject=" +
            encodeURIComponent(title) +
            "&body=" +
            encodeURIComponent(url),
        );
      });
  }
}
