(function () {
  // Домашняя сеть не открывает 2.56.123.213. Прокси должен быть на Маке в той же Wi-Fi.
  // var proxy = 'http://192.168.68.101:8090/';
  // var okhttp = 'okhttp/3.10.0';
  //
  // Lampa.Storage.set('online_mod_proxy_other', 'true');
  // Lampa.Storage.set('online_mod_proxy_other_url', proxy);
  // Lampa.Storage.set('online_mod_proxy_filmix', 'true');
  //
  // function hostOf(url) {
  //   var match = String(url).match(/^https?:\/\/([^\/?#]+)/i);
  //   return match ? match[1].split(':')[0].toLowerCase() : '';
  // }
  //
  // function throughProxy(url) {
  //   if (typeof url !== 'string' || url.indexOf(proxy) === 0) return url;
  //   var host = hostOf(url);
  //   if (!host || host.indexOf('filmix') === -1) return url;
  //   var ua = host.indexOf('filmixapp.') === 0 ? okhttp : 'Mozilla/5.0';
  //   var prefix = 'param/User-Agent=' + encodeURIComponent(ua) + '/';
  //   if (host.indexOf('filmixapp.') !== 0) {
  //     var origin = 'https://' + host;
  //     prefix += 'param/Origin=' + encodeURIComponent(origin) + '/';
  //     prefix += 'param/Referer=' + encodeURIComponent(origin + '/') + '/';
  //     prefix += 'param/X-Requested-With=' + encodeURIComponent('XMLHttpRequest') + '/';
  //   }
  //   return proxy + prefix + url;
  // }
  //
  // if (typeof Lampa.Reguest === 'function') {
  //   var Orig = Lampa.Reguest;
  //   var Wrapped = function () {
  //     var req = new Orig();
  //     ['native', 'silent', 'get', 'post'].forEach(function (method) {
  //       if (typeof req[method] !== 'function') return;
  //       var orig = req[method];
  //       req[method] = function () {
  //         var args = Array.prototype.slice.call(arguments);
  //         if (typeof args[0] === 'string') args[0] = throughProxy(args[0]);
  //         return orig.apply(req, args);
  //       };
  //     });
  //     return req;
  //   };
  //   Wrapped.prototype = Orig.prototype;
  //   Lampa.Reguest = Wrapped;
  // }

  var script = document.createElement('script');
  script.src = 'https://nb557.github.io/plugins/online_mod.js';
  script.onload = function () {
    // Lampa.Storage.set('online_mod_proxy_other', 'true');
    // Lampa.Storage.set('online_mod_proxy_other_url', proxy);
    // Lampa.Storage.set('online_mod_proxy_filmix', 'true');
  };
  document.head.appendChild(script);
})();
