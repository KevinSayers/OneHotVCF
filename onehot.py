#!python3
import vcf
import os

def generatePositionList(vcfList):
	positionList = []

	for i in vcfList:
		try:
			for record in i:
				if(record.POS not in positionList):
					positionList.append(record.POS)
		except:
			print ("failed: %s"%(i.filename))
	return positionList

def encodeVCF(vcf, positionList):
	encodedList = []
	vcfPOS = [x.POS for x in vcf]
	for i in positionList:
		if(i in vcfPOS):
			encodedList.append(1)
		else:
			encodedList.append(0)

	return encodedList
#Find unique implement so given two lists the function returns two lists with the
#SNPs found only in the inputted list
def findUnique():
	pass


def main():

	inputFolder = r'/home/kevin/Masters_thesis/MachineLearningWF/newtest/'
	outputFilename = 'transcriptome'
	sampletypedict = {}
	samples = open('/home/kevin/Masters_thesis/Barracuda/TranscriptsampleList.csv')
	for i in samples:
		i = i.strip()
		sampletypedict[i.split(',')[0].split('_')[0]] = i.split(',')[1]
	
	files = os.listdir(inputFolder)
	vcflist = []
	for vcffile in files:
		if vcffile.endswith(".vcf"):
			try:
				vcflist.append(vcf.Reader(open(inputFolder+vcffile,'r')))
			except:
				print ('error with file: %s'%(vcffile))

	encodedVCFs = {}
	posList = sorted(generatePositionList(vcflist))
	print ("Encoded positions: %s"%(len(posList)))
	for vcffile in files:
		if vcffile.endswith(".vcf"):
			encodedVCFs[vcffile] = encodeVCF(vcf.Reader(open(inputFolder+vcffile,'r')),posList)



	outfile = open(outputFilename,'w')
	for i in encodedVCFs.keys():
		try:
			sampletype = sampletypedict[i.split('_')[0]]
			outfile.write("%s,%s,%s\n"%(i,sampletype,",".join(str(x) for x in encodedVCFs[i])))
		except:
			print ("Failed: %s"%(i))




if __name__ == "__main__":
	main()


