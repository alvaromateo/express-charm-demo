# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""The haproxy http interface module."""

import abc
import logging
import typing
from pydantic import BaseModel, ValidationError

from ops import Relation, RelationBrokenEvent, RelationChangedEvent, RelationJoinedEvent
from ops.charm import CharmBase, CharmEvents, RelationEvent
from ops.framework import EventSource, Object


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
PROVIDER_URL_KEY = "url"

class HTTPBackendAvailableEvent(RelationEvent):
    """Event representing that http data has been provided."""

    @property
    def url(self) -> str:
        """Fetch the HTTP url from the relation."""
        assert self.relation.app
        return typing.cast(str, self.relation.data[self.relation.app].get("url"))


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


class HttpRelationData(BaseModel):
    """Represent the relation data.

    Attributes:
        url: The URL where the HTTP endpoint is located.
    """

    url: str

    def to_relation_data(self) -> typing.Dict[str, str]:
        """Convert an instance of HttpRelationData to the relation representation.

        Returns:
            Dict containing the representation.
        """
        return {
            "url": str(self.url),
        }


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
        self.charm = charm
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

    def get_relation_data(self) -> typing.Optional[HttpRelationData]:
        """Retrieve the relation data.

        Returns:
            HttpRelationData: the relation data.
        """
        relation = self.model.get_relation(self.relation_name)
        return self._get_relation_data_from_relation(relation) if relation else None

    def _get_relation_data_from_relation(
        self, relation: Relation
    ) -> typing.Optional[HttpRelationData]:
        """Retrieve the relation data.

        Args:
            relation: the relation to retrieve the data from.

        Returns:
            HttpRelationData: the relation data.
        """
        assert relation.app
        relation_data = relation.data[relation.app]
        if not relation_data:
            logger.warning(f"relation data for {relation.name} not found")
            return None

        return HttpRelationData(
            url=typing.cast(str, relation_data.get("url")),
        )

    def _is_relation_data_valid(self, relation: Relation) -> bool:
        """Validate the relation data.

        Args:
            relation: the relation to validate.

        Returns:
            true: if the relation data is valid.
        """
        try:
            _ = self._get_relation_data_from_relation(relation)
            return True
        except ValidationError as ex:
            error_fields = [error["loc"] for error in ex.errors()]
            error_field_str = " ".join(f"{f}" for f in error_fields)
            logger.warning("Error validation the relation data %s", error_field_str)
            return False


class HTTPRequirer(_IntegrationInterfaceBaseClass):
    """HTTP interface provider class to be instantiated by the haproxy-operator charm.

    Attrs:
        on: Custom events that are used to notify the charm using the provider.
    """

    on = HTTPRequirerEvents()

    def __init__(self, charm: CharmBase, relation_name: str):
        super().__init__(charm, relation_name)

    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Handle relation-joined event.

        Args:
            event: relation-joined event.
        """
        logger.info(f"{event.relation.name} relation joined")
        # here we do nothing because after relation-joined there's always a
        # relation-changed event, where we will do the processing

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handle relation-changed event.
        Is triggered always after a relation-joined event.
        This emits the http_backend_available event that the charm code can
        listen to and act upon.

        Args:
            event: relation-changed event.
        """

        assert event.relation.app
        relation_data = event.relation.data[event.relation.app]
        if relation_data:
            if self._is_relation_data_valid(event.relation):
                self.on.http_backend_available.emit(event.relation, app=event.app, unit=event.unit)

    def _on_relation_broken(self, event: RelationBrokenEvent) -> None:
        """Handle relation-broken event.

        Args:
            event: relation-broken event.
        """
        self.on.http_backend_removed.emit(
            event.relation,
            app=event.app,
            unit=event.unit,
        )


class HTTPProvider(_IntegrationInterfaceBaseClass):
    """HTTP interface provider class to be instantiated by the haproxy-operator charm."""

    def __init__(
        self,
        charm: CharmBase,
        url,
        relation_name = HTTP_INTERFACE_RELATION,
    ):
        super().__init__(charm, relation_name)
        self.url = url

    def _update_relation_data(self, event: RelationEvent) -> None:
        if self.model.unit.is_leader():
            relation_data = HttpRelationData(url=self.url).to_relation_data()
            event.relation.data[self.charm.model.app].update(relation_data)
            logger.info(f"{event.relation.name} - Add to app data {PROVIDER_URL_KEY}: {self.url}")
        else:
            logger.warning(f"{self.relation_name} - Leader = {self.model.unit.is_leader()}, Relations = {self.relations}")

    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Handle relation joined event.
        When a new unit joins the relation, the HTTPProvider writes in
        the application databag its hostname and port.

        Args:
            event: relation-joined event.
        """
        self._update_relation_data(event)

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handle relation-changed event.
        When the relation changes, the HTTPProvider writes in
        the application databag its hostname and port.

        Args:
            event: relation-changed event.
        """
        self._update_relation_data(event)

    def _on_relation_broken(self, event: RelationBrokenEvent) -> None:
        """Handle relation-broken event.
        Empty the application databag.

        Args:
            event: relation-broken event.
        """
        if self.model.unit.is_leader():
            relation_data = HttpRelationData(url="").to_relation_data()
            event.relation.data[self.charm.model.app].update(relation_data)
            logger.info(f"Removed {event.relation.name} data for app")
