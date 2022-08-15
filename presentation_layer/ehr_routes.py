from requests import Session
from flask import Blueprint

from data_layer import path_utils
from data_layer.flask_proxy import FlaskProxy
from data_layer.ssl_extension import HostNameIgnoringAdapter
from app_settings import OPENEHR_API_BASE_URI, VALIDATE_OPENEHR_API_CERTIFICATE, USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE

blueprint = Blueprint("OpenEHR routes", __name__)

base_uri = OPENEHR_API_BASE_URI
validate_certificate = VALIDATE_OPENEHR_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE

openehr_session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            openehr_session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "openehr_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

proxy = FlaskProxy(blueprint, OPENEHR_API_BASE_URI, session=openehr_session, extra_params=extra_params)

################# EHR #################

@proxy.redirect("/v1/ehr", methods=["POST"])
def create_ehr(response):
    """
    Create a new EHR with an auto-generated identifier.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr-ehr-post
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>", methods=["PUT"])
def create_ehr_with_id(response):
    """
    Create a new EHR with the specified ehr_id identifier.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr-ehr-put
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>", methods=["GET"])
def get_ehr_summary_by_id(response):
    """
    Retrieve the EHR with the specified ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr-ehr-get
    """
    return response

@proxy.redirect("/v1/ehr?subject_id=<subject_id>&subject_namespace=<subject_namespace>", methods=["GET"])
def get_ehr_summary_by_subject_id(response):
    """
    Retrieve the EHR with the specified subject_id and subject_namespace.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr-ehr-get-1
    """
    return response

################# EHR_STATUS #################

@proxy.redirect("/v1/ehr/<ehr_id>/ehr_status?version_at_time=<version_at_time>", methods=["GET"])
def get_EHR_STATUS_version_by_time(response):
    """
    Retrieves a version of the EHR_STATUS associated with the EHR identified by ehr_id

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-ehr_status-get
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/ehr_status/<version_uid>", methods=["GET"])
def get_EHR_STATUS_by_version_id(response):
    """
    Retrieves a particular version of the EHR_STATUS identified by version_uid and associated with the EHR identified by ehr_id

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-ehr_status-get-1
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/ehr_status", methods=["PUT"])
def update_EHR_STATUS(response):
    """
    Updates EHR_STATUS associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-ehr_status-put
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_ehr_status", methods=["GET"])
def get_versioned_EHR_STATUS(response):
    """
    Retrieves a VERSIONED_EHR_STATUS associated with an EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_ehr_status/revision_history", methods=["GET"])
def get_versioned_EHR_STATUS_revision_history(response):
    """
    Retrieves revision history of the VERSIONED_EHR_STATUS associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get-1
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_ehr_status/version?version_at_time=<version_at_time>", methods=["GET"])
def get_versioned_EHR_STATUS_version_by_time(response):
    """
    Retrieves a VERSION from the VERSIONED_EHR_STATUS associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get-2
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_ehr_status/version/<version_uid>", methods=["GET"])
def get_versioned_EHR_STATUS_version_by_id(response):
    """
    Retrieves a VERSION identified by version_uid of an EHR_STATUS associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get-3
    """
    return response

################# COMPOSITION #################

@proxy.redirect("/v1/ehr/<ehr_id>/composition", methods=["POST"])
def create_composition(response):
    """
    Creates the first version of a new COMPOSITION in the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-composition-post
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/composition/<versioned_object_uid>", methods=["PUT"])
def update_composition(response):
    """
    Updates COMPOSITION identified by versioned_object_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-composition-put
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/composition/<preceding_version_uid>", methods=["DELETE"])
def delete_composition(response):
    """
    Deletes the COMPOSITION identified by preceding_version_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-composition-delete
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/composition/<version_uid>", methods=["GET"])
def get_composition_by_version_id(response):
    """
    Retrieves a particular version of the COMPOSITION identified by version_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-composition-get
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/composition/<versioned_object_uid>?version_at_time=<version_at_time>", methods=["GET"])
def get_composition_at_time(response):
    """
    Retrieves a version of the COMPOSITION identified by versioned_object_uid and associated with the EHR identified by ehr_id.
    If version_at_time is supplied, retrieves the version extant at specified time, otherwise retrieves the latest COMPOSITION
    version.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-composition-get-1
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_composition/<versioned_object_uid>", methods=["GET"])
def get_versioned_composition(response):
    """
    Retrieves a VERSIONED_COMPOSITION identified by versioned_object_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_composition/<versioned_object_uid>/revision_history", methods=["GET"])
def get_versioned_composition_revision_history(response):
    """
    Retrieves revision history of the VERSIONED_COMPOSITION identified by versioned_object_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get-1
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_composition/<versioned_object_uid>/version/<version_uid>", methods=["GET"])
def get_versioned_composition_version_by_id(response):
    """
    Retrieves a VERSION identified by version_uid of a VERSIONED_COMPOSITION identified by versioned_object_uid and associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get-2
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/versioned_composition/<versioned_object_uid>/version?version_at_time=<version_at_time>", methods=["GET"])
def get_versioned_composition_version_at_time(response):
    """
    Retrieves a VERSION from the VERSIONED_COMPOSITION identified by versioned_object_uid and associated with the EHR identified
    by ehr_id. If version_at_time is supplied, retrieves the VERSION extant at specified time, otherwise retrieves the latest
    VERSION.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get-3
    """
    return response

################# DIRECTORY #################

