var check_smoke_tests = () => {
  var xpath = "//p[text()='Smoke Tests:']";
  var smoke_tests = document.evaluate(
    xpath,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;
  var smoke_test_items =
    smoke_tests.nextElementSibling.getElementsByTagName("li");

  disable_merge = false;
  if (smoke_test_items.length < 1) {
    disable_merge = true;
  } else if (smoke_test_items[0].textContent.trim() === "...") {
    disable_merge = true;
  }

  var merge = document.getElementsByClassName("merge-message")[0];
  merge.style.visibility = disable_merge ? "hidden" : "visible";
};

window.addEventListener("load", function () {
  // even with the load we have to make sure everything is loaded...Ugh!
  this.setTimeout(check_smoke_tests, 1000);
});
