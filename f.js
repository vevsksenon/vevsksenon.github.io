(function () {
  var proxy = 'http://2.56.123.213:8090/';
  Lampa.Storage.set('online_mod_proxy_other', 'true');
  Lampa.Storage.set('online_mod_proxy_other_url', proxy);

  var ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

  function wrap(url) {
    if (typeof url !== 'string' || url.indexOf(proxy) === 0 || !/^https?:\/\//i.test(url)) return url;
    return proxy + 'param/User-Agent=' + encodeURIComponent(ua) + '/' + url;
  }

  function wrapItem(item) {
    if (!item || typeof item !== 'object') return item;
    if (item.url) item.url = wrap(item.url);
    if (item.quality) {
      Object.keys(item.quality).forEach(function (key) {
        item.quality[key] = wrap(item.quality[key]);
      });
    }
    if (Array.isArray(item.playlist)) item.playlist.forEach(wrapItem);
    return item;
  }

  if (Lampa.Player) {
    var play = Lampa.Player.play;
    Lampa.Player.play = function (data) {
      return play.call(this, wrapItem(data));
    };
    if (Lampa.Player.playlist) {
      var playlist = Lampa.Player.playlist;
      Lampa.Player.playlist = function (list) {
        if (Array.isArray(list)) list.forEach(wrapItem);
        return playlist.call(this, list);
      };
    }
  }

  var script = document.createElement('script');
  script.src = 'https://nb557.github.io/plugins/online_mod.js';
  document.head.appendChild(script);
})();
