import click

from clouda_cli import opencrack
from clouda_cli.models import auth

LOGIN_URL = 'http://localhost:5000/v3/auth/tokens'


@click.group()
def cli():
    pass


@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True,
              hide_input=True, confirmation_prompt=True)
def login(username, password):
    click.secho("Passwords Match.", fg='green')

    click.echo("Hi, %s. Logging you in..." % username)

    pw_auth = auth.Auth(
        'password',
        {
            "user": {
                "domain": {"id": "default"},
                "name": username,
                "password": password
            }
        })

    login_response = opencrack.api_request(
        LOGIN_URL, None, pw_auth.as_dict())
    token = login_response.json()['token']

    # login token grab
    token_id = login_response.headers['X-Subject-Token']
    token_valid = False
    if 'OS-OTP' in token:
        # challenge the user for an OTP auth code
        while not token_valid:
            auth_code = click.prompt("Enter TOTP Code", type=str)
            challenge_request = auth.Auth(
                'totp', {"auth_code": auth_code, "token_exchange": token_id})

            challenge_response = opencrack.api_request(
                LOGIN_URL, None, challenge_request.as_dict())
            if challenge_response.status_code != 201:
                click.secho("Auth Code Invalid, retry.", fg='red')
                continue

            real_token = challenge_response.json()
            real_token_id = challenge_response.headers['X-Subject-Token']
            token_valid = True
            click.secho("yer token: %s" % real_token_id, fg='green')

    else:
        click.echo("real token, no OTP: %s" % token_id)
