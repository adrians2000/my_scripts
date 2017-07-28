copy sshd_config:
  file:
    - managed
    - source: salt://sshd/files/sshd_config
    - template: jinja
    - name: /etc/ssh/sshd_config
    - user: root
    - mode: 644
