from subprocess import call


def ping(address):
    return call(['ping', '-c', '1', address]) == 0

def scan(ip_range, verbose=False):
    network = IPv4Network(ip_range)
    ips = []
    for host in network:
        if ping(host.ip_address):
            ips.append(host.ip_address)
            if verbose:
                print("{}: AVAILABLE".format(host.ip_address))
        else:
            if verbose:
                print("{}: UNAVAILABLE".format(host.ip_address))
    return ips

