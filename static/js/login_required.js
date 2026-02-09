$(document).ready(function () {
  // 1. Handle clicking the Like button on Detail View
  $(document).on("click", "#detail-view-like", function () {
    const nextHref =
      window.location.pathname + window.location.search + "#detail-view-like";
    window.location.href =
      "/accounts/login/?next=" + encodeURIComponent(nextHref);
  });

  // 2. Handle clicking the Like button on List View
  $(document).on("click", ".blog-like-section", function () {
    const pk = $(this).data("id");
    // Anchor to the specific blog card
    const nextHref =
      window.location.pathname + window.location.search + "#blog-" + pk;
    window.location.href =
      "/accounts/login/?next=" + encodeURIComponent(nextHref);
  });

  // 3. Handle clicking the "What's on your mind?" box
  $(document).on("click", "#text-field-container", function () {
    const nextHref = "/blogs/new/";
    window.location.href =
      "/accounts/login/?next=" + encodeURIComponent(nextHref);
  });
});

// 4. Handle Comment Form Submission (Redirect to login)
function submitCommentForm(formObject) {
  const blog_pk = formObject.getAttribute("data-id");
  const nextHref =
    window.location.pathname +
    window.location.search +
    "#comment-input-box-" +
    blog_pk;
  window.location.href =
    "/accounts/login/?next=" + encodeURIComponent(nextHref);
  return false;
}

// 5. Handle Comment Like (Redirect to login)
function submitLike(commentLikeButtonObject) {
  const commentId = commentLikeButtonObject.getAttribute("data-id");
  const nextHref =
    window.location.pathname +
    window.location.search +
    "#comment-reaction-" +
    commentId;
  window.location.href =
    "/accounts/login/?next=" + encodeURIComponent(nextHref);
}

// 6. Share Function (Always works for everyone)
$(document).on("click", ".share-btn a", function (e) {
  e.preventDefault();
  const title = $(this).data("title");
  const url = $(this).data("url");
  shareBlogPost(title, url);
});

function shareBlogPost(title, url) {
  if (navigator.share) {
    navigator.share({ title: title, url: url }).catch(console.error);
  } else {
    navigator.clipboard
      .writeText(url)
      .then(function () {
        alert("Link copied to clipboard!");
      })
      .catch(function (err) {
        window.open(
          "mailto:?subject=" +
            encodeURIComponent(title) +
            "&body=" +
            encodeURIComponent(url),
        );
      });
  }
}
