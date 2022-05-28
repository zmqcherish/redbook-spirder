from tkinter import ttk, Tk, Label, Toplevel, Entry, Button, Checkbutton, Menu, messagebox, Scrollbar, IntVar, StringVar, HORIZONTAL, END
from util import *

app_version = 'v1'

class App(object):
	def __init__(self):
		self.item_num = 0
		self.columns = ['itemNum', 'userId', 'displayId', 'nickName', 'genderDisplay', 'followingCount', 'followerCount', 'qrCode', 'msgCount', 'content', 'secUid']
		self.user_map = dict()

		self.init_data()
		self.init_window()
		# self.init_loading()
		# self.root.after(1000, self.show_tip)


	def init_window(self):
		self.root = Tk() # 窗口
		self.root.title(f'小红书助手 - {app_version}')  # 标题
		g = self.get_geometry(1000, 700)
		self.root.geometry(g)

		self.btn_ok = Button(self.root, text='刷新', command=self.init_data)

		# 列表值: 表头名，列宽度
		columns_config = {
			'itemNum': ['序号', 50],
			'userId': ['标题', 500],
		}
		self.table = ttk.Treeview(
				master = self.root,  # 父容器
				# height=30,  # 表格显示的行数,height行
				columns=self.columns,  # 显示的列
				# show='headings',  # 隐藏首列
				)
		# 定义表头
		for k,v in columns_config.items():
			self.table.heading(k, text=v[0])

		# 定义列
		for k,v in columns_config.items():
			self.table.column(k, width=v[1], minwidth=v[1], anchor='s')

		item_num = 1
		row_index = 0
		for note in self.note_data:
			self.table.insert('', END, text='', iid=row_index, values=(item_num, note['title']), open=True)
			self.table.insert('', END, text=note['desc'], iid=row_index + 1, open=False)
			self.table.move(row_index + 1, row_index, 0)
			self.table.insert('', END, text=note['likes'], iid=row_index + 2, open=False)
			self.table.move(row_index + 2, row_index, 1)
			row_index += 3
			item_num += 1
			


		# adding children of first node
		


		self.btn_ok.grid(row=0, column=0, sticky='nsew')
		self.table.grid(row=1, column=0, columnspan=4)


	def init_data(self):
		self.user_data = defaultdict(list)

		self.note_data = get_json_file('dev/red_notes.json')

		self.note_data.sort(key=lambda x:x['id'], reverse=False)


		# for note_list in get_file_data():
		# 	for note in note_list:
		# 		user_id = note['user']['userid']
		# 		self.user_data[user_id].append(note)


	def get_geometry(self, width, height):
		screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
		screenheight = self.root.winfo_screenheight()  # 屏幕高度
		x = int((screenwidth - width) / 2)
		y = int((screenheight - height) / 2)
		return f'{width}x{height}+{x}+{y}'


	def mainloop(self):
		"""Start the GUI loop"""
		self.root.mainloop()


if __name__ == "__main__":
	print('正在初始化...')
	# init_app()
	app = App()
	print('初始化完成...')
	app.mainloop()