@proxy.redirect("/v1/ehr/<ehr_id>/directory", methods=["POST"])
def create_directory(response):
    """
    Creates a new directory FOLDER associated with the EHR identified by ehr_id.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#directory-directory
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/directory", methods=["PUT"])
def update_directory(response):
    """
    Updates directory FOLDER associated with the EHR identified by ehr_id. The existing latest version_uid of directory FOLDER
    resource (i.e the preceding_version_uid) must be specified in the If-Match header.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#directory-directory-put
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/directory", methods=["DELETE"])
def delete_directory(response):
    """
    Deletes directory FOLDER associated with the EHR identified by ehr_id. The existing latest version_uid of directory FOLDER
    resource (i.e the preceding_version_uid) must be specified in the If-Match header.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#directory-directory-delete
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/directory/<version_uid>?path=<path>", methods=["GET"])
def get_folder_in_directory_version(response):
    """
    Retrieves a particular version of the directory FOLDER identified by version_uid and associated with the EHR identified by
    ehr_id. If path is supplied, retrieves from the directory only the sub-FOLDER that is associated with that path.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#directory-directory-get
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/directory?version_at_time=<version_at_time>&path=<path>", methods=["GET"])
def get_folder_in_directory_version_at_time(response):
    """
    Retrieves the version of the directory FOLDER associated with the EHR identified by ehr_id. If version_at_time is supplied,
    retrieves the version extant at specified time, otherwise retrieves the latest directory FOLDER version. If path is supplied,
    retrieves from the directory only the sub-FOLDER that is associated with that path.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#directory-directory-get-1
    """
    return response

################# CONTRIBUTION #################

@proxy.redirect("/v1/ehr/<ehr_id>/contribution", methods=["POST"])
def create_contribution(response):
    """
    We will use the relaxed CONTRIBUTION XSD with the following attributes optional:

    time_committed: server will always set it
    UID: if provided will be accepted unless it is already used in which case an error will be returned
    system_id: where provided will be validated

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#contribution-contribution-post
    """
    return response

@proxy.redirect("/v1/ehr/<ehr_id>/contribution/<contribution_uid>", methods=["GET"])
def get_contribution_by_id(response):
    """
    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#contribution-contribution-get
    """
    return response

################# QUERY #################

@proxy.redirect("/v1/query/aql?q=<q>&ehr_id=<ehr_id>&offset=<offset>&fetch=<fetch>&query_parameters=<query_parameters>", methods=["GET"])
def execute_ad_hoc_AQL_query(response):
    """
    Execute ad-hoc query, supplied by q parameter, fetching fetch numbers of rows from offset and passing query_parameters to the
    underlying query engine.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get
    """
    return response

@proxy.redirect("/v1/query/aql", methods=["POST"])
def execute_ad_hoc_AQL_query2(response):
    """
    Execute ad-hoc query, supplied by q parameter, fetching fetch numbers of rows from offset and passing query_parameters to the
    underlying query engine.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get
    """
    return response

@proxy.redirect("/v1/query/<qualified_query_name>/<version>?ehr_id=<ehr_id>&offset=<offset>&fetch=<fetch>&query_parameters=<query_parameters>", methods=["GET"])
def execute_stored_query(response):
    """
    Execute a stored query, identified by the supplied qualified_query_name (at specified version), fetching fetch numbers of rows
    from offset and passing query_parameters to the underlying query engine.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get-1
    """
    return response

@proxy.redirect("/v1/query/<qualified_query_name>/<version>", methods=["POST"])
def execute_stored_query2(response):
    """
    Execute a stored query identified by the supplied qualified_query_name (at specified version).

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-post-1
    """
    return response

################# ADL 1.4 TEMPLATE #################

@proxy.redirect("/v1/definition/template/adl1.4/", methods=["POST"])
def upload_template_1_4(response):
    """
    Upload a new ADL 1.4 operational template (OPT).

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-1.4-template-post
    """
    return response

@proxy.redirect("/v1/definition/template/adl1.4", methods=["GET"])
def list_templates_1_4(response):
    """
    List the available ADL 1.4 operational templates (OPT) on the system.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-1.4-template-post
    """
    return response

@proxy.redirect("/v1/definition/template/adl1.4/<template_id>", methods=["GET"])
def get_template_1_4(response):
    """
    Retrieves the ADL 1.4 operational template (OPT) identified by template_id identifier.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-1.4-template-post
    """
    return response

################# ADL 2 TEMPLATE #################

@proxy.redirect("/v1/definition/template/adl2/?version=<version>", methods=["POST"])
def upload_template_2(response):
    """
    Upload a new ADL2 operational template.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-2-template-post
    """
    return response

@proxy.redirect("/v1/definition/template/adl2", methods=["GET"])
def list_templates_2(response):
    """
    List the available ADL2 operational templates on the system.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-2-template-get
    """
    return response

@proxy.redirect("/v1/definition/template/adl2/<template_id>/<version_pattern>", methods=["GET"])
def get_template_2(response):
    """
    Retrieves the ADL2 operational template identified by template_id identifier.

If version_pattern is specified then the latest template version with given prefix pattern is returned. If version_pattern is omitted, then the latest version of the operational template is returned.
    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-2-template-get-1
    """
    return response

################# STORED QUERY #################

@proxy.redirect("/v1/definition/query/<qualified_query_name>", methods=["GET"])
def list_stored_queries(response):
    """
    Parameter qualified_query_name is optional. If omitted they are treated as “wildcards” in the search.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-stored-query-get
    """
    return response

@proxy.redirect("/v1/definition/query/<qualified_query_name>/<version>?type=<type>", methods=["PUT"])
def store_a_query(response):
    """
    Store a new query on the system.

    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-stored-query-put
    """
    return response

@proxy.redirect("/v1/definition/query/<qualified_query_name>/<version>", methods=["GET"])
def get_stored_query_and_metadata(response):
    """
    More info at: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-stored-query-get-1
    """
    return response
