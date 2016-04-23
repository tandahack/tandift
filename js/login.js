// shim layer with setTimeout fallback
// always got hugz for Paul Irish
window.requestAnimFrame = (function() {
  return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    function(callback) {
      window.setTimeout(callback, 1000 / 60);
    };
})();

var goButton = document.getElementById("animate");
var container = document.getElementById("container");
var animating = false;

goButton.addEventListener('click', function() {

  if (animating)
    return;

  container.classList.add('active');
  animating = true;

  setTimeout(function() {
    requestAnimFrame(function() {
      animating = false;
      container.classList.remove('active');
      container.classList.toggle('reverse');
    });
  }, 680);
});