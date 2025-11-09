import tkinter as tk
import os
import ffmpeg
import sys
import torch
from tkinter import filedialog
import warnings

# filter warnings
warnings.filterwarnings(
    "ignore",
    message="Torch was not compiled with flash attention",
    category=UserWarning,
)
import whisper

warnings.filterwarnings("ignore", message="A matching Triton")
warnings.filterwarnings("ignore", message="1Torch was not compiled with flash attention.")
warnings.filterwarnings("ignore", message="Torch was not compiled with flash attention")
warnings.filterwarnings("ignore", message="A matching Triton")
warnings.filterwarnings("ignore", message="Some optimizations will not be enabled")
warnings.filterwarnings("ignore", message="No module named 'triton'")
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
try:
    import xformers
    import xformers.ops as xops
except Exception:
    pass
sys.stderr.close()
sys.stderr = stderr

# tkinter class
class Root():
	def __init__(self, window):
		self.window = window
		self.set_window()
		self.create()

	def set_window(self):
		self.window.title('VideoToText')
		width = 930
		height = 700
		screenwidth = self.window.winfo_screenwidth()
		screenheight = self.window.winfo_screenheight()
		size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
		self.window.geometry(size_geo)
	def create_button(self,tab,function,display,w=10):
		b = tk.Button(tab,text=display,command=function,font=('Consolas','12'),width=w)
		return b

	def create_text(self,tab,w,h):
		t = tk.Text(tab, undo=True, width=w,height=h,font=('Consolas','12'))
		return t

	def create_label(self,tab,display,w=10,h=1):
		l = tk.Label(tab,text=display,width=w,height=h,font=('Consolas','12'))
		return l
	
	def create_entry(self,tab,w=15):
		e = tk.Entry(tab,show=None,width=w,font=('Consolas','12'))
		return e

	def getpath(self):
		path = filedialog.askopenfilename(
				title = "Choise a file",
				initialdir = r"D:\will\\",
				filetypes = (
					("All Files", "*.*"),
					("Text File", "*.txt")
				)
			)
		return path
	# result display
	def display_results(self,tab,result):
		l_result = tk.Label(tab, text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

	def create(self):
		def clean():
			self.display_results(self.window, '')
		def getpath_video():
			clean()
			path = self.getpath()
			e_video.delete(0, tk.END)
			e_video.insert(0, path)
		def getpath_text():
			clean()
			path = self.getpath()
			e_text.delete(0, tk.END)
			e_text.insert(0, path)
		def extractaudio(videopath, audiopath):
			try:
				# extract audio
				(
					ffmpeg
					.input(videopath)
					.output(audiopath, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
					.overwrite_output()
					.run(quiet=True)
				)
			except Exception as e:
				self.display_results(self.window, 'ffmpeg error: ' + str(e.stderr.decode('utf-8')))

		def whisper_GPU(audiopath):
			try:
				# load whisper
				model = whisper.load_model('medium', device='cuda')
				if hasattr(model, 'enable_xformers_memory_efficient_attention'):
					model.enable_xformers_memory_efficient_attention()
					sys.stdout.write("xFormers memory-efficient attention enabled.\n")
				# transcribe
				result = model.transcribe(audiopath, verbose=True, language="zh", fp16=True)
				return result
			except Exception as e:
				self.display_results(self.window, 'whisper error: ' + str(e))

		def out_file(videopath, textpath, result):
			try:
				# format the result data
				videofilename = os.path.split(videopath)[1]
				v_name = os.path.splitext(videofilename)[0]
				outfile = str(textpath) + str(v_name) + '.txt'
				with open(outfile, 'w+') as f:
					f.write(result)
				t_output.insert("insert", str(result))
			except Exception as e:
				self.display_results(self.window, str(e))

		def transcribe():
			try:
				sys.stdout.write('[ START Transcribe ]\n')
				torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=True)
				sys.stdout.write("Using xFormers memory-efficient attention instead of torch flash attention.\n")
				videopath = e_video.get()
				# textpath = e_text.get()
				audiopath = "tmp_audio.wav"
				if videopath:
				# if videopath and  textpath:
					if torch.cuda.is_available():
						if torch.backends.cudnn.is_available():
							sys.stdout.write(f'CUDA and cuDNN is availlable, CUDA version: {torch.version.cuda}, torch version: {torch.__version__}\n\n')
							# extract audio
							extractaudio(videopath, audiopath)
							# transcribe audio
							result = whisper_GPU(audiopath)
							# output result
							# out_file(videopath, textpath, str(result))
							# delete temporary audio file
							os.remove('./tmp_audio.wav')
							sys.stdout.write('[ Transcription complete ]\n\n')
						else:
							sys.stdout.write('cuDNN is not available\n\n')
					else:
						sys.stdout.write('CUDA is not available, please check, please check the configuration.\n\n')
				else:
					self.display_results(self.window, 'Path is empty!')
			except Exception as e:
				self.display_results(self.window, str(e))

		l_description = self.create_label(self.window, 'Vidoe To Text', w=65, h=1)
		l_description.grid(row=0, column=0, columnspan=6)
		l_video = self.create_label(self.window, 'Video', w=10, h=1)
		l_video.grid(row=1, column=0)
		e_video = self.create_entry(self.window, w=70)
		e_video.grid(row=1, column=1)
		b_video = self.create_button(self.window, getpath_video, 'File')
		b_video.grid(row=1, column=2)
		# l_text = self.create_label(self.window, 'Text', w=10, h=1)
		# l_text.grid(row=2, column=0)
		# e_text = self.create_entry(self.window, w=70)
		# e_text.grid(row=2, column=1)
		# e_text.insert(0, "C:/Users/DC/Desktop/")
		# b_text = self.create_button(self.window, getpath_text, 'File')
		# b_text.grid(row=2, column=2)
		# t_output = self.create_text(self.window, w=90, h=25)
		# t_output.grid(row=3, column=0, columnspan=6)
		b_transcribe = self.create_button(self.window, transcribe, 'Transcribe')
		b_transcribe.grid(row=4, column=0, columnspan=6)
if __name__ == '__main__':
	window = tk.Tk()
	Root(window)
	window.mainloop()