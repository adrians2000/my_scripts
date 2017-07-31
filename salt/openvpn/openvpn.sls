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

mode 555 pam_google_authenticator.so:
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

{% for item in  'vars', 'openssl-1.0.cnf' %}
restart openvpn, {{ item }} changed:
  service.running:
    - name: openvpn
    - enable: True
    - reload: True
    - watch:
      - {{ pillar['openvpn_directory'] }}/easy-rsa/{{ item }}
{% endfor %}
