document.addEventListener('click', function (event) {
    if (event.target.getAttribute("data-disable-with") === "Closing project...") {
        var image = addImage();

        showConfetti(image);
        unfade(image);
    }
}, false);

function unfade(element) {
    var op = 0.1;
    element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }

        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 50);
}

function addImage() {
    var node = document.createElement("div");
    node.id = 'well-done';
    node.style = "position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);opacity:0;z-index:999;";

    var img = document.createElement("img");
    img.src = chrome.runtime.getURL("/img/well-done.png");

    node.appendChild(img);
    document.body.appendChild(node);

    return node;
}

function showConfetti(element) {

    var duration = 15 * 1000;
    var animationEnd = Date.now() + duration;
    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
    }

    var interval = setInterval(function() {
        var timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            element.parentNode.removeChild(element);
            return clearInterval(interval);
        }

        var particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);


}
