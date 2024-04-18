import sys
import edge_db

def _check_int(arg):
    try:
        return int(arg)
    except ValueError:
        print("Must be int")
        exit(1)

def get_db():
    con = edge_db.EdgeDatabase('localhost', 5432)
    return con

def help():
    print("Edge CLI (Command Line Interface) Usage Guide")
    print("\tedge_cli logs [amount]  | list logs (amount default 10)")
    print("\tedge_cli allowed        | list allowed uids")
    print("\tedge_cli allow <uid>    | allow a uid")
    print("\tedge_cli deny <uid>     | remove a uid")

def listAllowed():
    allowed = get_db().getAllowed()
    print("UID")
    for x in allowed:
        uid, = x
        print(uid)

def allow(uid):
    get_db().addAllowed(uid)
    print("Successfully allowed {}".format(uid))

def deny(uid):
    get_db().removeAllowed(uid)
    print("Successfully denied {}".format(uid))

def listLogs(amount=10):
    logs = get_db().getLogs(amount)

    print("UID\t\t\t\tTime")
    for x in logs:
        uid, time = x
        print("{}\t\t{}".format(uid, time))

# we can chain if statements because we exit after each execution don't need elif
def main(argv):
    if len(argv) == 1:
        help()
        exit(0)

    if len(argv) == 2:
        if argv[1] == 'allowed':
            listAllowed()
            exit(0)
        if argv[1] == 'logs':
            listLogs()
            exit(0)

    if len(argv) == 3:
        if argv[1] == 'logs':
            listLogs(_check_int(argv[2]))
        if argv[1] == 'allow':
            allow(argv[2])
            exit(0)
        if argv[1] == 'deny':
            deny(argv[2])
            exit(0)

    help()
    exit(0)

if __name__ == '__main__':
    main(sys.argv)
