from ipaddress import IPv4Network
from subprocess import call


def ping(address):
    return call(['ping', '-c', '1', address]) == 0

def scan(addresses, verbose=False):
    ips = []
    for host in addresses:
        if ping(host):
            ips.append(host)
            if verbose:
                print("{}: AVAILABLE".format(host))
        else:
            if verbose:
                print("{}: UNAVAILABLE".format(host))
    return ips

