# -*- coding: utf-8 -*-

"""Test cases for Bio2BEL CREEDS."""

import os

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_creeds import Manager

__all__ = [
    'TemporaryCacheClass',
]


class TemporaryCacheClass(AbstractTemporaryCacheClassMixin):
    """A test case containing a temporary database and a Bio2BEL CREEDS manager."""

    Manager = Manager
    manager: Manager

    @classmethod
    def populate(cls):
        """Populate the Bio2BEL CREEDS database with test data."""
        # cls.manager.populate(url=...)
        raise NotImplementedError
