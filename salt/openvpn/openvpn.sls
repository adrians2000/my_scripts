install openvpn:
  pkg:
    - installed
    - name: openvpn
    - enable: True

install google_auth:
  - installed
  - pkgs:
    - pam_google_authenticator
    - libqrencode

chmode 555 pam_google_authenticator.so:
  file:
    - name: /usr/local/lib/pam_google_authenticator.so
    - mode 555
    - user: root

copy openvn to pam.d:
  file:
    - managed
    - source: salt://openvpn/pam.d_openvpn
    - name: /etc/pam.d/openvpn
    - mode: 644
    - user: root

create {{ pillar['openvpn_directory'] }}:
  file:
    - directory
    - user: root
    - mode: 755
    - name: {{ pillar['openvpn_directory'] }}

{% for item in  'keys', 'easy-rsa' %}
create {{ pillar['openvpn_directory'] }}/{{ item }}:
  file:
    - directory
    - user: root
    - mode: 755
    - name: {{ pillar['openvpn_directory'] }}/{{ item }}
{% endfor %}

copy openvpn.conf:
  file:
    - managed
    - source: salt://openvpn/openvpn.conf
    - name: {{ pillar['openvpn_directory'] }}/openvpn.conf
    - mode: 644
    - user: root

copy openssl-1.0.cnf:
  file:
    - managed
    - source: salt://openvpn/{{ item }}
    - name: {{ pillar['openvpn_directory'] }}/easy-rsa/openssl-1.0.cnf
    - mode: 644
    - user: root

copy vars:
  file:
    - managed
    - source: salt://openvpn/vars
    - name: {{ pillar['openvpn_directory'] }}/easy-rsa/vars
    - mode: 644
    - user: root

{% for item in  pillar['keys_and_certs'] %}
copy {{ item }}:
  file:
    - managed
    - source: salt://openvpn/{{ item }}
    - name: {{ pillar['openvpn_directory'] }}/keys/{{ item }}
{% endfor %}

start openvpn:
  service.running:
    - name: openvpn
    - enable: True

restart openvpn if files change:
  service.running:
    - name: openvpn
    - enable: True
    - reload: True
    - watch:
      - {{ pillar['openvpn_directory'] }}/easy-rsa/vars
      - {{ pillar['openvpn_directory'] }}/easy-rsa/openssl-1.0.cnf
      - {{ pillar['openvpn_directory'] }}/openvpn.conf
      - {{ pillar['openvpn_directory'] }}/keys/dh.pem
      - {{ pillar['openvpn_directory'] }}/keys/ca.crt
      - {{ pillar['openvpn_directory'] }}/keys/ta.key
      - {{ pillar['openvpn_directory'] }}/keys/openvpn-server.crt
      - {{ pillar['openvpn_directory'] }}/keys/openvpn-server.key

{% for username, details in pillar.get('users', {}).items() %}
{{ username }}:
  group:
    - present
    - name: {{ username }}
    - gid: {{ details.get('gid', '') }}

  user:
    - present
    - fullname: {{ details.get('fullname','') }}
    - name: {{ username }}
    - shell: /bin/sh
    - home: /home/{{ username }}
    - password: {{ details.get('password','') }}
{% endfor %}
