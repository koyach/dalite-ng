import base64
import hashlib
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse

from .utils import create_token, verify_token


def create_student_token(username, email, exp=timedelta(weeks=16)):
    assert isinstance(
        username, basestring
    ), "Precondition failed for `username`"
    assert isinstance(email, basestring), "Precondition failed for `email`"

    payload = {"username": username, "email": email}
    output = create_token(payload, exp=exp)

    assert isinstance(output, basestring), "Postcondition failed"
    return output


def verify_student_token(token):
    assert isinstance(token, basestring), "Precondition failed for `token`"

    payload, err = verify_token(token)
    try:
        username = payload["username"]
        email = payload["email"]
    except KeyError:
        username = None
        email = None
        err = "This wasn't a student token"

    output = (username, email, err)
    assert (
        isinstance(output, tuple)
        and len(output) == 3
        and ((output[0] is None) == (output[1] is None))
        and ((output[0] is None) != (output[2] is None))
        and (output[0] is None or isinstance(output[0], basestring))
        and (output[1] is None or isinstance(output[1], basestring))
        and (output[2] is None or isinstance(output[2], basestring))
    ), "Postcondition failed"
    return output


def authenticate_student(token):
    assert isinstance(token, basestring), "Precondition failed for `token`"

    resp = None

    username, email, err = verify_student_token(token)

    if err is not None:
        resp = TemplateResponse(
            req,
            "400.html",
            context={
                "message": _(
                    "This page isn't valid. You can try asking for a new "
                    "login link."
                )
            },
        )
        output = HttpResponseBadRequest(resp.render())

    else:

        username_, password = get_student_username_and_password(email)

        if username == username_:
            user = authenticate(username=username, password=password)
        else:
            passwords = get_lti_passwords(username)
            users_ = [
                authenticate(username=username, password=p) for p in passwords
            ]
            user = [u for u in users_ if u is not None][0]

        if user is None:
            resp = TemplateResponse(
                req,
                "401.html",
                context={
                    "message": _("The account hasn't been verified yet.")
                },
            )
            output = HttpResponseUnauthorized(resp.render())
        else:
            output = user

    assert isinstance(output, HttpResponse) or isinstance(
        output, User
    ), "Postcondition failed"
    return output


def get_student_username_and_password(email, max_username_length=30):
    assert isinstance(email, basestring), "Precondition failed for `email`"

    key = settings.SECRET_KEY

    username = hashlib.md5(email.encode()).hexdigest()[:max_username_length]
    password = hashlib.md5(
        ("{}:{}".format(username, key)).encode()
    ).hexdigest()

    output = (username, password)

    assert (
        isinstance(output, tuple)
        and len(output) == 2
        and isinstance(output[0], basestring)
        and isinstance(output[1], basestring)
    ), "Postcondition failed"
    return output


def get_lti_passwords(hashed_username):
    assert isinstance(
        hashed_username, basestring
    ), "Precondition failed for `hashed_username`"

    key = settings.PASSWORD_GENERATOR_NONCE

    if hashed_username.endsWith("++"):
        usernames = [
            base64.urlsafe_b64decode(hashed_username[:-2] + i + j).encode()
            for i in ("+", "=")
            for j in ("+", "=")
        ]
    elif hashed_username.endsWith("+"):
        usernames = [
            base64.urlsafe_b64decode(hashed_username[:-1] + i).encode()
            for i in ("+", "=")
        ]
    else:
        usernames = [base64.urlsafe_b64decode(hashed_username).encode()]

    passwords = [hashlib.md5(u + key).digest() for u in usernames]

    output = passwords
    assert isinstance(output, list) and all(
        isinstance(o, basestring) for o in output
    ), "Postcondition failed"
    return output