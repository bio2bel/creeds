# -*- coding: utf-8 -*-

"""Command line interface for Bio2BEL CREEDS.

Why does this file exist, and why not put this in ``bio2bel_creeds.__main__``?

You might be tempted to import things from ``bio2bel_creeds.__main__`` later,
but that will cause problems - the code will get executed twice:

- When you run ``python3 -m bio2bel_creeds`` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``bio2bel_creeds.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``bio2bel_creeds.__main__`` in ``sys.modules``.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from .manager import Manager

main = Manager.get_cli()

if __name__ == '__main__':
    main()
