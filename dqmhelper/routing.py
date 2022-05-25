from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
import remotescripts.routing

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(remotescripts.routing.websocket_urlpatterns)),
        )
    }
)
