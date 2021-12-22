from typing import List


def dot(*args: str):
	return '.'.join(args)


def get_event_domain(event_name: str):
	return event_name.split(".")[0]
