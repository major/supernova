# Troubleshooting

Sometimes bad things happen.  This guide contains some commonly seen issues and fixes for them.

## Deprecated novaclient warning
When connecting to some API's you may see a warning like this:

```html
/home/major/.venv/lib/python2.7/site-packages/novaclient/v1_1/__init__.py:30: UserWarning: Module novaclient.v1_1 is deprecated (taken as a basis for novaclient.v2). The preferable way to get client class or object you can find in novaclient.client module.
  warnings.warn("Module novaclient.v1_1 is deprecated (taken as a basis for "
```

Many OpenStack clouds still use version 1.1 of the nova API.  Feel free to ignore this warning for now.

## subjectAltName warning

```html
/home/major/.venv/lib/python2.7/site-packages/requests/packages/urllib3/connection.py:251: SecurityWarning: Certificate has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/shazow/urllib3/issues/497 for details.)
```

This warning means that the API endpoint that you're connecting to isn't offering a certificate with a [subjectAltName OID](https://en.wikipedia.org/wiki/SubjectAltName).  This means the certificate is probably a little older than most but it doesn't have an impact of the security of the connection.
