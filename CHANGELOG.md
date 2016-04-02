
## 0.0.9

  **a083560**: Fix finding deeply nested files in a package. The following usage now works:
  
  	(some_env)$ envy edit package/subfolder/some_module.py

## 0.0.8

  **06c4392**: Address problems with `vim` discussed in #4

	If vim is set as $EDITOR, envy will use the standard default editor (vi) instead.

## 0.0.7

  **a76b994**: alert user if they run envy with existing backup copy
