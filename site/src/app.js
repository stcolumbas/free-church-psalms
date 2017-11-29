const Elm = require('./Main.elm');

require('./index.html');
require('./offline.html');
require('./manifest.json');
require('./static/favicon.ico');
require('./service-worker.js');
require('../node_modules/tailwindcss/dist/tailwind.min.css');

function handleDOMContentLoaded() {
  // setup elm
  const app = Elm.Main.fullscreen();
  // register SW
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
  }
}

window.addEventListener('DOMContentLoaded', handleDOMContentLoaded, false);
