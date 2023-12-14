
import base64
import concurrent.futures
import logging
import os
import random

from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossCoreConstants import GossCoreConstants
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.client.GossClient import Protocol
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import SimpleAccount
from gov_pnnl_goss.core.security.jwt.UnauthTokenBasedRealm import UnauthTokenBasedRealm
from gov_pnnl_goss.core.security.jwt.UserRepository import UserRepository
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


# from gov_pnnl_goss.gridappsd.app.AppManagerImpl import UsernamePasswordCredentials
# from gov_pnnl_goss.core.Client import PROTOCOL

# from java.util import Dictionary, Enumeration
# from pnnl.goss.core.security.jwt import UserDefault
# from pnnl.goss.core.security.jwt.realm import UnauthTokenBasedRealm
# from pnnl.goss.core.security.jwt.response_event import GossResponseEvent
# from java.io import Serializable
# from org.apache.shiro.util import SimpleAccount
# from org.apache.shiro.client import Client
# from org.apache.shiro.securequickrandom import SecureQuickRandom
# from org.apache.shiro.crypto import Base64, RandomNumberGenerator
# from org.apache.shiro.client import ClientFactory
# from org.apache.shiro.event import Start, ConfigurationDependency, ServiceDependency
# from org.apache.shiro.util import Client
# from org.apache.shiro.client.protocol import Protocol
# from org.apache.shiro.client.protocol import PROTOCOL
# from org.apache.shiro.config import ConfigurationDependency
# from org.apache.shiro.event.service.impl import DefaultSecurityEventPlugin
# from org.apache.shiro.util import ClientFactory, PROTOCOL_MANAGER, UsernamePasswordCredentials, PROTOCOL
# from org.apache.shiro.client.impl import DefaultClientFactory
# from org.apache.shiro.client.topic import GossCoreConstants




class UserRepositoryImpl(UserRepository):
    CONFIG_PID = "pnnl.goss.core.security.userfile"

    def __init__(self):
        self.logger = LogManager(UserRepositoryImpl.__name__)
        self.realm_name = UnauthTokenBasedRealm.get_class.__str__()
        self.user_map = concurrent.futures.ConcurrentHashMap()
        self.user_roles = concurrent.futures.ConcurrentHashMap()
        self.token_map = concurrent.futures.ConcurrentHashMap()
        self.client = None

    def start(self):
        try:
            self.client = ClientFactory.create(Protocol.STOMP,
                                               UsernamePasswordCredentials(SecurityConfig.get_manager_user(),
                                                                           SecurityConfig.get_manager_password()),
                                               False)
            self.client.publish("ActiveMQ.Advisory.Connection", "")
            login_topic = "/topic/" + GossCoreConstants.PROP_TOKEN_QUEUE
            self.client.subscribe(login_topic, ResponseEvent(self.client))
        except Exception as e:
            print(e)

    #@ConfigurationDependency(pid=CONFIG_PID)
    def updated(self, properties: dict) -> None:
        if properties is not None:
            self.logger.debug("Updating User Repository Impl")
            self.user_map.clear()
            self.user_roles.clear()

            keys = properties.keys()
            for k in keys:
                v = properties.get(k)
                cred_and_permissions = v.split(",")
                perms = set()
                acnt = SimpleAccount(k, cred_and_permissions[0], self.realm_name)
                for i in range(1, len(cred_and_permissions)):
                    acnt.add_string_permission(cred_and_permissions[i])
                    perms.add(cred_and_permissions[i])
                self.user_map.put(k, acnt)
                self.user_roles.put(k, perms)


class ResponseEvent(GossResponseEvent):

    def __init__(self, client):
        self.client = client

    def onMessage(self, response):
        self.logger.debug("Received token request")
        response_data = "{}"
        if isinstance(response, DataResponse):
            base64Auth = response.getData()
            user_auth_str = base64.b64decode(base64Auth).decode("utf-8")
            auth_arr = user_auth_str.split(":")
            user_id = auth_arr[0]
            if user_id in self.user_map and auth_arr[1] == self.user_map.get(user_id).get_credentials():
                token = self.token_map.get(user_id)
                if token is not None:
                    self.logger.debug("Token already exists for " + user_id)
                else:
                    token = SecurityConfig.create_token(auth_arr[0], self.user_roles.get(user_id))
                    self.logger.debug("Created token for " + user_id)
                    self.token_map.put(user_id, token)
                response_data = token
            else:
                self.logger.debug("Authentication failed for " + user_id)
                response_data = "authentication failed"
            self.logger.info("Returning token for user " + user_id + " on destination " + response.get_reply_destination())
            self.client.publish(response.get_reply_destination(), response_data)
        else:
            self.client.publish("goss/management/response", response_data)
