seq="10011011000111010100"

# if the i-th bit of the number f[i] in a binary form is 1,
# then term x^i is in f(x)
# example: 	if n-th function fn(x)=x^3 + x^2 + 1, 
# 			then fn(x) will be encoded into the n-th element of array f, 
# 			that is f[n] = int("0b1101",2)
f = [0 for i in range(21)]
l = [0 for i in range(21)]
d = [0 for i in range(21)]
f[0]=1
f[1]=0b11 #f1(x)=x+1
d[0]=1
l[0]=0
l[1]=1
min = 0

# @params f: the encoded decimal form of a function
# @params n: the degree of the function f
# convert f to a string
# example: 	if f = 3, then f=0b11, the return string will be "1 + x"
# 			if f = 11, then f=0b1011, the return string will be "1 + x^2 + x^3" 
def ftostr(f,n):
	fstr = "1 "
	for i in range (1, len(bin(f))-2):
		mask = 1 << i
		if bin(f & mask) != '0b0':
			if i > 1 : fstr+="+ x^{%d} " % i 
			else: fstr+="+ x ".format(i)
	fstr+=""
	return fstr

#to generate latex code of bm algorithm
for i in range(1,20):
	flen = len(bin(f[i]))-2
	d[i] = f[i] & int("0b" + seq[i-flen+1:i+1],2)
	print("计算$d_{%d}={%d}$，" % (i, bin(d[i]).count('1') % 2))
	print("$m={0}$。".format(min))
	if bin(d[i]).count('1') % 2 == 1:
		f[i+1] = f[i] ^ (f[min] << (i - min))
		print("$f_{%d}(x) = f_{%d}(x) + x^{%d-%d}f_{%d}(x)$\\\\" % (i+1, i, i, min, min))
		print("$f_{%d}(x) = %s + x^{%d}(%s)$\\\\" % (i+1, ftostr(f[i],i), i-min, ftostr(f[min],min)))
		print("$f_{%d}(x) = %s$\\\\" % (i+1, ftostr(f[i+1],i+1)))
		l[i+1] = max(l[i], i+1-l[i])
		print("$l_{%d}=max(l_{%d}, %d-l_{%d})=%d$" % (i+1, i, i+1, i, l[i+1]) )
		if i+1 - l[i] > l[i] : 
			min = i
	else:
		f[i+1] = f[i]
		print("$f_{%d}(x) = f_{%d}(x) = %s$。" % (i+1, i, ftostr(f[i+1],i+1)))
		l[i+1] = l[i]
		print("$l_{%d}=l_{%d} = %d$" % (i+1, i ,l[i]))
	print("\n~\\\\")
	