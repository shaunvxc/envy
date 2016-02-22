# envy [![Build Status](https://travis-ci.org/shaunvxc/envy.svg?branch=master)](https://travis-ci.org/shaunvxc/envy) [![PyPI version](https://badge.fury.io/py/envy.svg)](https://badge.fury.io/py/envy)

#### Why?
Ever been working on a project and wanted to test changes or set breakpoints on one of its dependencies? **Without** having to screw around with the version and running `setup.py install`? **Without** having to deal with backing up the virtualenv beforehand or worry about restoring it later? Let `envy` do it for you!

Ever wanted to directly edit or put a breakpoint in a virtualenv's copy of a file **without** having to punch out the full path? `envy edit` is your friend!

#### How?
Lets say you are working in a virtual environment for a project `foo` but are getting errors thrown from one of `foo`'s depedencies-- a library called `bar`.  Assuming `bar` is readily accessible in your workspace, you can simply make any local changes you want to `bar` (apply breakpoints, etc), and run:

   `(foo)$ envy sync bar`
  
This command will detect your current working virtualenv (in this case `foo`), as well as the current package you are working in (in this case, `bar`).  `envy` uses this information, along with some checks, to construct `bar`'s location *within* `foo`'s virtualenv.  It will copy your local changes to `bar`'s site-package within `foo`'s virtualenv.

#### Okay great, but what if I don't have a local copy of the dependency? :confused:
What if you have no local copy of `bar`?  Or you have a local copy, but your local version is different than the version used in `foo`'s virtual environment.  

In these cases, one option is to make a small change or put a breakpoint in the virtualenv's copy of the file.  Of course, this requires pointing a text editor to the file's location within the virtualenv. (i.e. `~/.virtualenvs/foo/lib/pythonX.X/site-packages/bar/bar.py` )

A better option is to use `envy`'s `edit` command to directly edit the copy of the file within the virtual environment, in the text editor of your choice (`vim` by default).

   `(foo)$ envy edit bar/bar.py`

This command will open the `bar/bar.py` within `foo`'s virtual environment (a lot quicker, no?).

#### Could this corrupt my virtualenv? :fearful:

Rest easy! :sweat_smile: Before copying local changes (or directly making changes with `envy edit`), envy **first** backs up the existing virtualenv.  It keeps a clean copy in `~/.envies/{virtual_env_name}/{project_name}`.

Whenever you are done testing and/or wish to restore the virtualenv to its original state, simply run:
    
`$ envy clean`

## Usage Examples
Copy all changes from `foo` to `~/.virtualenvs/foo/lib/pythonX.X/site-packages/bar`:

`(foo)$ envy sync bar `

Copy changes from a file in `bell.py` to `~/.virtualenvs/foo/lib/pythonX.X/site-packages/bar`:

`(foo)$ envy sync bar/bell.py`

Restore virtualenv to its original state:

`(foo)$ envy clean`

### `envy edit`
Set the default text editor that you'd like to summon when using `envy edit`:

`$ envy edit set-editor vim # or emacs, atom, subl, etc`

Edit the virtualenv's copy of a file directly: `bell.py`

`(foo)$ envy edit bar/bell.py`

**Note** that for the above command, unless you are running `envy` from within a local copy of `bar`, you'll **need** to specify the **both** package-name **and** the filename (as is done in the above with both `bar` and `bell.py`) 

If you **are** running `envy` from within a local copy of the package you are debugging, you can omit the package and just run:

`(foo)$ envy edit bar.py`

##Installation

`$ pip install envy`

####Future work:

- improve test coverage
- ?

## Contributing
1. Fork it ( https://github.com/shaunvxc/envy/fork )
1. Create your feature branch (`git checkout -b new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Run the tests (`make test`)
1. Push change to the branch (`git push origin new-feature`)
1. Create a Pull Request



