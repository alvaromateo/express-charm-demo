#!/usr/bin/env python3
# Copyright 2025 Ubuntu
# See LICENSE file for licensing details.

"""Flask Charm entrypoint."""

import logging
import typing

import ops
import paas_charm.flask
import lib.charms.http_k8s.v0.http_interface as http_interface

logger = logging.getLogger(__name__)


class FlaskAppCharm(paas_charm.flask.Charm):
    """Flask Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """Initialize the instance.

        Args:
            args: passthrough to CharmBase.
        """
        super().__init__(*args)

        self.httpProvider = http_interface.HTTPProvider(self, "backend", "80");


if __name__ == "__main__":
    ops.main(FlaskAppCharm)
