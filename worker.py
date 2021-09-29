from threading import Thread


def do_in_background(target, args):
    thread = Thread(target=target, args=args)
    thread.start()
