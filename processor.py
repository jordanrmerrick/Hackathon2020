import usaddress


def address_checker(address):
    tagged = usaddress.tag(address)
    if tagged[-1] == "Ambiguous":
        return "Please enter a valid address!", 1
    else:
        return address, 0


def state(address):
    tagged = usaddress.tag(address)
    dtagged = dict(tagged[0])
    return dtagged["StateName"].lower()
