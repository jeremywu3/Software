import kmeans
import numpy as np

from . import logger

class AntiInstagram():

	def __init__(self):
		self.num_colors = 3
		self.ideal_colors = [[0, 0, 0], [0, 255, 255], [255, 255, 255]]
		self.transformation = [0,0,0]
		self.scale = [1.0,1.0,1.0]
		self.shift = [0.0,0.0,0.0]
		self.health = 0

	def applyTransform(self,image):
		# IPython.embed()
		corrected_image = kmeans.scaleandshift(image,self.scale,self.shift)
		return corrected_image

	def calculateTransform(self,image,testframe=False):
		trained,counter = kmeans.runKMeans(image)
		mapping = kmeans.identifyColors(trained, kmeans.CENTERS)
		# IPython.embed()
		r,g,b,cost = kmeans.getparameters2(mapping, trained, counter, kmeans.CENTERS)

		if r[0][0] == 0.0: return

		# Estimates the scale and shift over multiple frame via an IIR filter with preference towards low-cost frames
		IIR_weight=1000/(10000+cost)
		logger.info("cost = %f, IIR_weight = %f" % (cost, IIR_weight))
		# self.scale = [r[0][0][0],g[0][0][0],b[0][0][0]]
		# self.shift = [r[1][0], g[1][0],b[1][0]]
		deltascale = np.array([r[0][0][0],g[0][0][0],b[0][0][0]])
		deltashift = np.array([r[1][0], g[1][0],b[1][0]])
		if testframe:
			self.scale = deltascale
			self.shift = deltashift
		else:
			self.scale = (self.scale+deltascale*IIR_weight)/(1+IIR_weight)
			self.shift = (self.shift+deltashift*IIR_weight)/(1+IIR_weight)
		self.health=1/(cost+np.finfo('double').eps)
		return 1

	def calculateHealth(self):
		'''
		   one way is to keep one img every 1 sec and compare the diff 
			http://stackoverflow.com/questions/189943/how-can-i-quantify-difference-between-two-images
		'''

	
		return self.health
		

	def calibrateLighting(self, cal_img):
		# XXX these are unused
		sample = self.getSample(cal_img)

		equalParam = self.histEqual(sample)

		kMeansParam = self.kMeansParam(sample)

		return self.calibration_parameters

# 	def getSample(self, img):
# 		'''code to sample from entire img a part that contains lanes and floor'''
#
# 		return sample
#
# 	def histEqual(self, img):
# 		'''https://en.wikipedia.org/wiki/Normalization_(image_processing)'''
#
# 		return equalParam
#
# 	def kMeans(self, img):
#
# 		return kMeansParam