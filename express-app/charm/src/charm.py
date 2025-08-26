#!/usr/bin/env python3
# Copyright 2025 Alvaro Mateo
# See LICENSE file for licensing details.

"""ExpressJS Charm entrypoint."""

import logging
import typing

import ops
import paas_charm.expressjs
import charms.http_k8s.v0.http_interface as http_interface

from paas_charm.app import App, WorkloadConfig
from paas_charm.charm_state import CharmState
from paas_charm.database_migration import DatabaseMigration

logger = logging.getLogger(__name__)


BACKEND_RELATION_NAME = "flask-backend"

class ExpressApp(App):
    def __init__(
        self,
        *,
        container: ops.Container,
        charm_state: CharmState,
        workload_config: WorkloadConfig,
        database_migration: DatabaseMigration,
        framework_config_prefix: str = "APP_",
        configuration_prefix: str = "APP_",
        integrations_prefix: str = "",
        http_integration: http_interface.HTTPRequirer = None,
    ):
        super().__init__(
            container=container,
            charm_state=charm_state,
            workload_config=workload_config,
            database_migration=database_migration,
            framework_config_prefix=framework_config_prefix,
            configuration_prefix=configuration_prefix,
            integrations_prefix=integrations_prefix
        )
        self._http_integration = http_integration

    def gen_environment(self) -> dict[str, str]:
        env = super().gen_environment()
        # add environment variables for HTTP flask-backend
        logger.info("Generating environment for ExpressApp")
        http_relation_data = self._http_integration.get_relation_data()
        if http_relation_data:
            prefix = BACKEND_RELATION_NAME.replace('-', '_').upper()
            logger.info(f"url = {http_relation_data.url}")
            #env[f"{prefix}_URL"] = http_relation_data[http_interface.PROVIDER_URL_KEY]
            #logger.info(f"Added {prefix}_URL = {http_relation_data[http_interface.PROVIDER_URL_KEY]}")
        return env


class ExpressCharmDemoCharm(paas_charm.expressjs.Charm):
    """ExpressJS Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """
        Initialize the instance.
        """
        super().__init__(*args)

        self._httpRequirer = http_interface.HTTPRequirer(self, BACKEND_RELATION_NAME)

        self.framework.observe(self._httpRequirer.on.http_backend_available, self.restart)
        self.framework.observe(self._httpRequirer.on.http_backend_removed, self.restart)

    def _create_app(self) -> App:
        """Build a App instance.

        Returns:
            A new App instance.
        """
        charm_state = self._create_charm_state()
        return ExpressApp(
            container=self._container,
            charm_state=charm_state,
            workload_config=self._workload_config,
            database_migration=self._database_migration,
            framework_config_prefix="",
            http_integration=self._httpRequirer,
        )

if __name__ == "__main__":
    ops.main(ExpressCharmDemoCharm)
