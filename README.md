# envy [![PyPI version](https://badge.fury.io/py/envy.svg)](https://badge.fury.io/py/envy)

#### Why?
Ever been working on a project and wanted to test changes or set breakpoints on one of its dependencies? **Without** having to screw around with the version and running `setup.py install`? **Without** having to deal with backing up the virtualenv beforehand or worry about restoring it later? Let `envy` do it for you!

Ever wanted to directly edit a file SITTING in a virtualenv *without* having to type out the full path?

**`envy edit`** is your friend!

#### How?
Envy-edit --  wip
Lets say you are working in a virtual environment for project A but get errors thrown from project B (a dependency of project A).  Assuming project B is readily accessible in your workspace, you can simply make any local changes you want to project B (apply breakpoints, etc), and run:

    $ envy sync <what you want sync'd>
  
This command will detect your current working virtualenv, as well as the path to project B *within* A's virtualenv.  It will copy your local changes to B's site-package within A's virtualenv.

#### Could this corrupt my virtualenv?
Before copying local changes, envy first backs up the existing virtualenv.  It keeps a clean copy in       `~/.envies/{virtual_env_name}/{project_name}`.

When you are done testing and wish to restore the virtualenv to its original state, simple run:

    $ envy clean

## Usage Examples
Copy all changes from `project_b` to `~/.virtualenvs/project_a/lib/pythonX.X/site-packages/project_b`:


`(project_a)$ envy sync project_b `

Copy changes from a file in `project_b` to `~/.virtualenvs/project_a/lib/pythonX.X/site-packages/project_b`:


`(project_a)$ envy sync project_b/file.py`

Restore virtualenv to its original state:

`(project_a)$: envy clean`

##Installation

`$ pip install envy`

This is a very early stage project and can likely be improved.  

## Contributing
1. Fork it ( https://github.com/shaunvxc/envy/fork )
1. Create your feature branch (`git checkout -b new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Run the tests (`make test`) # need to add tests!!
1. Push change to the branch (`git push origin new-feature`)
1. Create a Pull Request



