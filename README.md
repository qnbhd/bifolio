## BiFolio
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&vCenter=true&width=500&height=40&lines=BiFolio+-+your+crypto+portfolio+tracker)](https://git.io/typing-svg)


BiFolio - web-service for tracking your crypto-portfolio.

Functional possibilities:

- Create account / login / logout;
- Make transactions for ETH, BTC;
- See portfolio charts, your holdings;
- Make many portfolios

In this MR was implemented:

- some blueprints;
- frontend, pages: login, signup, profile, home (empty) pages;
- tests for domain logic - crypto portfolio tracking;
- secure elements: headers, cors, ..., j2 configuration

CI tests: linters, checks, run tests.

### Profile form:

<details>

<img width="1262" alt="image" src="https://user-images.githubusercontent.com/6369915/192570921-981867c4-65c3-40c6-b2c1-3ac61b80aec1.png">

</details>

### Login form

<details>

<img width="1262" alt="image" src="https://user-images.githubusercontent.com/6369915/192571064-2b6be1b9-d9fb-4b04-9783-972e20fc1cb3.png">

</details>

### Make transaction modal form

<details>

<img width="1105" alt="image" src="https://user-images.githubusercontent.com/6369915/192575348-0c6ac68e-c5af-4304-8d8e-c70f1b03da46.png">


</details>

Needed services:

- Some db, for example SQLite;
- Redis / MemCache storage.

## Installation

You need have installed python >= 3.8.0.

For regular use, you can install BiFolio dependencies with:

```bash
pip install -r requirements.txt
```

For development, you can install BiFolio dependencies with:

```bash
pip install -r requirements-dev.txt
```

## Usage:

```bash
python3 server.py
```

Sanic has a built-in web server, so you can use it for production and development.

## Documentation

You can check the documentation on `/docs` endpoint.

## Tests

For run tests you can use:

```bash
pytest
```

## License

BiFolio is licensed under the MIT License. See [LICENSE](LICENSE) for the full license text.
