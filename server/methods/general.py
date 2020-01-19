from server import utils
from server import cache
import requests
import config

class General():
	@classmethod
	def info(cls):
		data = utils.make_request('getblockchaininfo')

		if data['error'] is None:
			data['result']['reward'] = utils.reward(data['result']['blocks'])
			data['result']['debug'] = config.debug
			data['result'].pop('verificationprogress')
			data['result'].pop('initialblockdownload')
			data['result'].pop('pruned')
			data['result'].pop('softforks')
			data['result'].pop('bip9_softforks')
			data['result'].pop('warnings')
			data['result'].pop('size_on_disk')

			nethash = utils.make_request('getnetworkhashps', [120, data['result']['blocks']])
			if nethash['error'] is None:
				data['result']['nethash'] = int(nethash['result'])

		return data

	@classmethod
	@cache.memoize(timeout=config.cache)
	def supply(cls):
		data = utils.make_request('getblockchaininfo')
		height = data['result']['blocks']

		calc_height = height

		reward = utils.satoshis(50)
		halvings = 840000
		halvings_count = 0
		supply = reward

		while calc_height > halvings:
			total = halvings * reward
			reward = reward / 2
			calc_height = calc_height - halvings
			halvings_count += 1

			supply += total

		supply = supply + calc_height * reward

		return {
			'halvings': int(halvings_count),
			'supply': int(supply),
			'height': height
		}

	@classmethod
	def fee(cls):
		#data = utils.make_request('estimatesmartfee', [6])

		#if data['error'] is None:
		#	data['result']['feerate'] = utils.satoshis(data['result']['feerate'])

		#return data

		return utils.response({
			'feerate': utils.satoshis(0.001),
			'blocks': 6
		})

	@classmethod
	def mempool(cls):
		data = utils.make_request('getmempoolinfo')

		if data['error'] is None:
			if data['result']['size'] > 0:
				mempool = utils.make_request('getrawmempool')['result']
				data['result']['tx'] = mempool
			else:
				data['result']['tx'] = []

		return data

	@classmethod
	def price(cls):
		link = 'https://api.coingecko.com/api/v3/simple/price?ids=beyondcoin&vs_currencies=usd,btc'
		return requests.get(link).json()
