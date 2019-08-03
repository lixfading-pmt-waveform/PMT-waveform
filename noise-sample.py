import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import random
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
#读取文件数据
with open(sys.argv[1]) as ipt:
	csv_noise = np.loadtxt(ipt)
print(csv_noise)
#读入信号数据
ipt = h5py.File(sys.argv[2])
h=ipt['PEInfo'][...]
num1=[]
num2=[]
num3=[]
num4=[]
for i in h:
	num1.append(i[0])
	num2.append(i[1])
	num3.append(i[2])
	num4.append(i[3])
#print(num1)
#print(num2)
#print(num3)
#print(num4)
num5=[]
num6=[]
num7=[0]*len(num1)
num5.append(num1[0])
num6.append(num2[0])
#进度条
for i in range(int(max_steps/4)):
	process_bar.show_process()
	time.sleep(0.05)
#将同一channel下的信号合并
j=0
while True:
	j=j+1
	if j==len(h):
		break
	if num1[j]==num1[j-1]:
		if num2[j]==num2[j-1]:
			j=j
		else:
			num5.append(num1[j])
			num6.append(num2[j])
	else:
		num5.append(num1[j])
		num6.append(num2[j])
		continue
num7=[0]*len(num1)
#进度条
for i in range(int(max_steps/4)):
	process_bar.show_process()
	time.sleep(0.05)
#进度条
#产生高斯白噪音，其均值为0，方差为1
for j in range(len(num1)):
	mu, sigma = 0, csv_noise
	s = np.random.normal(mu, sigma, 1029)
	num7[j]=s
print(num7)
#进度条
for i in range(int(max_steps/2)):
	process_bar.show_process()
	time.sleep(0.05)
#进度条
#写入文件
g=h5py.File(sys.argv[3],'w')
dt = np.dtype([(' EventID',np.int64), (' ChannelID', np.int16),(' Waveform', np.float, (1029,))])
i=0
x = np.array((num5[0],num6[0],num7[0]), dtype=dt)
while True:	
	i=i+1
	if i==len(num5):
		break
	else:
		y = np.array((num5[i],num6[i],num7[i]), dtype=dt)
	x = np.hstack((x,y))	
g['Noise']=x
#进度条截止
process_bar.close()
