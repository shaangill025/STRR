#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
STRR Data Portal API Resource.
"""

import logging
from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from strr_api.common.auth import jwt
from strr_api.enums.enum import RegistrationStatus, Role
from strr_api.exceptions import error_response, exception_response
from strr_api.models import Registration, RentalProperty

logger = logging.getLogger("api")
bp = Blueprint("dataportal", __name__)


@bp.route("<registration_number>", methods=("GET",))
@swag_from({"security": [{"Bearer": []}]})
@cross_origin(origin="*")
@jwt.requires_auth
@jwt.has_one_of_roles([Role.STRR_EXAMINER.value, Role.SYSTEM.value])
def get_registration_data(registration_number):
    """
    Get registration data for a registration number.
    ---
    tags:
      - data-portal
    parameters:
      - in: path
        name: registration_number
        type: string
        required: true
        description: Registration Number
    responses:
      200:
        description:
      400:
        description:
      401:
        description:
      403:
        description:
      502:
        description:
    """
    try:
        registration = Registration.query.filter_by(registration_number=registration_number).first()
        if not registration:
            return error_response(HTTPStatus.NOT_FOUND, "Registration not found")
        rental_property = RentalProperty.query.filter_by(registration_id=registration.id).first()
        primary_contact = next((contact for contact in rental_property.contacts if contact.is_primary), None)
        response_data = {
            "registrationNumber": registration.registration_number,
            "status": registration.status.value,
            "dateOfRegistration": registration.start_date.isoformat(),
            "dateOfExpiration": registration.expiry_date.isoformat(),
            "propertyHostInformation": {
                "firstName": primary_contact.contact.firstname if primary_contact else None,
                "middleName": primary_contact.contact.middlename if primary_contact else None,
                "lastName": primary_contact.contact.lastname if primary_contact else None,
                "preferredName": primary_contact.contact.preferredname if primary_contact else None,
                "phoneNumber": primary_contact.contact.phone_number if primary_contact else None,
                "email": primary_contact.contact.email if primary_contact else None,
                "mailingAddress": primary_contact.contact.address.to_oneline_address()
                if primary_contact and primary_contact.contact.address
                else None,
            },
            "strPropertyInformation": {
                "nickname": rental_property.nickname,
                "rentalUnitAddress": rental_property.address.to_oneline_address() if rental_property.address else None,
                "pid": rental_property.parcel_identifier,
                "localGovernmentBusinessLicence": rental_property.local_business_licence,
                "localGovernmentBusinessLicenceExpiryDate": (
                    rental_property.local_business_licence_expiry_date.isoformat()
                    if rental_property.local_business_licence_expiry_date
                    else None
                ),
                "ownershipType": rental_property.ownership_type.value,
                "rentalType": "Entire Home" if rental_property.is_principal_residence else "Shared Accommodation",
                "rentalTypeDetails": rental_property.property_type.value,
                "platformURLs": [listing.url for listing in rental_property.property_listings],
            },
            "principalResidenceRequirement": {
                "exemptionReason": rental_property.pr_exempt_reason,
                "exemptionCategory": rental_property.service_provider,
            },
        }
        return jsonify(response_data), HTTPStatus.OK
    except Exception as exception:
        return exception_response(exception)


@bp.route("/registration-numbers", methods=("GET",))
@swag_from({"security": [{"Bearer": []}]})
@cross_origin(origin="*")
@jwt.requires_auth
@jwt.has_one_of_roles([Role.STRR_EXAMINER.value, Role.SYSTEM.value])
def get_registration_numbers():
    """
    Return list of active registration numbers.
    ---
    tags:
      - data-portal
    parameters:
      - in: query
        name: status
        enum: [ACTIVE, EXPIRED, SUSPENDED, CANCELLED]
        description: Registration Status Filter.
    responses:
      204:
        description:
      401:
        description:
      403:
        description:
      502:
        description:
    """

    try:
        status = request.args.get("status")
        if status not in ["ACTIVE", "EXPIRED", "SUSPENDED", "CANCELLED"]:
            return error_response(HTTPStatus.BAD_REQUEST, "Registration status not found")
        if not status:
            status = "ACTIVE"
        status_enum = RegistrationStatus[status.upper()]
        active_registrations = Registration.query.filter_by(status=status_enum).all()
        registration_numbers = [reg.registration_number for reg in active_registrations]
        response_data = {"registration_numbers": registration_numbers}
        return jsonify(response_data), HTTPStatus.OK
    except Exception as exception:
        return exception_response(exception)
