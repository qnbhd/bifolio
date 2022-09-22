"""Module contains the main web-application for bifolio."""

from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic_ext import validate
from sanic_openapi import doc
from sanic_openapi import openapi2_blueprint

from bifolio.models import Item


app = Sanic("bifolio")
app.blueprint(openapi2_blueprint)

app.config["API_VERSION"] = "0.0.1"
app.config["API_TITLE"] = "BiFolio"
app.config["API_LICENSE_NAME"] = "MIT"
app.config["API_CONTACT_EMAIL"] = "1qnbhd@gmail.com"
app.config["API_DESCRIPTION"] = (
    "BiFolio is a web-application"
    " for tracking your crypto-portfolio."
)
app.config["OAS_IGNORE_HEAD"] = True
app.config["OAS_IGNORE_OPTIONS"] = True


@app.get("/hello")
async def hello(request):
    """This is a simple hello-world handler."""

    return text("Hello, world!")


@app.get("/hello/<name:str>")
async def hello_name(request, name: str):
    """This is a simple hello-world handler with a name."""

    return text(f"Hello, {name}!")


@app.get("/query")
@doc.summary("This is a simple query handler.")
async def query_param_endpoint(request):
    """This is a simple query handler."""

    return json({"query": request.args.get("param")})


@app.post("/with/body")
@doc.summary("This is a simple body handler.")
@validate(json=Item)
async def body_param_endpoint(request, body: Item):
    """This is a simple body handler."""

    return text(f"Body: {body}")


if __name__ == "__main__":
    app.run(auto_reload=True)
