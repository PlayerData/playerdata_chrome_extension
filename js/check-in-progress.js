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
  var colour = currentInProgress > 4 ? "red" : "orange";
  area.style.border = `${colour} 3px solid`;
};

window.addEventListener("load", function () {
  // even with the load we have to make sure everything is loaded...Ugh!
  this.setTimeout(check_in_progress, 1000);
});
