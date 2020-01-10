from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
import trackermaps.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                trackermaps.routing.websocket_urlpatterns
            )
        ),
    )
})
