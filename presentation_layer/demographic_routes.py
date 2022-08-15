from requests import Session
from flask import Blueprint

from data_layer import path_utils
from data_layer.flask_proxy import FlaskProxy
from data_layer.ssl_extension import HostNameIgnoringAdapter
from business_layer.timing import timed, CREATE_PATIENT_MEASUREMENT, UPDATE_PATIENT_MEASUREMENT, DELETE_PATIENT_MEASUREMENT, GET_PATIENT_MEASUREMENT, GET_VERSIONED_PATIENT_MEASUREMENT, GET_VERSIONED_PATIENT_REVISION_HISTORY_MEASUREMENT, GET_VERSIONED_PATIENT_VERSION_MEASUREMENT, LIST_PATIENTS_MEASUREMENT, GET_EHR_ID_FROM_PATIENT_MEASUREMENT, SET_EHR_ID_FROM_PATIENT_MEASUREMENT, GET_CONTRIBUTION_OF_PATIENT_MEASUREMENT
from app_settings import DEMOGRAPHIC_API_BASE_URI, VALIDATE_DEMOGRAPHIC_API_CERTIFICATE, USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE

blueprint = Blueprint("Demographic routes", __name__)

base_uri = DEMOGRAPHIC_API_BASE_URI
validate_certificate = VALIDATE_DEMOGRAPHIC_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE

demographic_session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            demographic_session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "demographic_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

proxy = FlaskProxy(blueprint, DEMOGRAPHIC_API_BASE_URI, session=demographic_session, extra_params=extra_params)

@proxy.redirect("/v1/patient", methods=["POST"], decorators=[ timed.measure(CREATE_PATIENT_MEASUREMENT) ])
def create_patient(response):
    """
    Creates a new versioned patient (VERSIONED_PARTY) and its first version.
    """
    return response

@proxy.redirect("/v1/patient/<versioned_object_uid>", methods=["PUT"], decorators=[ timed.measure(UPDATE_PATIENT_MEASUREMENT) ])
def update_patient(response):
    """
    Updates the data of a patient identified by versioned_object_uid. If the request body already contains a PERSON.uid.value, it must match the versioned_object_uid in the URL. The existing latest version_uid of the PERSON resource (i.e the preceding_version_uid) must be specified in the If-Match header.
    """
    return response

@proxy.redirect("/v1/patient/<preceding_version_uid>", methods=["DELETE"], decorators=[ timed.measure(DELETE_PATIENT_MEASUREMENT) ])
def delete_patient(response):
    """
    Deletes the patient identified by preceding_version_uid
    """
    return response

@proxy.redirect("/v1/patient/<versioned_object_uid>?version_at_time=<version_at_time>", methods=["GET"], decorators=[ timed.measure(GET_PATIENT_MEASUREMENT) ])
def get_patient(response):
    """
    Retrieves a version of the patient identified by versioned_object_uid. If version_at_time is supplied, retrieves the version extant at specified time, otherwise retrieves the latest patient version.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>", methods=["GET"], decorators=[ timed.measure(GET_VERSIONED_PATIENT_MEASUREMENT) ])
def get_versioned_patient(response):
    """
    Retrieves a VERSIONED_PARTY identified by versioned_object_uid.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/revision_history", methods=["GET"], decorators=[ timed.measure(GET_VERSIONED_PATIENT_REVISION_HISTORY_MEASUREMENT) ])
def get_versioned_patient_revision_history(response):
    """
    Retrieves the revision history of the VERSIONED_PARTY identified by versioned_object_uid.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/version/<version_uid>", methods=["GET"], decorators=[ timed.measure(GET_VERSIONED_PATIENT_VERSION_MEASUREMENT) ])
def get_versioned_patient_version_by_id(response):
    """
    Retrieves a VERSION identified by version_uid of a VERSIONED_PARTY identified by versioned_object_uid.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/version?version_at_time=<version_at_time>", methods=["GET"], decorators=[ timed.measure(GET_VERSIONED_PATIENT_VERSION_MEASUREMENT) ])
def get_versioned_patient_version_at_time(response):
    """
    Retrieves a VERSION from the VERSIONED_PARTY identified by versioned_object_uid. If version_at_time is supplied, retrieves the VERSION extant at specified time, otherwise retrieves the latest VERSION.
    """
    return response

@proxy.redirect("/v1/patient", methods=["GET"], decorators=[ timed.measure(LIST_PATIENTS_MEASUREMENT) ])
def list_patients(response):
    """
    Lists the IDs of all the patients in the system.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/ehr", methods=["GET"], decorators=[ timed.measure(GET_EHR_ID_FROM_PATIENT_MEASUREMENT) ])
def get_ehr_id_from_patient(response):
    """
    Retrieves the EHR identifier associated with a given patient.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/ehr", methods=["PUT"], decorators=[ timed.measure(SET_EHR_ID_FROM_PATIENT_MEASUREMENT) ])
def set_ehr_id_of_patient(response):
    """
    Sets the EHR identifier associated with a given patient.
    """
    return response

@proxy.redirect("/v1/versioned_patient/<versioned_object_uid>/contribution/<contribution_uid>", methods=["GET"], decorators=[ timed.measure(GET_CONTRIBUTION_OF_PATIENT_MEASUREMENT) ])
def get_contribution(response):
    """
    Retrieves a contribution of a given patient.
    """
    return response
