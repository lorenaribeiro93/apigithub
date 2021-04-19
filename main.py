from flask import Flask, jsonify
from github import Github
import os

from file import *


app = Flask(__name__)

GITHUB_TOKEN = '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'
GTHUB = Github(GITHUB_TOKEN)

orgs = 'orgs.json'
if not file_exists(orgs):
    create_file(orgs)

login = ''


def request(r):
    organization = r.get_organization(login)
    name = organization.name
    public_repos = organization.public_repos
    followers = organization.get_public_members().totalCount
    score = followers + public_repos

    org = {'login': login, 'name': name, 'score': score}

    store_org(orgs, org)

    for org in read_file(orgs):
        if org['login'] == login:
            return org


def delete(r):
    file = read_file(orgs)
    delete_org(orgs, file[login])
    return file


@app.route('/', methods=['GET'])
def get_orgs():
    return jsonify(read_file(orgs))


@app.route('/<string:arg>', methods=['GET'])
def get_org(arg):
    global login
    login = arg
    return jsonify(request(GTHUB))


@app.route('/<string:arg>', methods=['DELETE'])
def delete_org(arg):
    global login
    login = arg
    return jsonify(delete(GTHUB))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
