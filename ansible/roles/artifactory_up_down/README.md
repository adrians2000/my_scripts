# this playbook is used to upload or download items from Artifactory
# the group_vars/artifactory_up_down/vars.yml file contains the necessary variables
# the group_vars/artifactory_up_down/vault.yml contains the passowrd inside the playbook
# fill that file and you are ready to go
#
# vault pass is: NothingToDo
# Ansible command to run role:
# ansible-playbook -i inventory/dev artifactory_up_down.yml --ask-vault-pass
