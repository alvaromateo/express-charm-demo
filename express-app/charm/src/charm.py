#!/usr/bin/env python3
# Copyright 2025 Alvaro Mateo
# See LICENSE file for licensing details.

"""ExpressJS Charm entrypoint."""

import logging
import typing

import ops

import paas_charm.expressjs

logger = logging.getLogger(__name__)


class ExpressCharmDemoCharm(paas_charm.expressjs.Charm):
    """ExpressJS Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """
        Initialize the instance.
        """
        super().__init__(*args)

        self.container = self.unit.get_container("app")
        # config changed
        # relation created
        # relation changed


if __name__ == "__main__":
    ops.main(ExpressCharmDemoCharm)
