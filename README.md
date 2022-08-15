# OpenEHR proxy service

> This project is part of Thayse Marques Solis' masters project, yet to be released.

This project is an implementation of a web service which receives requests according to the OpenEHR, demographic and PROV APIs and redirects them to the right services.

## Running locally

In order to run this service locally, you must first create the Python virtual environment:

```bash
python3 -m venv venv
```

Then, after activating the virtual environment, you must install all requirements.

```bash
pip install -r requirements.txt
```

Finally, you may run the Python application:

```bash
python app.py
```

## Environment variables

In order to run this application, the environment variables described in this section must be set.

> The `.env` file is provided with sample values for these variables.

### PROV API settings

- `PLAIN_HTTP`: if `yes`, the server will run in HTTP mode, else it will run in HTTPS mode.
- `SERVER_PORT`: the port that will receive incoming HTTP requests.
- `INCLUDE_USAGE_STATISTICS`: if `yes`, the server will collect usage statistics and provide an additional route `/usage_statistics` to get usage statistics.
- `USAGE_STATISTICS_MAX_SAMPLES`: the maximum number of timing samples collected for the usage statistics.

### OpenEHR API access settings

- `OPENEHR_API_BASE_URI`: the private URI used to access the openEHR API.
- `VALIDATE_OPENEHR_API_CERTIFICATE`: if `yes`, the SSL certificate of the openEHR API will be validated (this setting has no effect if the openEHR API uses HTTP).
- `USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE`: if `yes`, the root CA certificate of the certification chain of the openEHR API will be validated based on the file `other_certificates/openehr_api_ca_certificate.pem`.

### Demographic API access settings

- `DEMOGRAPHIC_API_BASE_URI`: the private URI used to access the demographic API.
- `VALIDATE_DEMOGRAPHIC_API_CERTIFICATE`: if `yes`, the SSL certificate of the demographic API will be validated (this setting has no effect if the demographic API uses HTTP).
- `USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE`: if `yes`, the root CA certificate of the certification chain of the demographic API will be validated based on the file `other_certificates/demographic_api_ca_certificate.pem`.

### PROV API access settings

- `PROV_API_BASE_URI`: the private URI used to access the PROV API.
- `VALIDATE_PROV_API_CERTIFICATE`: if `yes`, the SSL certificate of the PROV API will be validated (this setting has no effect if the PROV API uses HTTP).
- `USE_CUSTOM_PROV_API_CA_CERTIFICATE`: if `yes`, the root CA certificate of the certification chain of the PROV API will be validated based on the file `other_certificates/prov_api_ca_certificate.pem`.
