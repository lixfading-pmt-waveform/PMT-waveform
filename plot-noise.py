import h5py
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
#定义进度条
class ShowProcess():
	i = 0 # 当前的处理进度
	max_steps = 1 # 总共需要处理的次数
	max_arrow = 50 #进度条的长度

	# 初始化函数，需要知道总共的处理次数
	def __init__(self, max_steps):
		self.max_steps = max_steps
		self.i = 0

	# 显示函数，根据当前的处理进度i显示进度
	# 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
	def show_process(self, i=None):
		if i is not None:
			self.i = i
		else:
			self.i += 1
		num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
		num_line = self.max_arrow - num_arrow #计算显示多少个'-'
		percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
		process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
					 + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
		sys.stdout.write(process_bar) #这两句打印字符到终端
		sys.stdout.flush()

	def close(self, words='done'):
		print('')
		print (words)
		self.i = 0
max_steps = 100
process_bar = ShowProcess(max_steps)	
#读取画图数据
ipt = h5py.File(sys.argv[3])
h=ipt['Noise'][...]
num1=[]
num2=[]
num3=[]
num4=[]
for i in h:
	num1.append(i[0])
	num2.append(i[1])
	num3.append(i[2])
#print(num1)
#print(num2)
#print(num3)
#进度条
for i in range(int(max_steps*3/4)):
	process_bar.show_process()
	time.sleep(0.05)
#进度条
#读取画图数据
for i in range(len(num1)):
	if num1[i]==int(sys.argv[2]):
		if num2[i]==int(sys.argv[1]):
			num4=num3[i]
#进度条	
for i in range(int(max_steps*1/4)):
	process_bar.show_process()
	time.sleep(0.05)
#进度条
#画图
plt.plot(num4) 
plt.title('Noise') 
plt.xlabel('ns'); plt.ylabel('mV')
plt.savefig(sys.argv[4])
plt.show()
#进度条截止
process_bar.close()