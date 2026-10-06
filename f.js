(function () {
  Lampa.Storage.set('online_mod_proxy_other', 'true');
  Lampa.Storage.set('online_mod_proxy_other_url', 'http://194.156.119.181:8090/');

  var script = document.createElement('script');
  script.src = 'https://nb557.github.io/plugins/online_mod.js';
  document.head.appendChild(script);
})();
