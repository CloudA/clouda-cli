import click

from clouda_cli import opencrack
from clouda_cli.models import auth

REGIONS = ['ca-ns-1', 'ca-bc-1']


@click.group()
def cli():
    pass


@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True,
              hide_input=True, confirmation_prompt=True)
@click.option('--region', prompt=True, type=click.Choice(REGIONS))
def login(username, password, region):
    click.secho("Passwords Match.", fg='green')

    click.echo("Hi, %s. Logging you in to %s..." % (username, region))

    pw_auth = auth.Auth(
        'password',
        {
            "user": {
                "domain": {"id": "default"},
                "name": username,
                "password": password
            }
        })

    login_url = 'https://keystone.%s.clouda.ca:8443/v3/auth/tokens' % region

    login_response = opencrack.api_request(
        login_url, None, pw_auth.as_dict())
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
                login_url, None, challenge_request.as_dict())
            if challenge_response.status_code != 201:
                click.secho("Auth Code Invalid, retry.", fg='red')
                continue

            challenge_response.json()
            real_token_id = challenge_response.headers['X-Subject-Token']
            token_valid = True
            click.secho("Token: %s" % real_token_id, fg='green')

    else:
        click.secho("Token: %s" % token_id, fg='green')
