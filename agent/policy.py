DENY = set()

ASK = {"write_file"}


def policy_check(name, args):
    if name in DENY:
        return "deny"
    if name in ASK:
        return "ask"
    return "allow"
