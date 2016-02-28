# envy [![Build Status](https://travis-ci.org/shaunvxc/envy.svg?branch=master)](https://travis-ci.org/shaunvxc/envy) [![PyPI version](https://badge.fury.io/py/envy.svg)](https://badge.fury.io/py/envy)

### Why?

Have you ever needed to look at some code living in one of your virtual environments? And then spent a good 3 or 4 seconds typing out the path? At which point you were weary about making changes/setting breakpoints in your site-packages without first creating a backup... which then needed to be restored again after testing, and yada yada yada.  *This workflow is annoying and tedious*.

`envy` is a utility that allows you to **interact with all of the site-packages** in your currently active `virtualenv` as if they were in your **current working directory**

### How?
Let's say you are working in a virtual environment for a project `foo` but are getting errors thrown from one of `foo`'s depedencies-- a library called `bar`.  The stacktrace tells us the error was thrown from `baz.py`.  Using `envy`, simply run (from anywhere in your file system):

`(foo)$ envy edit bar/baz.py`

and you'll instantly be looking at the point-of-error from your favorite text editor!  This is pretty awesome, considering that this would normally require at some point typing out (or copy pasting-- which **is also** annoying) a full path like this: `~/.virtualenvs/foo/lib/pythonX.X/site-packages/bar/baz.py`.  

##### Great, the file is open, but I shouldn't create a backup before editing a file in my site-packages? :confused:
This is a good practice, but with `envy`, there is no need! `envy` will create a back up of the entire package (in the above example, `bar`) in `~/.envies/foo/bar`.  Throw down some `pdb`'s, `print`'s, or any little hack you want.  Whenever you are ready to restore the package back to it's original state, you need only run:

`(foo)$ envy clean bar`

And it'll be like you were never there!

### Wait, there's more! :pig2: :egg:
With `envy` you can also test changes on a library that you maintain and have checked out locally. 

Say you maintain a library `ham`, as well as another project `eggs` that depends on `ham`.  You want to test out some of your recent changes to `ham`, but are far from ready to start messing with the versioning or running `setup.py install`. With `envy` you can very quickly sync the changes from your local dev copy of `ham` to the one that lives `eggs` virtual environment like so:

`(eggs)$ envy sync ham`

You can also sync indivual files:

`(eggs)$ envy sync ham/spam.py`

**Note** that the `envy sync` commands must be run from within your local copy of the package you are syncing (i.e. `ham`)

As with `envy edit`, an backup of the package's (`ham`'s) state will be created automatically.  As with before, to restore the original state:

`(eggs)$ envy clean ham`

#### No talk, straight usage :no_mouth:

Edit any file from any site-package installed in your active virtual environment:

`(active-virtualenv)$ envy edit any-site-package/any-file.py`

Discard any and all edits and return `any-site-package` to its original state:

`(active-virtualenv)$ envy clean any-site-package`

You can run both `edit` and `clean` from anywhere in your filesystem, as long as you are in a virtualenv that contains the package you ask it for.

To sync all local changes from some `random_lib` to where its copy in `some-virtualenv`, run:

`(some-virtualenv):dev/random_lib$ envy sync random_lib`

For the time being, `sync` commands cannot be run as flexibly as `edit` and `clean` (they will only work when run from within the python package you wish to sync)- although it would certainly be possible to improve this in the future.

**Note**
`envy edit` uses the `$EDITOR` environment varible to launch a text editor-- if this is not set, simply add:

`export EDITOR=your_editor_of_choice`

to your .bashrc file.

##Installation

`$ pip install envy`

####Future work:
- allow syncing from anywhere on filesystem
- improve test coverage
- add optional virtualenv argument to allow syncing/editing to nonactive virtualenvs

## Contributing
1. Fork it ( https://github.com/shaunvxc/envy/fork )
1. Create your feature branch (`git checkout -b new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Run the tests (`make test`)
1. Push change to the branch (`git push origin new-feature`)
1. Create a Pull Request



