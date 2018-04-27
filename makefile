.RECIPEPREFIX = >

develop:
> python3 -m venv .venv
> .venv/bin/pip install --upgrade pip
> .venv/bin/pip install ansible
> .venv/bin/pip install --editable .

provision:
> .venv/bin/ansible-playbook -e "HOSTS=hatbox" ansible/playbook.yml
