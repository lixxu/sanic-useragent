#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    werkzeug.useragents
    ~~~~~~~~~~~~~~~~~~~

    This module provides a helper to inspect user agent strings.  This module
    is far from complete but should work for most of the currently available
    browsers.


    :copyright: (c) 2014 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import re


class UserAgentParser:

    """A simple user agent parser.  Used by the `UserAgent`."""

    platforms = (
        ('cros', 'chromeos'),
        ('iphone|ios', 'iphone'),
        ('ipad', 'ipad'),
        (r'darwin|mac|os\s*x', 'macos'),
        ('win', 'windows'),
        (r'android', 'android'),
        (r'x11|lin(\b|ux)?', 'linux'),
        ('(sun|i86)os', 'solaris'),
        (r'nintendo\s+wii', 'wii'),
        ('irix', 'irix'),
        ('hp-?ux', 'hpux'),
        ('aix', 'aix'),
        ('sco|unix_sv', 'sco'),
        ('bsd', 'bsd'),
        ('amiga', 'amiga'),
        ('blackberry|playbook', 'blackberry'),
        ('symbian', 'symbian')
    )
    browsers = (
        ('googlebot', 'google'),
        ('msnbot', 'msn'),
        ('yahoo', 'yahoo'),
        ('ask jeeves', 'ask'),
        (r'aol|america\s+online\s+browser', 'aol'),
        ('opera', 'opera'),
        ('chrome', 'chrome'),
        ('firefox|firebird|phoenix|iceweasel', 'firefox'),
        ('galeon', 'galeon'),
        ('safari|version', 'safari'),
        ('webkit', 'webkit'),
        ('camino', 'camino'),
        ('konqueror', 'konqueror'),
        ('k-meleon', 'kmeleon'),
        ('netscape', 'netscape'),
        (r'msie|microsoft\s+internet\s+explorer|trident/.+? rv:', 'msie'),
        ('lynx', 'lynx'),
        ('links', 'links'),
        ('seamonkey|mozilla', 'seamonkey')
    )

    _browser_version_re = r'(?:%s)[/\sa-z(]*(\d+[.\da-z]+)?'
    _language_re = re.compile(
        r'(?:;\s*|\s+)(\b\w{2}\b(?:-\b\w{2}\b)?)\s*;|'
        r'(?:\(|\[|;)\s*(\b\w{2}\b(?:-\b\w{2}\b)?)\s*(?:\]|\)|;)'
    )

    def __init__(self):
        self.platforms = [(b, re.compile(a, re.I)) for a, b in self.platforms]
        self.browsers = [(b, re.compile(self._browser_version_re % a, re.I))
                         for a, b in self.browsers]

    def __call__(self, headers):
        user_agent = headers.get('user-agent', '')
        if user_agent:
            for platform, regex in self.platforms:
                match = regex.search(user_agent)
                if match is not None:
                    break

            else:
                platform = None

            for browser, regex in self.browsers:
                match = regex.search(user_agent)
                if match is not None:
                    version = match.group(1)
                    break

            else:
                browser = version = None

            match = self._language_re.search(user_agent)
            if match is not None:
                language = match.group(1) or match.group(2)
            else:
                language = None

        else:
            platform = browser = version = language = None

        return platform, browser, version, language


class UserAgent:

    """Represents a user agent.  Pass it a Sanic request.headers
    string and you can inspect some of the details from the user agent
    string via the attributes.  The following attributes exist:

    .. attribute:: string

       the raw user agent string

    .. attribute:: platform

       the browser platform.  The following platforms are currently
       recognized:

       -   `aix`
       -   `amiga`
       -   `android`
       -   `bsd`
       -   `chromeos`
       -   `hpux`
       -   `iphone`
       -   `ipad`
       -   `irix`
       -   `linux`
       -   `macos`
       -   `sco`
       -   `solaris`
       -   `wii`
       -   `windows`

    .. attribute:: browser

        the name of the browser.  The following browsers are currently
        recognized:

        -   `aol` *
        -   `ask` *
        -   `camino`
        -   `chrome`
        -   `firefox`
        -   `galeon`
        -   `google` *
        -   `kmeleon`
        -   `konqueror`
        -   `links`
        -   `lynx`
        -   `msie`
        -   `msn`
        -   `netscape`
        -   `opera`
        -   `safari`
        -   `seamonkey`
        -   `webkit`
        -   `yahoo` *

        (Browsers maked with a star (``*``) are crawlers.)

    .. attribute:: version

        the version of the browser

    .. attribute:: language

        the language of the browser

    .. attribute:: locale
        the closest language of the user agent for translation

    .. attribute:: accept_languages
        the accepted languages list of the browser
    """

    _parser = UserAgentParser()

    def __init__(self, headers={}, default='en_US'):
        self.string = headers.get('user-agent', '')
        self.platform, self.browser, self.version, self.language = \
            self._parser(headers)
        self.accept_languages = self.get_browser_locale(headers)
        self._locale = self.get_locale(default)

    def get_browser_locale(self, headers):
        locales = []
        if 'accept-language' in headers:
            languages = headers['accept-language'].split(',')
            for language in languages:
                parts = language.strip().split(';')
                if len(parts) > 1 and parts[1].startswith('q='):
                    try:
                        score = float(parts[1][2:])
                    except (ValueError, TypeError):
                        score = 0.0

                else:
                    score = 1.0

                locales.append((parts[0], score))

            if locales:
                locales.sort(key=lambda pair: pair[1], reverse=True)

        return locales

    @property
    def locale(self):
        return self._locale

    def get_locale(self, default='en_US'):
        for l in self.accept_languages:
            parts = l[0].replace('-', '_').split('_')
            if len(parts) == 2:
                return parts[0].lower() + '_' + parts[1].upper()

        return default

    def to_dict(self):
        return dict(string=self.string,
                    platform=self.platform,
                    browser=self.browser,
                    version=self.version,
                    language=self.language,
                    locale=self.locale,
                    accept_languages=self.accept_languages,
                    )

    def to_header(self):
        return self.string

    def __str__(self):
        return self.string

    def __nonzero__(self):
        return bool(self.browser)

    __bool__ = __nonzero__

    def __repr__(self):
        return '<{} {!r}/{}>'.format(self.__class__.__name__,
                                     self.browser,
                                     self.version
                                     )


class SanicUserAgent:
    __locale__ = 'en_US'

    @classmethod
    def init_app(cls, app, default_locale=None):
        if not default_locale:
            default_locale = app.config.get('DEFAULT_LOCALE') or cls.__locale__

        @app.middleware('request')
        async def add_useragent(request):
            request.ctx.user_agent = UserAgent(request.headers, default_locale)
