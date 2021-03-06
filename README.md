# cheat-ext
[![Build Status](https://travis-ci.org/chhsiao90/cheat-ext.svg?branch=master)](https://travis-ci.org/chhsiao90/cheat-ext)
[![Coverage Status](https://coveralls.io/repos/github/chhsiao90/cheat-ext/badge.svg?branch=master)](https://coveralls.io/github/chhsiao90/cheat-ext?branch=master)
[![PyPI](https://img.shields.io/pypi/v/cheat-ext.svg)](https://pypi.python.org/pypi/cheat-ext/)
[![PyPI](https://img.shields.io/pypi/dm/cheat-ext.svg)](https://pypi.python.org/pypi/cheat-ext/)
  
An extension of [cheat](https://github.com/chrisallenlane/cheat)
Provide simple methodology to extends cheatsheets

## Install
```
pip install cheat-ext
```

## Usage

### Download cheatsheets from github
This command will clone github respository to ```~/.cheat/.ext/author_repository```  
and will also add symbolic link from ```~/.cheat/cmd``` to ```~/.cheat/.ext/author_repository/cmd```

```
# installed cheatsheets from github repository
cheat-ext install chhsiao90/cheatsheets-java
# then use cheat to display the cheatsheet defined in the cheatsheets repository
cheat cmd
```

## Available cheatsheets
- [chhsiao90/cheatsheets-java](https://github.com/chhsiao90/cheatsheets-java) : Cheatsheets for Java
