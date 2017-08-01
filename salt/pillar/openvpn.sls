openvpn_directory: /usr/local/etc/openvpn
keys_and_certs:
  - dh.pem
  - ca.crt
  - ta.key
  - openvpn-server.crt
  - openvpn-server.key

users:
  ion:
    fullname: ion ion
    password: $6$STHPJrYoipxWAFpV$rm62K0wEkBhrQoZe9VboFRMJyysH1yEiSdouccD6Hg/qfyS6bXRYKorg0i9Ku6Ov8wmnLIc1ZoGNeBKK/dnDw0

  alt_ion:
    fullname: alt ion
    password: $6$STHPJrYoipxWAFpV$rm62K0wEkBhrQoZe9VboFRMJyysH1yEiSdouccD6Hg/qfyS6bXRYKorg0i9Ku6Ov8wmnLIc1ZoGNeBKK/dnDw0

  inca_un_ion:
    fullname: inca un ion
    password: $6$STHPJrYoipxWAFpV$rm62K0wEkBhrQoZe9VboFRMJyysH1yEiSdouccD6Hg/qfyS6bXRYKorg0i9Ku6Ov8wmnLIc1ZoGNeBKK/dnDw0
