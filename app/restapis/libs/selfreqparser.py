from flask_restful.reqparse import Argument, RequestParser
from flask import request, current_app
from werkzeug import exceptions
from app.handler.http_handler import self_abort
import six


class SelfArgument(Argument):

    def handle_validation_error(self, error, bundle_errors):
        """Called when an error is raised while parsing. Aborts the request
        with a 400 status and an error message

        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        if 'required' in error_msg:
            err_code = 404
            msg = f"{self.name} {error_msg}"
        else:
            err_code = 500
            msg = f"{self.name} {error_msg}"

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        self_abort(err_code, msg)


class SelfRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.argument_class = SelfArgument

    def parse_args(self, req=None, strict=False, error_code=400):
        """Parse all arguments from the provided request and return the results
        as a Namespace

        :param req: Can be used to overwrite request from Flask
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        :param http_error_code: use custom error code for `flask_restful.abort()`
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            self_abort(error_code, str(errors))
            # print(errors, '---------------------')
            # self_abort(error_code, "{field} {error}".format(field=field, error=error))
            # flask_restful.abort(http_error_code, message=errors)

        if strict and req.unparsed_arguments:
            pass
            # raise exceptions.BadRequest('Unknown arguments: %s'
            #                             % ', '.join(req.unparsed_arguments.keys()))

        return namespace