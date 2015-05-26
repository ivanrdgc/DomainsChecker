#!/usr/bin/python3

import common, tkinter, sys, os, os.path, tempfile, subprocess

class MainAppProxy:
	def __init__(self, executableName):
		self.process = None
		self.filename = None
		self.writer = None
		self.reader = None
		self.domain = None
		self.executableName = executableName

	def start(self, domain):
		if (self.process != None):
			return

		self.domain = domain
		self.filename = common.get_full_path(self.executableName + '.log')

		self.writer = open(self.filename, 'wb')
		self.reader = open(self.filename, 'rb', 1)

		if (hasattr(sys, 'frozen')):
			self.process = subprocess.Popen([os.path.join(os.path.dirname(os.path.realpath(sys.executable)), self.executableName), self.domain], stdout=self.writer, stderr=self.writer)
		else:
			self.process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.realpath(__file__)), self.executableName), self.domain], stdout=self.writer, stderr=self.writer)

	def get_output(self):
		ret = ''

		if (self.process != None):
			if (self.process.poll() == None):
				ret = self.reader.read().decode('utf-8')
			else:
				ret = self.reader.read().decode('utf-8')
				self.stop()
		
		try:
			return(ret.strip().splitlines()[-1])

		except IndexError:
			return(ret.strip())

	def stop(self):
		if (self.process != None):
			if (self.process.poll() == None):
				self.process.kill()
			self.process.wait()
			self.process = None
		
		if (self.writer != None):
			self.writer.close()
			self.writer = None
		
		if (self.reader != None):
			self.reader.close()
			self.reader = None

		if (self.filename != None):
			self.filename = None

	def __del__(self):
		self.stop()

class GUIApplication(tkinter.Frame):
	def __init__(self, master=None):
		if (master == None):
			master = tkinter.Tk()
		
		tkinter.Frame.__init__(self, master)
		master.title('Check domains Availability')

		self.master = master
		self.pack()
		self.create_widgets()

		self.appProxy = MainAppProxy('app.exe' if hasattr(sys, 'frozen') else 'app.py')

	def create_widgets(self):
		self.textlabeltxt = tkinter.StringVar()
		self.textlabel = tkinter.Label(self, textvariable=self.textlabeltxt)
		self.textlabel.pack(side='top')
		self.textlabeltxt.set('Domain to check:')

		self.textbox = tkinter.Entry(self)
		self.textbox.pack(side='top')
		self.textbox.focus_set()

		self.checkbtn = tkinter.Button(self, text='Check domain', command=self.check_domains)
		self.checkbtn.pack(side='left')

		self.QUIT = tkinter.Button(self, text='QUIT', fg='red', command=self.master.destroy)
		self.QUIT.pack(side='right')

		self.browser = tkinter.Button(self, text='Browser', command=self.browser)
		self.browser.pack(side='bottom')

	def check_domains(self):
		domain_text = self.textbox.get().strip()

		if (len(domain_text) > 0):
			self.textlabeltxt.set('Started!')
			self.appProxy.start(domain_text)
			self.checkbtn.config(state='disabled')
			self.repaint_label()

	def repaint_label(self):
		last_text = self.appProxy.get_output()
		
		if (len(last_text) > 0):
			self.textlabeltxt.set(last_text)
		
		if (self.appProxy.process != None):
			self.after(500, self.repaint_label)
		else:
			self.textlabeltxt.set('Completed!')
			self.checkbtn.config(state='normal')

	def browser(self):
		import sys, subprocess, os.path, os

		if sys.platform == 'darwin':
			def openFolder(path):
				subprocess.call(['open', path])
		elif sys.platform.startswith('linux'):
			def openFolder(path):
				subprocess.call(['gnome-open', path])
		elif sys.platform == 'win32':
			def openFolder(path):
				subprocess.call(['explorer', path])

		app_config = common.read_config()

		output_path = common.get_full_path(app_config['OutputPath'])
		os.makedirs(output_path, 0o755, True)
		openFolder(output_path)

if (__name__ == '__main__'):
	app = GUIApplication()
	app.mainloop()
