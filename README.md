# sanic-useragent

Add `user_agent` to request for Sanic.

## Installation

`pip install sanic-useragent`

## Usage

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic
from sani.response import json
from sanic_useragent import SanicUserAgent

app = Sanic(__name__)

SanicUserAgent.init_app(app)
# or pass default_locale
# SanicUserAgent.init_app(app, default_locale='en_US')
# or define DEFAULT_LOCALE in app.config
# SanicUserAgent.init_app(app)

@app.route('/')
async def index(request):
    return json(request['user_agent'].to_dict())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

```
