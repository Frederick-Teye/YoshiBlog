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
}

function submitLike(commentLikeButtonObject) {
  let nextHref = window.location.href;
  let commentIdInDatabase = commentLikeButtonObject.getAttribute("data-id");
  let commentIdInHtml = "#comment-reaction-" + commentIdInDatabase;
  window.location.href = "/accounts/login/?next=" + nextHref + commentIdInHtml;
}

// Function to share the blog post
function shareBlogPost(title, url) {
  console.log("shareBlogPost called with title:", title, "url:", url);
  if (navigator.share) {
    console.log("Using navigator.share");
    navigator
      .share({
        title: title,
        url: url,
      })
      .then(() => {
        console.log("Share successful");
      })
      .catch((error) => {
        console.error("Share failed:", error);
      });
  } else {
    console.log("Navigator.share not available, trying clipboard");
    // Fallback: copy to clipboard
    navigator.clipboard
      .writeText(url)
      .then(function () {
        console.log("Link copied to clipboard");
        alert("Link copied to clipboard: " + url);
      })
      .catch(function (err) {
        console.error("Failed to copy:", err);
        // Fallback: open a new window or something
        console.log("Opening mailto");
        window.open(
          "mailto:?subject=" +
            encodeURIComponent(title) +
            "&body=" +
            encodeURIComponent(url),
        );
      });
  }
}
