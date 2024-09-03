
from typing import Any, Union

from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.ProcessManagerComponentTests import GossResponseEvent


class Client:

    def get_response(self, request: Any, topic: str, response_format: Any) -> Union[str, None]:
        """
        Makes a synchronous call to the server.

        Args:
            request: The request object.
            topic: The topic to send the request to.
            response_format: The response format.

        Returns:
            The response as a serializable object or None.
        """
        pass

    def subscribe(self, topic_name: str, event: GossResponseEvent) -> None:
        """
        Lets the client subscribe to a Topic of the given name for event-based communication.

        Args:
            topic_name: The name of the topic to subscribe to.
            event: The event handler for receiving responses.

        Raises:
            SystemException: If there is an issue with the subscription.
        """
        pass

    def publish(self, topic_name: str, message: str) -> None:
        """
        Publishes a message to the specified topic.

        Args:
            topic_name: The name of the topic to publish the message to.
            message: The message to publish.

        Raises:
            SystemException: If there is an issue with publishing the message.

        alternately
            def publish(self, destination: str, data: str) -> None:
            Publishes a message to the specified destination.

            Args:
                destination: The destination to publish the message to.
                data: The data to publish.

            Raises:
                SystemException: If there is an issue with publishing the message.
        """
        pass

    def close(self) -> None:
        """
        Closes the connection with the server.
        """
        pass

    def get_protocol(self):
        """
        Gets the global_property_types of protocol that the client will use to connect with.

        Returns:
            The client protocol as a ClientProtocol enum value.
        """
        pass
