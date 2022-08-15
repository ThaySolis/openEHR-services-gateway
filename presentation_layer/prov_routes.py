from requests import Session
from flask import Blueprint

from data_layer import path_utils
from data_layer.flask_proxy import FlaskProxy
from data_layer.ssl_extension import HostNameIgnoringAdapter
from business_layer.timing import timed, GET_PROVENANCE_MEASUREMENT
from app_settings import PROV_API_BASE_URI, VALIDATE_PROV_API_CERTIFICATE, USE_CUSTOM_PROV_API_CA_CERTIFICATE

blueprint = Blueprint("PROV routes", __name__)

base_uri = PROV_API_BASE_URI
validate_certificate = VALIDATE_PROV_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_PROV_API_CA_CERTIFICATE

prov_session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            prov_session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "prov_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

proxy = FlaskProxy(blueprint, PROV_API_BASE_URI, session=prov_session, extra_params=extra_params)

@proxy.redirect("/provenance/service?target=<target>", methods=["GET"], decorators=[ timed.measure(GET_PROVENANCE_MEASUREMENT) ])
def get_provenance(response):
    """
    Gets the provenance of a resource.
    """
    return response
