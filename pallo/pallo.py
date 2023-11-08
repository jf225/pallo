from itertools import combinations
import random
from itertools import product
from tqdm import tqdm

class gphrModel:

	dataset = []
	assetCount = None
	numshares = 1
	binCount = None
	rangeSets = []
	binSets = []
	totalSets = []
	positions = []
	meanSets = []
	uniqPos = []
	probs = []
	totalev = 0
	hprs = []
	bases = []
	GHPRs = []
	maxGHPR = 0.0
	bestValues = []
	underDrawValues = []
	underDrawGHPR = 0
	probOfDraw = 0


	def __init__(self, dataset):
		self.dataset = dataset
		self.assetCount = len(self.dataset)
		for i in range(0, self.assetCount):
			self.bases.append(.01)

	def defineBins(self, numBins=5):
		if numBins < 3:
			print("Minimum bin count is 3.")
			return
		else:
			self.binCount = numBins

		for i in range(0, self.assetCount):

			changes = self.dataset[i]

			low = changes[0] * self.numshares
			high = changes[0] * self.numshares

			rCount = self.binCount-2

			for prices in changes:
				prices = prices * self.numshares
				if prices < low:
					low = prices
				if prices > high:
					high = prices	

			rang = high - low
			split = rang / rCount

			ranges = [str(low)]
			i = 0
			while i < rCount:
				thing = str(low) + "|"
				low = low + split
				thing = thing + str(low)
				ranges.append(thing)
				i = i + 1

			ranges.append(low)

			bins = []
			totals = []
			for i in range(0, numBins):
				bins.append(0)
				totals.append(0)

			self.rangeSets.append(ranges)
			self.binSets.append(bins)
			self.totalSets.append(totals)
		self.storeOutcomes()


	def storeOutcomes(self):
		for m in range(0, len(self.dataset[0])):
			poses = ""
			for asset in range(0, self.assetCount):
				outcome = self.dataset[asset][m]
				outcome = outcome * self.numshares
				j = 0
				found = 0
				while j < self.binCount:
					if j == 0:
						if outcome == float(self.rangeSets[asset][0]):
							self.binSets[asset][0] = self.binSets[asset][0] + 1
							self.totalSets[asset][0] += outcome
							if asset == 0:
								poses += str(j)
							else:
								poses += "-" + str(j)
							found = 1
							j = self.binCount
					elif j == self.binCount - 1:
						if outcome == float(self.rangeSets[asset][self.binCount - 1]):
							self.binSets[asset][self.binCount-1] = self.binSets[asset][self.binCount-1] + 1
							self.totalSets[asset][self.binCount-1] += outcome
							if asset == 0:
								poses += str(j)
							else:
								poses += "-" + str(j)
							found = 1
							j = self.binCount
					else:
						lower = float(self.rangeSets[asset][j].split("|")[0])
						higher = float(self.rangeSets[asset][j].split("|")[1])
						if outcome > lower and outcome < higher:
							self.binSets[asset][j] = self.binSets[asset][j] + 1
							self.totalSets[asset][j] += outcome
							if asset == 0:
								poses += str(j)
							else:
								poses += "-" + str(j)
							found = 1
							j = self.binCount

					j = j + 1
				if found == 0:
					j = 0
					while j < self.binCount:
						outcome = round(outcome, 5)
						if j == 0:
							if outcome == float(self.rangeSets[asset][0]):
								self.binSets[asset][0] = self.binSets[asset][0] + 1
								self.totalSets[asset][0] += outcome
								if asset == 0:
									poses += str(j)
								else:
									poses += "-" + str(j)
								found = 1
								j = self.binCount
						elif j == self.binCount-1:
							if outcome == float(self.rangeSets[asset][self.binCount-1]):
								self.binSets[asset][self.binCount-1] = self.binSets[asset][self.binCount-1] + 1
								self.totalSets[asset][self.binCount-1] += outcome
								if asset == 0:
									poses += str(j)
								else:
									poses += "-" + str(j)
								found = 1
								j = self.binCount
						else:
							lower = float(self.rangeSets[asset][j].split("|")[0])
							higher = float(self.rangeSets[asset][j].split("|")[1])
							if outcome > lower and outcome < higher:
								self.binSets[asset][j] = self.binSets[asset][j] + 1
								self.totalSets[asset][j] += outcome
								if asset == 0:
									poses += str(j)
								else:
									poses += "-" + str(j)
								found = 1
								j = self.binCount

						j = j + 1
			self.positions.append(poses)
		self.calcProbs()


	def calcProbs(self):
		for asset in range(0, self.assetCount):
			means = []
			for i in range(0, len(self.binSets[0])):
				try:
					means.append(self.totalSets[asset][i]/self.binSets[asset][i])
				except:
					means.append(0)
			self.meanSets.append(means)

		self.uniqPos.append(self.positions[0])
		for item in self.positions:
			inList = 0
			for q in self.uniqPos:
				if q == item:
					inList = 1
			if inList == 0:
				self.uniqPos.append(item)

		countedPos = []
		for z in range(0, len(self.uniqPos)):
			countedPos.append(0)

		for item in self.positions:
			for n in range(0, len(self.uniqPos)):
				if item == self.uniqPos[n]:
					countedPos[n] += 1

		totProb = 0
		for each in countedPos:
			totProb += each

		for things in countedPos:
			self.probs.append(things/totProb)

		totalmeans = []
		for item in self.uniqPos:
			currMean = 0
			for asset in range(0, self.assetCount):
				num = item.split("-")[asset]
				meanForNum = self.meanSets[asset][int(num)]
				currMean += meanForNum

			totalmeans.append(currMean)

		evofpos = []
		for i in range(0, len(self.uniqPos)):
			evofpos.append(self.probs[i]*totalmeans[i])

		for item in evofpos:
			self.totalev += item


	def getHPR(self, fs):
		hprs = []
		for asset in range(0, self.assetCount):
			hpr = []
			for k in self.uniqPos:
				broken = k.split("-")
				pr = ((0-float(self.meanSets[asset][int(broken[asset])]))/float(self.rangeSets[asset][0])) * fs[asset]
				hpr.append(pr + 1)

			hprs.append(hpr)

		nethpr = []
		for i in range(0, len(hprs[0])):
			totHpr = -2
			for asset in range(0, self.assetCount):
				totHpr += hprs[asset][i]
			nethpr.append(totHpr)

		return nethpr


	def findGHPR(self, fs):
		ghpr = 1.0
		nhprs = self.getHPR(fs)
		for item in nhprs:
			ghpr = ghpr * (item**self.probs[nhprs.index(item)])
		return ghpr


	def findRandomPath(self, numOfIntervals):
		nums = []
		for i in range(0, numOfIntervals):
			nums.append(random.randint(0, len(self.uniqPos)-1))
		return nums


	def createBetaK(self, path, risk, netHPR):
		hprp = []
		probOfNode = 1.0
		for i in range(0, len(path)):
			if i == 0:
				if netHPR[path[0]] > 1.0:
					hprp.append(1.0)
				else:
					hprp.append(netHPR[path[0]])
			else:
				new = hprp[i-1] * netHPR[path[i]]
				if new > 1.0:
					hprp.append(1.0)
				else:
					hprp.append(new)
			probOfNode = probOfNode * self.probs[path[i]]


		hprpb = []
		hprpbSUM = 0
		for item in hprp:
			hprpbSUM += item-risk
			hprpb.append(item-risk)

		hprpbabs = []
		hprpbabsSUM = 0
		for item in hprpb:
			hprpbabsSUM += abs(item)
			hprpbabs.append(abs(item))

		betaK = int(hprpbSUM/hprpbabsSUM)
		output = betaK * probOfNode
		return output, probOfNode


	def calcGPHRs(self, portfolioLimit=.33):
		print("Calculating GPHRs. This may take some time.")
		ranges = [range(101)] * self.assetCount
		new = list(product(*ranges))
		preMovedGs = []
		for each in new:
			fixed = []
			for item in each:
				fi = float(item)/100
				fixed.append(fi)
			preMovedGs.append(fixed)

		preGs = []
		for each in preMovedGs:
			size = 0
			for i in range(0, len(each)):
				size += each[i]
			if size <= portfolioLimit:
				preGs.append(each)

		for i in tqdm(range(0, len(preGs))):
			newGHPR = self.findGHPR(preGs[i])
			try:
				newGHPR = float(newGHPR)
			except:
				newGHPR = newGHPR.real
			info = [newGHPR, preGs[i]]
			self.GHPRs.append(info)
			if newGHPR > self.maxGHPR:
				self.maxGHPR = newGHPR
				self.bestValues = preGs[i]

		self.GHPRs = sorted(self.GHPRs, reverse=True)


	def findBestUnderDrawdown(self, drawdownConstraint, periods, percentChance, extraBranches=False):
		print("\n\nFinding best asset distribution under drawdown constraint. (Loading bar is an estimate, time may exceed loading constraint)")
		lessThan = False
		i = 0
		bestGHPRavail = 0.0
		pbar = tqdm(total=len(self.GHPRs))
		while lessThan == False:
			totalOut = 0
			totalProbs = 0
			nhpr = self.getHPR(self.GHPRs[i][1])
			branchCount = 50000
			if extraBranches == True:
				if len(self.uniqPos)**periods > 6250000:
					branchCount = 6250000
				else:
					branchCount = self.uniqPos**periods
			if branchCount == 50000:
				for j in range(0, branchCount):
					betaK, newProb = self.createBetaK(self.findRandomPath(periods), drawdownConstraint, nhpr)
					totalOut += betaK
					totalProbs += newProb
			else:
				for j in tqdm(range(0, branchCount)):
					betaK, newProb = self.createBetaK(self.findRandomPath(periods), drawdownConstraint, nhpr)
					totalOut += betaK
					totalProbs += newProb

			totValue = (1-(totalOut/totalProbs))

			if float(totValue) < float(percentChance):
				bestValues = self.GHPRs[i][1]
				bestGHPRavail = self.GHPRs[i][0]
				lessThan = True
			else:
				i += 1
			pbar.update(len(self.GHPRs)/500)
		pbar.close()

		nhpr = self.getHPR(bestValues)

		probofnet = 0
		totalofnhpr = 0
		for item in nhpr:
			totalofnhpr += 1
			if item < .97:
				probofnet +=1

		self.underDrawValues = bestValues
		self.underDrawGHPR = bestGHPRavail
		self.probOfDraw = probofnet/totalofnhpr

		return bestValues


	def showStats(self):
		print("\n\nModel Information:")
		print("\nPercent of nhpr that draws beneth drawdown constraint: " + str(self.probOfDraw))
		print("GHPR with chance drawdown below entered drawdown constraint: " + str(self.underDrawGHPR))
		print("Best Allocation under entered percentage chance of drawdown: ")
		print(self.underDrawValues)
		print('\nTotal EV per period with 1/3 position going to each stock: ' + str(self.totalev))
		print("Event distributions:")
		print(self.binSets)




#mod = gphrModel(createDataset())
#mod.defineBins(10)
#mod.calcGPHRs(.20)
#mod.findBestUnderDrawdown(.97, 10, .10)
#mod.showStats()
