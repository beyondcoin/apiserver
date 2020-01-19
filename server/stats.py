from datetime import timedelta
import server as state

def socket(func):
	def wrapper(*args, **kwargs):
		state.socket_counter += 1
		return func(*args, **kwargs)

	return wrapper

def rest(func):
	def wrapper(*args, **kwargs):
		state.rest_counter += 1
		return func(*args, **kwargs)

	return wrapper

def info():
	uptime = timedelta(seconds=time.monotonic() - state.start_time)
	return {
		'uptime': str(uptime),
		'subscriptions': {
			'connections': state.connections,
			'subscribers': len(state.subscribers),
			'rooms': len(state.rooms)
		},
		'requests': {
			'socket': state.socket_counter,
			'rest': state.rest_counter
		}
	}
