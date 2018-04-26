.RECIPEPREFIX = >

install_dir := /opt/sortinghat
bin_dir := /usr/local/bin

develop:
> python3 -m venv .venv
> .venv/bin/pip install --upgrade pip
> .venv/bin/pip install --editable .

install:
> [[ -d ${install_dir} ]] || python3 -m venv ${install_dir}
> ${install_dir}/bin/pip install --upgrade pip
> ${install_dir}/bin/pip install .
> ln -s ${install_dir}/bin/sortinghat ${bin_dir}/sortinghat
