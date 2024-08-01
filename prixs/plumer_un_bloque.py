import struct as st
import matplotlib.pyplot as plt

print("plumer_un_bloque.py ...")
with open('prixs/dar.bin', 'rb') as co:
	bins = co.read()
	#
	I,T,L,N, = st.unpack('IIII', bins[:4*4])
	dar = st.unpack('f'*I*T*L*N, bins[4*4:])
	# 
	t = int(0.99 * T)
	#
	fig, ax = plt.subplots(1 + L, I)
	#
	for i in range(I):
		depart = i*(T*L*N) + t*(L*N)
		bloque = dar[depart:depart+L*N]
		#
		#ax[0][i].imshow([[bloque[l*N + n] for n in range(N)] for l in range(L)])
		ax[0][i].imshow([[bloque[n*L + l] for l in range(L)] for n in range(N)])
		#
		#for l in range(L):
		#	ax[1+l][i].plot(bloque[l*N:l*N+N])
		for l in range(L):#	.T
			ax[1+l][i].plot([bloque[n*L+l] for n in range(N)])
		#
	plt.show()