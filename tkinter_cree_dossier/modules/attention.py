from tkinter_cree_dossier.modules._etc import *

from tkinter_cree_dossier.modules.dot1d import *

class ATTENTION_2D(Module_Mdl):
	bg, fg = 'light blue', 'black'
	nom = "[ATTENTION 2D]"
	X, Y = [0], [0]
	X_noms, Y_noms = ["X"], ["Y"]
	params = {
		'Ax' : 1,
		'Ay' : 1,
		'Clef' : 1,
		'Vx' : 1,
		'C0' : 1,
	}
	def cree_ix(self):
		#	Params
		X = self.X[0]
		Y = self.Y[0]

		Ax = self.params['Ax']
		Ay = self.params['Ay']

		Clef = self.params['Clef']

		Vx = self.params['Vx']

		C0 = self.params['C0']

		#	------------------

		do = self.do

		self.elements = {
			#'x' : MODULE_i_Canalisation  (X=[Ax*Ay],    Y=[Ax*Ay*C0], params={'C0':C0}).cree_ix(),
			'x' : MODULE_i_Y(X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={}).cree_ix(),
			#
			'q' : MODULE_i_MatMul_Poid_AP(X=[Ax*Ay*C0], Y=[Clef*Ay*C0], params={'Ax':Ax, 'Ay':Ay, 'Bx':Clef, 'C0':C0}).cree_ix(),
			'k' : MODULE_i_MatMul_Poid_AP(X=[Ax*Ay*C0], Y=[Clef*Ay*C0], params={'Ax':Ax, 'Ay':Ay, 'Bx':Clef, 'C0':C0}).cree_ix(),
			'v' : MODULE_i_MatMul_Poid_AP(X=[Ax*Ay*C0], Y=[Vx  *Ay*C0], params={'Ax':Ax, 'Ay':Ay, 'Bx':Vx,   'C0':C0}).cree_ix(),
			#
			#'k.T' : MODULE_i_Transpose2d (X=[Clef*Ay*C0], Y=[Ay*Clef*C0], params={'Ax':Clef, 'Ay':Ay, 'C0':C0}).cree_ix(),
			#
			'q@k.T' :            MODULE_i_QKtDivClef(X=[Clef*Ay*C0, Ay*Clef*C0], Y=[Ay*Ay*C0], params={'Ax':Clef, 'Ay':Ay, 'Bx':Ay, 'C0':C0}, do=0, dc=0).cree_ix(),
			'softmax(q@k.T)' :   SOFTMAX            (X=[       Ay*Ay*C0       ], Y=[Ay*Ay*C0], params={'C0':Ay*C0},                           do=0, dc=0).cree_ix(),
			'softmax(q@k.T)@v' : MODULE_i_MatMul    (X=[  Ay*Ay*C0, Vx*Ay*C0  ], Y=[Vx*Ay*C0], params={'Ax':Ay,   'Ay':Ay, 'Bx':Vx, 'C0':C0}, do=do,dc=0).cree_ix()
		}

		self.connections = {
			'x' : {0:None},
			#
			'q' : {0:('x',0)},
			'k' : {0:('x',0)},
			'v' : {0:('x',0)},
			#
			#'k.T' : {0:('k',0)},
			#
			'q@k.T'            : {0:('q',0), 1:('k',0)},
			'softmax(q@k.T)'   : {0:('q@k.T', 0)},
			'softmax(q@k.T)@v' : {0:('softmax(q@k.T)', 0), 1 : ('v', 0)}
		
		}

		self.cree_elements_connections()
		return self.ix

class Encodeur(Module_Mdl):
	bg, fg = 'light blue', 'black'
	nom = "[Encodeur]"
	X, Y = [0], [0]
	X_noms, Y_noms = ["X"], ["Y"]
	params = {
		'Ax' : 1,
		'Ay' : 1,
		'C0' : 1,
	}
	def cree_ix(self):
		#	Params
		X = self.X[0]
		Y = self.Y[0]

		Ax = self.params['Ax']
		Ay = self.params['Ay']

		Clef = Ax

		Vx = Ax

		C0 = self.params['C0']

		#	------------------

		do = self.do

		self.elements = {
			'x' : MODULE_i_Y(X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={}).cree_ix(),

			'positionnal encoding' : "positionnal encoding (apres le embeding)",
			
			'norme_x'   : BATCH_NORM(X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={'C0':C0*Ay}).cree_ix(),
			'attention' : ATTENTION_2D (X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={'Ax':Ax,'Ay':Ay,'Clef':Clef,'Vx':Vx,'C0':C0}).cree_ix(),

			'somme0' : MODULE_i_Somme(X=[Ax*Ay*C0, Ax*Ay*C0], Y=[Ax*Ay*C0], params={}).cree_ix(),

			'norme_somme0' : BATCH_NORM(X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={'C0':C0*Ay}).cree_ix(),
			'GeLu(Wx+b)'   : DOT1D        (X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={'C0':C0,'activ':f_GELU}).cree_ix(),
			'W@relu+b'     : DOT1D        (X=[Ax*Ay*C0], Y=[Ax*Ay*C0], params={'C0':C0,'activ':f_Id}).cree_ix(),

			'somme1' : MODULE_i_Somme(X=[Ax*Ay*C0, Ax*Ay*C0], Y=[Ax*Ay*C0], params={}).cree_ix(),
		}

		self.connections = {
			'x' : {0:None},

			#'norme_x' : {0:('x',0)},
			'attention' : {0:('x',0)},#{0:('norme_x',0)},

			'somme0' : {0:('x',0), 1:('attention',0)},

			'norme_somme0' : {0:('somme0',0)},
			'GeLu(Wx+b)' : {0:('somme0',0)},#{0:('norme_somme0',0)},
			'W@relu+b' : {0:('GeLu(Wx+b)',0)},

			'somme1' : {0:('somme0',0), 1:('W@relu+b',0)}
		}

		self.cree_elements_connections()
		return self.ix