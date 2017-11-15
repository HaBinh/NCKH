#!/usr/bin/python

import sys
import subprocess
import codecs
import re

chuoiamvi = []
EndWithR = ['EH', 'UH', 'AO', 'AA', 'IH', 'IY', 'AW']
Vowel =['AO', 'AA', 'IY', 'UW', 'EH', 'IH', 'UH', 'AH', 'AX', 'AE', 'EY', 'AY', 'OW', 'AW'
, 'OY', 'ER', 'AXR', 'EH R', 'UH R', 'AO R', 'AA R', 'IH R', 'IY R', 'AW R']
chuoiamtiet =[]
VowelNotCombineConsonant= ['EY', 'AY', 'OW', 'AW', 'OY', 'UH R', 'AW R']
Coda = ['M', 'N', 'NG', 'P', 'T', 'K']
dict ={'AO': 'O', 'AA' : 'A', 'IY': 'I', 'UW': 'u', 'EH':'E', 'IH': 'I', 'UH' :'u', 'AH': 'oUs','AX': 'oU', 'AE':'E',
'EY': 'oUs ji', 'AY': 'a ji', 'OW': 'oUs wu', 'AW': 'a wu', 'OY': 'Os ji', 'ER': 'oU', 'AXR': 'oU', 'EH R': 'E', 'UH R': 'Uo', 'AO R': 'O', 'AA R':'A',
'IH R' : 'ie', 'IY R' :'ie' , 'AW R': 'a wu',
'P': 'p', 'B': 'b', 'T':'t', 'D': 'd', 'K':'k', 'G': 'G',
'CH' : 'c', 'JH': 'z', 
'F': 'f', 'V':'v', 'TH': 'tH', 'DH' : 'z', 'S': 's', 'Z': 'z' , 'SH': 'sr',
'ZH' : 'z', 'HH' : 'h',
'M': 'm', 'EM': 'm', 'N': 'n','EN': 'n', 'NG': 'N', 'ENG': 'i N', 
'L': 'l', 'EL': 'o', 'R' : 'zr', 'DX':'t', 'NX': 't', 
'Y': 'z', 'W': 'w', 'Q': 'Q'}
chuoiamtietVn =[]  # mang am tiet tieng viet
amtietcon = []
amviVn =""
amtietVn=""
ExceptionVowelGroup1 = ['IH', 'IY' ,'AX', 'IX', 'ER', 'AXR', 'UH R' ]
ExceptionConsonantGroup1 = ['NG', 'ENG']
ExceptionVowelGroup2= ['AX', 'IX', 'ER', 'AXR', 'UH R' ]
StopConsonants= ['p','t','k']
def IsEndWithR(amvi):
	if amvi in EndWithR:
		return 1
	else:
		return 0	

def IsVowel(amvi):
	if amvi in Vowel:
		return 1
	else:
		return 0	

def IsVowelNotCombineConsonant(amvi):
	if amvi in VowelNotCombineConsonant:
		return 1
	else:
		return 0

def IsCoda(amvi):
	if amvi in Coda:
		return 1
	else:
		return 0

def IsKey(amviEn):
	KeyDic= dict.keys()
	if amviEn in KeyDic:
		return dict[amviEn]
	else:
		return 0	

def IsKAndW(chuoiamvi):
	pos = 0;
	while (pos < len(chuoiamvi)-1):
		if(chuoiamvi[pos] == 'K'):
			if(chuoiamvi[pos+1] == 'W'):
				chuoiamvi[pos] = chuoiamvi[pos]+" "+ chuoiamvi[pos+1]
				chuoiamvi.remove(chuoiamvi[pos+1])
		pos+=1	
	return chuoiamvi		

def IsHasPhonemeEndWithR(chuoiamvi):
	pos=1
	while (pos < len(chuoiamvi)):
		#kiem tra co phai la am vi co 'R'
		if(chuoiamvi[pos] == 'R'):
			if(IsEndWithR(chuoiamvi[pos-1]) == 1):
				chuoiamvi[pos-1] = chuoiamvi[pos-1]+" "+ chuoiamvi[pos]
				chuoiamvi.remove(chuoiamvi[pos])
		pos+=1		
	return chuoiamvi

def IsSpace(inputchuoiamvi):
	global chuoiamvinotspace
	chuoiamvinotspace = []
	for amvi in inputchuoiamvi:
		chuoiamvinotspace.extend(amvi.strip().split(' '))
	return chuoiamvinotspace

