from anakonda.config import Config

STATUS_MESSAGES = {
    100: "ok",
    101: "Method is not implemented",
}


def jsonify(state={}, metadata={}, status=200, code=100, headers={}):
    resource = {}
    resource["result"] = state
    resource["metadata"] = metadata
    resource["status"] = {
        "code": code,
        "message": STATUS_MESSAGES if Config.DEBUG else None,
    }
    return resource, status, headers
