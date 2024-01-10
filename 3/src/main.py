from general import General


def init_generals(generals_spec):
    generals = []
    for i, spec in enumerate(generals_spec):
        general = General(i)
        if spec == "l":
            pass
        elif spec == "t":
            general.is_traitor = True
        else:
            print("Error, bad input in generals list: {}".format(generals_spec))
            exit(1)
        generals.append(general)
    for general in generals:
        general.other_generals = generals
    return generals


def print_decisions(generals):
    for i, l in enumerate(generals):
        print("General {}: {}".format(i, l.decision))


def main():
    m = 4
    generals = "l,l,t,l,l,t,l,l,t,t"
    order = "ATTACK"

    generals_spec = [x.strip() for x in generals.split(',')]
    generals = init_generals(generals_spec=generals_spec)
    generals[0](m=m, order=order)
    print_decisions(generals)


if __name__ == "__main__":
    main()
