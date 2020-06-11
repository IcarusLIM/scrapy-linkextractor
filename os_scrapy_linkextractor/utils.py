import asyncio

from twisted.internet import defer


def as_deferred(f):
    return defer.Deferred.fromFuture(asyncio.ensure_future(f))
