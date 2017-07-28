install openvpn:
  pkg:
    - installed
    - name: openvpn
    - enable: True

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

copy /usr/local/etc/openvpn/openvpn.conf:
  file:
    - managed
    - source: salt://openvpn/openvpn.conf
    - name: /usr/local/etc/openvpn/openvpn.conf
    - mode: 644
    - user: root

{% for item in  'vars', 'openssl-1.0.cnf' %}
copy {{ item }} file:
  file:
    - managed
    - source: salt://openvpn/{{ item }}
    - name: {{ pillar['openvpn_directory'] }}/easy-rsa/{{ item }}
{% endfor %}

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
