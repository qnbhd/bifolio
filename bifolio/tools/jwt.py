from functools import wraps

from sanic.response import redirect
from sanic.views import HTTPMethodView

# noinspection PyProtectedMember
from sanic_jwt.decorators import _do_protection


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