# Ham tach am vi
def PhonemeSeparation(chuoiamvi):
	# Tach am vi
	# print "------vong lap 1"
	pos=0
	while (pos < len(chuoiamvi)):
		#kiem tra co phai la am vi co phai la nguyen am
		if(IsVowel(chuoiamvi[pos]) == 1):
			chuoiamtiet.append(chuoiamvi[pos])
		else:
			chuoiamtiet.append(0)
		pos+=1	
	# print chuoiamtiet
	# them phu am truoc nguyen am
	# print "------vong lap 2"
	pos=1
	while (pos < len(chuoiamvi)):
		if(IsVowel(chuoiamvi[pos]) == 1):
			if(IsVowel(chuoiamvi[pos-1]) == 0):
				chuoiamtiet[pos]=chuoiamvi[pos-1] + " "+ chuoiamvi[pos]
				chuoiamtiet[pos-1] = 1		
		pos+=1	
	# print chuoiamtiet

	# them phu am sau nguyen am
	# print "------vong lap 3"
	pos=1
	while (pos < len(chuoiamvi)):
		if(chuoiamtiet[pos] == 0):
			if(IsVowel(chuoiamvi[pos-1]) == 1 and IsVowelNotCombineConsonant(chuoiamvi[pos-1]) == 0 
				and IsCoda(chuoiamvi[pos]) == 1):
				chuoiamtiet[pos-1]=chuoiamtiet[pos-1] + " "+ chuoiamvi[pos]
				chuoiamtiet[pos] = 1		
		pos+=1	
	# print chuoiamtiet

	# print "------vong lap 4"
	pos=0
	while (pos < len(chuoiamvi)):
		if(chuoiamtiet[pos] == 0):
			chuoiamtiet[pos] = chuoiamvi[pos] + " " + 'AX'	
		pos+=1	
	# print chuoiamtiet

	# output chuoi am tiet

	while 1 in chuoiamtiet: 
		chuoiamtiet.remove(1)
	return chuoiamtiet


#Ham xu ly cac ngoai le truoc khi anh xa
def IsException(chuoiamvi):
	# AH and AX
	if(chuoiamvi[len(chuoiamvi)-1] == 'AH'):
		chuoiamvi[len(chuoiamvi)-1] = 'AX'

	#Group 1:
	#Vowel: = 'IH', 'IY' ,'AX', 'IX', 'ER', 'AXR', 'UH R'
	#Consonant := 'NG', 'ENG'
	posGroup1 = 0
	while(posGroup1 < len(chuoiamvi)-1):
		if chuoiamvi[posGroup1] in ExceptionVowelGroup1:
			if chuoiamvi[posGroup1+1] in ExceptionConsonantGroup1:
				chuoiamvi[posGroup1+1] = 'EN'
		posGroup1+=1
	
	# Group 2:
	#Vowel: = 'AX', 'IX', 'ER', 'AXR', 'UH R'
	#Consonant: ='K'

	posGroup2 =0
	while(posGroup2 < len(chuoiamvi)-1):
		if chuoiamvi[posGroup2] in ExceptionVowelGroup1:
			if(chuoiamvi[posGroup2+1] == 'K'):
				chuoiamvi[posGroup2] = 'AH'
		posGroup2+=1

	return chuoiamvi


# Ham am xa
def Mapping(chuoiamtiet):
	global amviVn, amtietVn
	for amtiet in chuoiamtiet:
		amtietVn =""  # khoi tao ban dau am tiet tieng viet
		amtietEn = re.findall(r'[\w+]{1,4}[\s]',amtiet+" ") # 1 am tiet trong tieng anh + " "
		amtietEnNotSpace = IsSpace(amtietEn)
		amtietEn = IsHasPhonemeEndWithR(amtietEnNotSpace) 
		amtietEn = IsException(amtietEn)
		# print amtietEn
		for amviEn in amtietEn:			
  			amviVn = IsKey(amviEn)   # anh xa sang am vi tieng viet	  
  			# print amviVn		 
	  		amtietVn += str(amviVn + " ")  # am tiet tieng viet doi voi 1 am tiet tieng anh
	  	# Sac hoa
	  	if amviVn in StopConsonants:
	  		amtietVn+='_7'
	  	else:
	  		amtietVn+='_1'	
	  	chuoiamtietVn.append(amtietVn)
	return chuoiamtietVn	

#HAM CHINH
### code import perl script
tutienganh =sys.argv[1].upper();

perl_script = subprocess.Popen(["t2p_dt_test.pl", tutienganh], stdout=subprocess.PIPE , shell=True)
result = perl_script.stdout.read()
print "*****Using 2tp*****"
print result
amvi = re.findall(r'[\w+]{1,4}[\s]',result) # lay ra chuoi am vi

# Tien xu ly chuoi am vi
for elem in amvi:
    chuoiamvi.extend(elem.strip().split(' '))   # xoa dau cach
# print chuoiamvi

#xoa am vi '_'
while '_' in chuoiamvi: 
	chuoiamvi.remove('_')

#ket hop cac am vi doi voi 'R' neu dung
chuoiamvi = IsHasPhonemeEndWithR(chuoiamvi)

# Xu Li truong hop: K va W
chuoiamvi = IsKAndW(chuoiamvi)

#Tach am vi
chuoiamvi = PhonemeSeparation(chuoiamvi)
print "*****After Phoneme Separation*****"
print chuoiamvi

# Mapping am tiet tieng anh thanh am tiet tieng viet
print "*****Vietnamese Syllables*****"
print Mapping(chuoiamtiet) 
