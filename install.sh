#!/bin/bash
set -euo pipefail

PORT=8090
DIR=/opt/filmix-proxy
PYTHON=$(command -v python3 || true)

if [ -z "$PYTHON" ]; then
  echo "python3 не найден, установите: apt-get install -y python3"
  exit 1
fi

mkdir -p "$DIR"
curl -fsSL https://vevsksenon.github.io/filmix_proxy.py -o "$DIR/filmix_proxy.py"

cat > /etc/systemd/system/filmix-proxy.service <<EOF
[Unit]
Description=Filmix proxy for Lampa
After=network-online.target

[Service]
ExecStart=$PYTHON $DIR/filmix_proxy.py $PORT
Restart=always
DynamicUser=yes

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable filmix-proxy
systemctl restart filmix-proxy

if command -v ufw >/dev/null && ufw status | grep -q "Status: active"; then
  ufw allow "$PORT/tcp"
fi

sleep 2
CHECK_URL="http://127.0.0.1:$PORT/param/User-Agent=okhttp%2F3.10.0/http://filmixapp.cyou/api/v2/post/8415?user_dev_id=0123456789abcdef&user_dev_token=aaaabbbbccccddddeeeeffffaaaabbbb"
if curl -s -m 30 "$CHECK_URL" | grep -q '"playlist":{"1"'; then
  echo "ГОТОВО: прокси работает. В Лампе укажите альтернативный прокси http://$(curl -s -m 10 https://ipinfo.io/ip || echo IP-сервера):$PORT/"
else
  echo "ОШИБКА: прокси не отдал Баффи. Лог службы:"
  journalctl -u filmix-proxy -n 20 --no-pager
  exit 1
fi
