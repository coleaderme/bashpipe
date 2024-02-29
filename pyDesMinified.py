#!/usr/bin/env python
L=' bytes'
K='Invalid Initial Value (IV), must be a multiple of '
J='Cannot use a pad character with PAD_PKCS5'
I=str
H=map
F=list
G=bytes
E=print
D=len
A=None
class C:
	def __init__(A,mode=0,IV=A,pad=A,padmode=1):
		F=padmode;C=pad;B=IV
		if B:B=A._guardAgainstUnicode(B)
		if C:C=A._guardAgainstUnicode(C)
		A.block_size=8
		if C and F==2:E(J)
		if B and D(B)!=A.block_size:E(K+I(A.block_size)+L)
		A._mode=mode;A._iv=B;A._padding=C;A._padmode=F
	def getKey(A):return A.__key
	def setKey(B,key):A=key;A=B._guardAgainstUnicode(A);B.__key=A
	def getMode(A):return A._mode
	def setMode(A,mode):A._mode=mode
	def getPadding(A):return A._padding
	def setPadding(C,pad):
		B=pad
		if B is not A:B=C._guardAgainstUnicode(B)
		C._padding=B
	def getPadMode(A):return A._padmode
	def setPadMode(A,mode):A._padmode=mode
	def getIV(A):return A._iv
	def setIV(B,IV):
		A=IV
		if not A or D(A)!=B.block_size:E(K+I(B.block_size)+L)
		A=B._guardAgainstUnicode(A);B._iv=A
	def _padData(B,data,pad,padmode):
		H=padmode;F=pad;C=data
		if H is A:H=B.getPadMode()
		if F and H==2:E(J)
		if H==1:
			if D(C)%B.block_size==0:return C
			if not F:F=B.getPadding()
			if not F:E('Data must be a multiple of '+I(B.block_size)+' bytes in length. Use padmode=PAD_PKCS5 or set the pad character.')
			C+=(B.block_size-D(C)%B.block_size)*F
		elif H==2:K=8-D(C)%B.block_size;C+=G([K]*K)
		return C
	def _unpadData(F,data,pad,padmode):
		D=padmode;C=pad;B=data
		if not B:return B
		if C and D==2:E(J)
		if D is A:D=F.getPadMode()
		if D==1:
			if not C:C=F.getPadding()
			if C:B=B[:-F.block_size]+B[-F.block_size:].rstrip(C)
		elif D==2:G=B[-1];B=B[:-G]
		return B
	def _guardAgainstUnicode(B,data):
		A=data
		if isinstance(A,I):
			try:return A.encode('ascii')
			except UnicodeEncodeError:pass
		return A
class B(C):
	__pc1=[56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3];__left_rotations=[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1];__pc2=[13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,33,52,45,41,49,35,28,31];__ip=[57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7,56,48,40,32,24,16,8,0,58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6];__expansion_table=[31,0,1,2,3,4,3,4,5,6,7,8,7,8,9,10,11,12,11,12,13,14,15,16,15,16,17,18,19,20,19,20,21,22,23,24,23,24,25,26,27,28,27,28,29,30,31,0];__sbox=[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]];__p=[15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24];__fp=[39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25,32,0,40,8,48,16,56,24];ENCRYPT=0;DECRYPT=1
	def __init__(A,key,mode=0,IV=A,pad=A,padmode=1):C.__init__(A,mode,IV,pad,padmode);A.key_size=8;A.L=[];A.R=[];A.Kn=[[0]*48]*16;A.final=[];A.setKey(key)
	def setKey(A,key):C.setKey(A,key);A.__create_sub_keys()
	def __String_to_BitList(F,data):
		A=data;B=0
		for E in A:
			C=7
			while C>=0:
				if E&1<<C!=0:([0]*(D(A)*8))[B]=1
				else:([0]*(D(A)*8))[B]=0
				B+=1;C-=1
		return[0]*(D(A)*8)
	def __BitList_to_String(E,data):
		C=[];A=0;B=0
		while A<D(data):
			B+=data[A]<<7-A%8
			if A%8==7:C.append(B);B=0
			A+=1
		return G(C)
	def __permutate(A,table,block):return F(H(lambda x:block[x],table))
	def __create_sub_keys(A):
		D=A.__permutate(B.__pc1,A.__String_to_BitList(A.getKey()));C=0;A.L=D[:28];A.R=D[28:]
		while C<16:
			E=0
			while E<B.__left_rotations[C]:A.L.append(A.L[0]);del A.L[0];A.R.append(A.R[0]);del A.R[0];E+=1
			A.Kn[C]=A.__permutate(B.__pc2,A.L+A.R);C+=1
	def __des_crypt(A,block,crypt_type):
		I=block;I=A.__permutate(B.__ip,I);A.L=I[:32];A.R=I[32:]
		if crypt_type==B.ENCRYPT:K=0;L=1
		else:K=15;L=-1
		M=0
		while M<16:
			N=A.R[:];A.R=A.__permutate(B.__expansion_table,A.R);A.R=F(H(lambda x,y:x^y,A.R,A.Kn[K]));D=[A.R[:6],A.R[6:12],A.R[12:18],A.R[18:24],A.R[24:30],A.R[30:36],A.R[36:42],A.R[42:]];C=0;E=[0]*32;G=0
			while C<8:O=(D[C][0]<<1)+D[C][5];P=(D[C][1]<<3)+(D[C][2]<<2)+(D[C][3]<<1)+D[C][4];J=B.__sbox[C][(O<<4)+P];E[G]=(J&8)>>3;E[G+1]=(J&4)>>2;E[G+2]=(J&2)>>1;E[G+3]=J&1;G+=4;C+=1
			A.R=A.__permutate(B.__p,E);A.R=F(H(lambda x,y:x^y,A.R,A.L));A.L=N;M+=1;K+=L
		A.final=A.__permutate(B.__fp,A.R+A.L);return A.final
	def crypt(A,data,crypt_type):
		J=crypt_type;C=data
		if not C:return''
		if D(C)%A.block_size!=0:C+=(A.block_size-D(C)%A.block_size)*A.getPadding()
		if A.getMode()==1:
			if A.getIV():K=A.__String_to_BitList(A.getIV())
		L=0;M=[]
		while L<D(C):
			E=A.__String_to_BitList(C[L:L+8])
			if A.getMode()==1:
				if J==B.ENCRYPT:E=F(H(lambda x,y:x^y,E,K))
				I=A.__des_crypt(E,J)
				if J==B.DECRYPT:I=F(H(lambda x,y:x^y,I,K));K=E
				else:K=I
			else:I=A.__des_crypt(E,J)
			M.append(A.__BitList_to_String(I));L+=8
		return G.fromhex('').join(M)
	def encrypt(D,data,pad=A,padmode=A):
		E=pad;C=data;C=D._guardAgainstUnicode(C)
		if E is not A:E=D._guardAgainstUnicode(E)
		C=D._padData(C,E,padmode);return D.crypt(C,B.ENCRYPT)
	def decrypt(D,data,pad=A,padmode=A):
		E=pad;C=data;C=D._guardAgainstUnicode(C)
		if E is not A:E=D._guardAgainstUnicode(E)
		C=D.crypt(C,B.DECRYPT);return D._unpadData(C,E,padmode)
