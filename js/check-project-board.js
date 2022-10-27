const check_in_progress = () => {
  var xpath = "//span[text()='In Progress']";
  var matchingElement = document.evaluate(
    xpath,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;
  if (!matchingElement) {
    return;
  }
  var parentOfSpan = matchingElement.parentNode;
  var currentInProgress = parentOfSpan.nextSibling.textContent;
  if (currentInProgress < 3) return;

  var area = parentOfSpan.parentNode.parentNode.parentNode.parentNode;
  currentInProgress > 4
    ? area.classList.add("pd-in-progress-red")
    : area.classList.add("pd-in-progress-orange");
};

const check_for_points = () => {
  const cards = document.querySelectorAll(
    '[data-test-id="board-view-column-card"]'
  );
  cards.forEach((card) => {
    const allLabels = card.querySelectorAll('[data-test-id="issue-label"]');
    var isEpic = false;
    var hasPoints = false;
    allLabels.forEach((lbl) => {
      if (lbl.firstChild.textContent === "epic") {
        isEpic = true;
      }
      if (lbl.firstChild.textContent.indexOf("points/") > 0) {
        hasPoints = true;
      }
    });

    if (isEpic && !hasPoints) {
      card.classList.add("pd-in-progress-red");
    }
  });
};

const handleScroll = () => {
  document.querySelector('[data-test-id="board-view"]').addEventListener(
    "scroll",
    function (event) {
      check_for_points();
    },
    false
  );
};

window.addEventListener("load", function () {
  setTimeout(() => {
    check_in_progress();
    check_for_points();
    handleScroll();
  }, 1000);
});
