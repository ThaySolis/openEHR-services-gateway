import requests
import inspect

from flask import request, Response

from .relative_url_pattern import RelativeURLPattern

class FlaskProxy:
    def __init__(self, app, remote_base_url, session=None, extra_params=None):
        self._app = app
        self._remote_base_url = remote_base_url
        self._session = session
        self._extra_params = {} if extra_params is None else extra_params

    def redirect(self, local_url, target_url=None, methods=["GET"], decorators=[]):
        """
        Decorates the function as a Flask route handler which redirects to a remote service.

        The decorated function must take a single positional argument and may receive additional arguments.
        """

        if target_url is None:
            target_url = local_url

        local_relative_url = RelativeURLPattern(local_url)
        remote_relative_url = RelativeURLPattern(target_url)

        def proxy_decorator(fn):
            sig = inspect.signature(fn)
            params = sig.parameters.values()
            has_kwargs = any([True for p in params if p.kind == p.VAR_KEYWORD])

            def handle_request(**path_params):
                # clone all arguments from path and query string.
                params = path_params.copy()
                query_string = request.args.to_dict()
                for key in query_string:
                    variable_name = local_relative_url.query_string_variable_from_key(key)
                    if variable_name is not None:
                        params[variable_name] = query_string[key]

                # send request to remote system.
                remote_url = self._remote_base_url + remote_relative_url.replace(**params)
                requester = requests
                if self._session is not None:
                    requester = self._session
                resp = requester.request(
                    method=request.method,
                    url=remote_url,
                    headers={key: value for (key, value) in request.headers if key != 'Host'},
                    data=request.get_data(),
                    cookies=request.cookies,
                    allow_redirects=False,
                    **self._extra_params)

                # create Flask-style response object.
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
                response = Response(resp.content, resp.status_code, headers)

                if has_kwargs:
                    return fn(response, **params)
                else:
                    return fn(response)

            handle_request.__name__ = fn.__name__

            decorated = handle_request
            for decorator in decorators:
                decorated = decorator(decorated)

            flask_decorator = self._app.route(local_relative_url.path_pattern, methods=methods)
            return flask_decorator(decorated)

        return proxy_decorator

    def __repr__(self):
        return '<FlaskProxy>'