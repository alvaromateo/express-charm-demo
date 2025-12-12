#!/usr/bin/env python3
# Copyright 2025 Ubuntu
# See LICENSE file for licensing details.

"""Flask Charm entrypoint."""

import logging
import typing

import ops
import paas_charm.flask
from charms.traefik_k8s.v2.ingress import IngressPerAppRequirer

logger = logging.getLogger(__name__)


class AppCharm(paas_charm.flask.Charm):
    """Flask Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """Initialize the instance.

        Args:
            args: passthrough to CharmBase.
        """
        super().__init__(*args)

        self._frontend_port = self.config.get("frontend_port", 3010)

        self._ingress_frontend = IngressPerAppRequirer(
            self,
            relation_name="ingress-frontend",
            port=self._frontend_port,
            strip_prefix=True,
        )
        self.framework.observe(self._ingress_frontend.on.ready, self._on_ingress_ready)
        self.framework.observe(self._ingress_frontend.on.revoked, self._on_ingress_revoked)

    def restart(self, rerun_migrations: bool = False) -> None:
        """Restart or start the service if not started with the latest configuration.

        Args:
            rerun_migrations: whether it is necessary to run the migrations again.
        """
        if not self.is_ready():
            return

        self._ingress_frontend.provide_ingress_requirements(port=self._frontend_port)
        self.unit.set_ports(ops.Port(protocol="tcp", port=self._frontend_port))

        super().restart()
    
    def _on_update_status(self, event: ops.HookEvent) -> None:
        super()._on_update_status(event)
        self._ingress_frontend._publish_auto_data()


if __name__ == "__main__":
    ops.main(AppCharm)
