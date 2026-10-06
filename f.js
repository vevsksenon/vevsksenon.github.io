(function () {
  var src = 'https://nb557.github.io/plugins/online_mod.js';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', src + '?t=' + Date.now());
  xhr.onload = function () {
    var code = xhr.responseText.replace("Lampa.Storage.set('online_mod_proxy_filmix', 'true');", "Lampa.Storage.set('online_mod_proxy_filmix', 'false');");
    var script = document.createElement('script');
    script.text = code;
    document.head.appendChild(script);
  };
  xhr.onerror = function () {
    var script = document.createElement('script');
    script.src = src;
    document.head.appendChild(script);
  };
  xhr.send();
})();
