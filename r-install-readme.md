# README for Installing Packages in WSL2

Instead of using `install.packages`, for many packages it may just be less trouble to install precompiled packages from the Ubuntu repository.
The issue is you will encounter many "this dependency is not installed please do `deb foo`" errors during installation.
The package websites are not super clear about what prerequisites are required to be installed before attempting to install them in a WSL2 system.
This will cause a lot of frustration in trying to install these packages when most of the time you simply want to install `tidyverse`, `languageserver` if using with VSC, and a task view of choice.

The alternative is to directly install `r-cran` packages maintained by the `c2d4u` team.
First grab task view descriptions with `wget`:
```
wget https://github.com/cran-task-views/Econometrics/blob/main/<View>.md
```
`<View>` is the name of the task view (e.g., `Econometrics`). Then retrieve all named packages and install those that are available in the `c2d4u` repository:
```
sudo apt-get -y --no-install-recommends install $(apt-cache --generate pkgnames | grep --line-regexp --fixed-strings $(grep -P -i -o "(?<=pkg\(\")[a-z0-9_]+?(?=\")" <View>.md | sed -E s/^/-e\ r-cran-/i | tr [A-Z] [a-z])))
```
