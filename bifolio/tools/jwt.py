from functools import wraps
from urllib.parse import urlparse

import aiohttp as aiohttp
from sanic import Blueprint
from sanic.response import redirect
from sanic.views import HTTPMethodView

# noinspection PyProtectedMember
from sanic_jwt.decorators import _do_protection
from sanic_jwt.decorators import instant_config
import sanic_jwt.utils as utils


# Temporary bad solution for blacklisting tokens
# ISSUE: https://github.com/ahopkins/sanic-jwt/issues/152
def protected_sec(
    initialized_on=None, redirect_to="account.login", **kw
):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if issubclass(request.__class__, HTTPMethodView):
                request = args[0]
            kwargs.update(
                {
                    "initialized_on": initialized_on,
                    "kw": kw,
                    "request": request,
                    "f": f,
                }
            )

            redis = request.app.ctx.redis
            access_token = request.cookies.get("access_token")
            in_blacklist = await redis.exists(
                f"blacklist:{access_token}"
            )

            if in_blacklist:
                return redirect(request.app.url_for(redirect_to))

            return await _do_protection(*args, **kwargs)

        return decorated_function

    return decorator


def inject_user_sec(initialized_on=None, **kw):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if issubclass(request.__class__, HTTPMethodView):
                request = args[0]

            if initialized_on and isinstance(
                initialized_on, Blueprint
            ):  # noqa
                instance = initialized_on
            else:
                instance = request.app

            with instant_config(instance, request=request, **kw):
                if request.method == "OPTIONS":
                    return await utils.call(
                        f, request, *args, **kwargs
                    )  # noqa

                payload = await instance.ctx.auth.extract_payload(
                    request, verify=False
                )

                redis = request.app.ctx.redis
                access_token = request.cookies.get("access_token")
                in_blacklist = await redis.exists(
                    f"blacklist:{access_token}"
                )

                if in_blacklist:
                    return await f(
                        request, user=None, *args, **kwargs
                    )

                user = await utils.call(
                    instance.ctx.auth.retrieve_user, request, payload
                )
                response = f(request, user=user, *args, **kwargs)
                return await response

        return decorated_function

    return decorator