class O(C):
	def __init__(A,key,mode=0,IV=A,pad=A,padmode=1):C.__init__(A,mode,IV,pad,padmode);A.setKey(key)
	def setKey(A,key):
		F=key;A.key_size=24
		if D(F)!=A.key_size:
			if D(F)==16:A.key_size=16
			else:E('Invalid triple DES key size. Key must be either 16 or 24 bytes long')
		if A.getMode()==1:
			if not A.getIV():A._iv=F[:A.block_size]
			if D(A.getIV())!=A.block_size:E('Invalid IV, must be 8 bytes in length')
		A.__key1=B(F[:8],A._mode,A._iv,A._padding,A._padmode);A.__key2=B(F[8:16],A._mode,A._iv,A._padding,A._padmode)
		if A.key_size==16:A.__key3=A.__key1
		else:A.__key3=B(F[16:],A._mode,A._iv,A._padding,A._padmode)
		C.setKey(A,F)
	def setMode(A,mode):
		C.setMode(A,mode)
		for B in(A.__key1,A.__key2,A.__key3):B.setMode(mode)
	def setPadding(A,pad):
		C.setPadding(A,pad)
		for B in(A.__key1,A.__key2,A.__key3):B.setPadding(pad)
	def setPadMode(A,mode):
		C.setPadMode(A,mode)
		for B in(A.__key1,A.__key2,A.__key3):B.setPadMode(mode)
	def setIV(A,IV):
		C.setIV(A,IV)
		for B in(A.__key1,A.__key2,A.__key3):B.setIV(IV)
	def encrypt(C,data,pad=A,padmode=A):
		H=pad;E=data;I=B.ENCRYPT;K=B.DECRYPT;E=C._guardAgainstUnicode(E)
		if H is not A:H=C._guardAgainstUnicode(H)
		E=C._padData(E,H,padmode)
		if C.getMode()==1:
			C.__key1.setIV(C.getIV());C.__key2.setIV(C.getIV());C.__key3.setIV(C.getIV());J=0;L=[]
			while J<D(E):F=C.__key1.crypt(E[J:J+8],I);F=C.__key2.crypt(F,K);F=C.__key3.crypt(F,I);C.__key1.setIV(F);C.__key2.setIV(F);C.__key3.setIV(F);L.append(F);J+=8
			return G.fromhex('').join(L)
		else:E=C.__key1.crypt(E,I);E=C.__key2.crypt(E,K);return C.__key3.crypt(E,I)
	def decrypt(C,data,pad=A,padmode=A):
		H=pad;E=data;L=B.ENCRYPT;I=B.DECRYPT;E=C._guardAgainstUnicode(E)
		if H is not A:H=C._guardAgainstUnicode(H)
		if C.getMode()==1:
			C.__key1.setIV(C.getIV());C.__key2.setIV(C.getIV());C.__key3.setIV(C.getIV());J=0;M=[]
			while J<D(E):K=E[J:J+8];F=C.__key3.crypt(K,I);F=C.__key2.crypt(F,L);F=C.__key1.crypt(F,I);C.__key1.setIV(K);C.__key2.setIV(K);C.__key3.setIV(K);M.append(F);J+=8
			E=G.fromhex('').join(M)
		else:E=C.__key3.crypt(E,I);E=C.__key2.crypt(E,L);E=C.__key1.crypt(E,I)
		return C._unpadData(E,H,padmode)
from sys import argv
import base64 as M
def N():F=B(b'38346591',0,b'\x00\x00\x00\x00\x00\x00\x00\x00',pad=A,padmode=2);C=argv[1];C=M.b64decode(C.strip());D=F.decrypt(C,padmode=2).decode('utf-8');D=D.replace('_96.mp4','_320.mp4');E(D)
N()
