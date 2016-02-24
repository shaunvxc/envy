# envy [![Build Status](https://travis-ci.org/shaunvxc/envy.svg?branch=master)](https://travis-ci.org/shaunvxc/envy) [![PyPI version](https://badge.fury.io/py/envy.svg)](https://badge.fury.io/py/envy)

### Why?

Have you ever needed to look at some code living in one of your virtual environments? And then spent a good 3 or 4 seconds typing out the path? At which point you were weary about making changes/setting breakpoints in your site-packages without first creating a backup... which then needed to be restored again after testing, and yada yada yada.  *This workflow is annoying and tedious*.

`envy` is a utility that allows you to **interact with all of the site-packages** in your currently active `virtualenv` as if they were in your **current working directory**

### How?
Let's say you are working in a virtual environment for a project `foo` but are getting errors thrown from one of `foo`'s depedencies-- a library called `bar`.  The stacktrace tells us the error was thrown from `baz.py`.  Using `envy`, simply run (from anywhere in your file system):

`(foo)$ envy edit bar/baz.py`

and you'll instantly be looking at the point-of-error from your favorite text editor!  This is pretty awesome, considering that this would normally require at some point typing out (or copy pasting-- which **is also** annoying) a full path like this: `~/.virtualenvs/foo/lib/pythonX.X/site-packages/bar/baz.py`.  

##### Great, the file is open, but I shouldn't create a backup before editing a file in my site-packages?
This is a good practice, but with `envy`, there is no need! `envy` will create a back up of the entire package (in the above example, `bar`) in `~/.envies/foo/bar`.  Throw down some `pdb`'s, `print`'s, or any little hack you want.  Whenever you are ready to restore the package back to it's original state, you need only run:

`(foo)$ envy clean bar`

And it'll be like you were never there!

### Wait, there's more!
`envy` can also you test changes on a library that you maintain and have checked out locally. 

Say you maintain a library `ham`, as well as another project `eggs` that depends on `ham`.  You want to test out some of you recent changes to `ham`, but are far from ready to start messing with the versioning or running `setup.py install`. With `envy` you can very quickly sync the changes from your local dev copy of `ham` to the one that lives `eggs` virtual environment like so:

`(eggs)$ envy sync ham`

You can also sync indivual files:

`(eggs)$ envy sync ham/spam.py`

**Note** that the `envy sync` commands must be run from within your local copy of the package you are syncing (i.e. `ham`)

As with `envy edit`, an backup of the package's (`ham`'s) state will be created automatically.  As with before, to restore the original state:

`(eggs)$ envy clean ham`

#### No talk, straight usage

Edit any file from any site-package installed in your active virtual environment:

`(active-virtualenv)$ envy edit any-site-package/any-file.py`

Discard any and all edits and return `any-site-package` to its original state:

`(active-virtualenv)$ envy clean any-site-package`
 ## old readme

It's times like these where `envy` can help!  `envy` gives you the power to open  **any module** within your current virtualenv, **from anywhere** in your filesystem,


Ever been working on a project and wanted to test changes or set breakpoints on one of its dependencies? **Without** having to screw around with the version, backing up a copy and running `setup.py install`? Let `envy sync` do it for you!

Ever wanted to directly edit or put a breakpoint in a virtualenv's copy of a file **without** having to type out `~/.virtualenvs/blah/lib/pythonX.X/site-packages/more/blah`? Enter `envy edit`!

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

Before copying local changes (or directly making changes with `envy edit`), envy **first** backs up the existing virtualenv.  It keeps a clean copy in `~/.envies/{virtual_env_name}/{project_name}`.

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
Edit the virtualenv's copy of a file directly: `bell.py`

`(foo)$ envy edit bar/bell.py`

**Note** that for the above command, unless you are running `envy` from within a local copy of `bar`, you'll **need** to specify the **both** package-name **and** the filename (as is done in the above with both `bar` and `bell.py`) 

If you **are** running `envy` from within a local copy of the package you are debugging, you can omit the package and just run:

`(foo)$ envy edit bar.py`

**Note**
`envy edit` uses the $EDITOR environment varible to launch a text editor-- if this is not set, simply add:

`export EDITOR=your_editor_of_choice`

to your .bashrc file.

##Installation

`$ pip install envy`

####Future work:

- improve test coverage
- explore implementing this using sym linking

## Contributing
1. Fork it ( https://github.com/shaunvxc/envy/fork )
1. Create your feature branch (`git checkout -b new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Run the tests (`make test`)
1. Push change to the branch (`git push origin new-feature`)
1. Create a Pull Request



