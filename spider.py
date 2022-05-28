from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *




class MainAddon:
	def __init__(self):
		self.can_spider = False
		self.target_host = 'edith.xiaohongshu.com'
		self.test_path = 'httpbin.org/json'
		self.path_method_map = {
			'/note/user/posted': self.handle_notes,
			'/user/me?': self.handle_user,
			'/user/info?': self.handle_user,
		}
		self.note_db = {}
		self.init_data()


	def init_data(self):
		tiny_db = TinyDB(user_file, encoding="utf8", ensure_ascii=False)
		self.user_table = tiny_db.table('user')

		self.note_ids = defaultdict(set)
		for note_list in get_file_data():
			for note in note_list:
				note_id = note['id']
				user_id = note['user']['userid']
				self.note_ids[user_id].add(note_id)


	@except_decorative
	def handle_notes(self, data):
		if not data.get('success'):
			return
		user_id = notes[0]['user']['userid']
		notes = data.get('data').get('notes', [])
		filter_notes = [n for n in notes if n['id'] not in self.note_ids[user_id]]
		if not filter_notes:
			return
		ids = [n['id'] for n in filter_notes]
		note_table = self.note_db[user_id]
		note_table.insert_multiple(filter_notes)
		self.note_ids[user_id].update(ids)


	@except_decorative
	def handle_user(self, data):
		user_info = data.get('data')
		user_id = user_info['userid']
		nick_name = user_info['nickname']
		note_file = f'{file_path}/note-{user_id}.json'
		tiny_db = TinyDB(note_file, encoding="utf8", ensure_ascii=False)
		self.note_db[user_id] = tiny_db.table('note')
		self.user_table.upsert(user_info, Query().userid == user_id)
		log_info_list(['开始抓取', user_id, nick_name])


	@except_decorative
	def response(self, flow):
		print(req.url)
		req = flow.request
		if self.test_path in req.url:
			log_info('成功连接代理...')
			self.can_spider = True
			return
		if not self.can_spider:
			return
		if self.target_host not in [req.host, req.host_header]:
			return
		method = None
		for path, _method in self.path_method_map.items():
			if path in req.url:
				method = _method
		if not method:
			return
		res = flow.response
		method(json.loads(res.text))


def init_app():
	create_folder(file_path)


if __name__ == '__main__':
	init_app()
	ip, port = get_user_ip_port('192.168.1.4')
	opts = Options(listen_host=ip, listen_port=port)
	opts.add_option("body_size_limit", int, 0, "")

	m = DumpMaster(opts, with_termlog=False, with_dumper=False)
	config = ProxyConfig(opts)
	m.server = ProxyServer(config)
	m.addons.add(MainAddon())

	try:
		log_info('proxy :', (ip, port))
		log_info('请用手机浏览器打开: https://httpbin.org/json')
		m.run()
	except KeyboardInterrupt:
		m.shutdown()