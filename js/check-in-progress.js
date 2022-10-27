const check_in_progress = () => {
  var xpath = "//span[text()='In Progress']";
  var matchingElement = document.evaluate(
    xpath,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;
  var parentOfSpan = matchingElement.parentNode;
  var currentInProgress = parentOfSpan.nextSibling.textContent;
  if (currentInProgress < 3) return;

  var area = parentOfSpan.parentNode.parentNode.parentNode.parentNode;
  currentInProgress > 4
    ? area.classList.add("pd-in-progress-red")
    : area.classList.add("pd-in-progress-orange");
};

window.addEventListener("load", function () {
  setTimeout(check_in_progress, 1000);
});
