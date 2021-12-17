def dot(*args):
	return '.'.join(args)


def get_event_domain(event_name):
	return event_name.split(".")[0]
