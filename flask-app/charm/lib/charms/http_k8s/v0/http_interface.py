# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""The haproxy http interface module."""

import abc
import logging

from ops import RelationBrokenEvent, RelationChangedEvent, RelationJoinedEvent
from ops.charm import CharmBase, CharmEvents, RelationEvent
from ops.framework import EventSource, Object
from ops.model import Relation


### THESE 3 VARIABLES ARE NEEDED TO BE ABLE TO RUN "charmcraft fetch-libs"

# The unique Charmhub library identifier, never change it
# Library it's still not published, so it's a random string
LIBID = "3785165b24a743f2b0c60de52db25abc"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


logger = logging.getLogger()

HTTP_INTERFACE_RELATION = "http"
HTTP_INTERFACE_PORT = "80"

PROVIDER_HOSTNAME_KEY = "hostname"
PROVIDER_PORT_KEY = "port"

class HTTPBackendAvailableEvent(RelationEvent):
    """Event representing that http data has been provided."""


class HTTPBackendRemovedEvent(RelationEvent):
    """Event representing that http data has been removed."""


class HTTPRequirerEvents(CharmEvents):
    """Container for HTTP Provider events.

    Attrs:
        http_backend_available: Custom event when integration data is provided.
        http_backend_removed: Custom event when integration data is removed.
    """

    http_backend_available = EventSource(HTTPBackendAvailableEvent)
    http_backend_removed = EventSource(HTTPBackendRemovedEvent)


class _IntegrationInterfaceBaseClass(Object):
    """Base class for integration interface classes.

    Attrs:
        relations: The list of Relation instances associated with the charm.
        bind_address: The unit address.
    """

    def __init__(self, charm: CharmBase, relation_name: str):
        """Initialize the interface base class.

        Args:
            charm: The charm implementing the requirer or provider.
            relation_name: Name of the integration using the interface.
        """
        super().__init__(charm, relation_name)

        observe = self.framework.observe
        self.charm: CharmBase = charm
        self.relation_name = relation_name

        observe(charm.on[relation_name].relation_joined, self._on_relation_joined)
        observe(charm.on[relation_name].relation_changed, self._on_relation_changed)
        observe(charm.on[relation_name].relation_broken, self._on_relation_broken)

    @abc.abstractmethod
    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Abstract method to handle relation-joined event.

        Raises:
            NotImplementedError: if the abstract method is not implemented.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Abstract method to handle relation-changed event.

        Raises:
            NotImplementedError: if the abstract method is not implemented.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _on_relation_broken(self, event: RelationBrokenEvent) -> None:
        """Abstract method to handle relation-changed event.

        Raises:
            NotImplementedError: if the abstract method is not implemented.
        """
        raise NotImplementedError

    @property
    def relations(self) -> list[Relation]:
        """The list of Relation instances associated with the charm."""
        return self.charm.model.relations.get(self.relation_name, [])

    @property
    def bind_service(self) -> str:
        """Get unit bind k8s service name (needs CoreDNS to work properly).

        Returns:
            The service name, which is the same as the app name
        """
        return self.model.name


class HTTPRequirer(_IntegrationInterfaceBaseClass):
    """HTTP interface provider class to be instantiated by the haproxy-operator charm.

    Attrs:
        on: Custom events that are used to notify the charm using the provider.
    """

    onHTTPEvents = HTTPRequirerEvents()

    def __init__(self, charm: CharmBase, relation_name: str):
        super().__init__(charm, relation_name)

    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Handle relation-changed event.

        Args:
            event: relation-changed event.
        """
        provider_data = event.relation.data.get(event.relation.app)
        if provider_data:
            # update the databag of the unit that just received the event
            # with the information of the provider hostname and port
            event.relation.data[self.charm.unit].update(
                {
                    PROVIDER_HOSTNAME_KEY: provider_data[PROVIDER_HOSTNAME_KEY],
                    PROVIDER_PORT_KEY: provider_data[PROVIDER_PORT_KEY]
                }
            )

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handle relation-changed event.
        Is triggered always after a relation-joined event.
        This emits the http_backend_available event that the charm code can
        listen to and act upon.

        Args:
            event: relation-changed event.
        """
        self.onHTTPEvents.http_backend_available.emit(
            event.relation,
            event.app,
            event.unit,
        )

    def _on_relation_broken(self, event: RelationBrokenEvent) -> None:
        """Handle relation-broken event.

        Args:
            event: relation-broken event.
        """
        self.onHTTPEvents.http_backend_removed.emit(
            event.relation,
            event.app,
            event.unit,
        )


class HTTPProvider(_IntegrationInterfaceBaseClass):
    """HTTP interface provider class to be instantiated by the haproxy-operator charm."""

    def __init__(
        self,
        charm: CharmBase,
        relation_name = HTTP_INTERFACE_RELATION,
        port = HTTP_INTERFACE_PORT
    ):
        super().__init__(charm, relation_name)
        self.port = port

    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Handle relation joined event.
        When a new unit joins the relation, the HTTPProvider writes in
        the application databag its hostname and port.

        Args:
            event: relation-joined event.
        """
        if self.model.unit.is_leader():
            event.relation.save(
                {
                    PROVIDER_HOSTNAME_KEY: self.bind_service,
                    PROVIDER_PORT_KEY: self.port
                },
                self.charm.app
            )

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handle relation-changed event.

        Args:
            event: relation-changed event.
        """
        logger.debug(f"Nothing to do for relation-changed ({event.relation.name}).")

    def _on_relation_broken(self, event: RelationBrokenEvent) -> None:
        """Handle relation-broken event.
        Empty the application databag.

        Args:
            event: relation-broken event.
        """
        if self.model.unit.is_leader():
            event.relation.save({}, self.charm.app)
