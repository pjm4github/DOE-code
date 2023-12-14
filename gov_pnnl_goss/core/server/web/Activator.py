
from gov_pnnl_goss.SpecialClasses import Filter, HttpService, HttpContext, Hashtable
from gov_pnnl_goss.core.security.impl.Activator import DependencyActivatorBase, SecurityManager
from gov_pnnl_goss.core.server.TokenIdentifierMap import TokenIdentifierMap
from gov_pnnl_goss.core.server.impl.PooledSqlServiceFactory import DependencyManager
from gov_pnnl_goss.core.server.web.LoggedInFilter import LoggedInFilter
from gov_pnnl_goss.core.server.web.LoginService import LoginService
from gov_pnnl_goss.core.server.web.LoginTestService import LoginTestService
from gov_pnnl_goss.core.server.web.XDomainFilter import XDomainFilter


class Activator(DependencyActivatorBase):

    WEB_CONFIG_PID = "pnnl.goss.core.server.web"

    def __init__(self, context, manager):
        self.init(context, manager)

    def init(self, context, manager: DependencyManager):
        xDomainProps = Hashtable()
        xDomainProps.put("pattern", ".*")
        xDomainProps.put("service.ranking", 10)

        loggedInFilterProps = Hashtable()
        loggedInFilterProps.put("pattern", ".*\\api\\/.\\A.*")
        loggedInFilterProps.put("contextId", "GossContext")

        contextWrapperProps = Hashtable()
        contextWrapperProps.put("contextId", "GossContext")
        contextWrapperProps.put("context.shared", True)

        httpRef = context.getServiceReference(HttpService)
        httpService = context.getService(httpRef)

        if httpService is None:
            raise Exception("HttpService not available.")

        self.manager.add(
            self.createComponent()
                .setInterface(HttpContext.getName(), contextWrapperProps)
                .setImplementation(httpService.createDefaultHttpContext())
        )

        self.manager.add(
            self.createComponent()
                .setInterface(Filter.getName(), xDomainProps)
                .setImplementation(XDomainFilter)
        )

        self.manager.add(
            self.createComponent()
                .setInterface(Filter.getName(), loggedInFilterProps)
                .setImplementation(LoggedInFilter)
                .add(
                    self.createServiceDependency()
                        .setService(TokenIdentifierMap)
                )
        )

        self.manager.add(
            self.create_component()
                .setInterface(LoginService.getName(), None)
                .setImplementation(LoginService)
                .add(
                    self.createServiceDependency()
                        .setService(SecurityManager)
                )
                .add(
                    self.createServiceDependency()
                        .setService(TokenIdentifierMap)
                )
        )

        self.manager.add(
            self.create_component()
                .setInterface(LoginTestService.getName(), None)
                .setImplementation(LoginTestService)
        )

    def destroy(self, context, manager: DependencyManager):
        pass
