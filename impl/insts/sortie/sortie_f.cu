#include "sortie.cuh"

__global__
static void kerd__sortie(
	uint x0_t, uint X0, float * x0,
	//
	uint    Y,
	float * y,
	//
	uint * ts__d, uint mega_t)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x;
	uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (_y < Y && _t < GRAND_T) {
		uint tx0 = t_MODE(_t-x0_t, mega_t);
		uint ty  = t_MODE(_t,      mega_t);
		//
		y[ty*Y + _y] = x0[tx0*X0 + _y];
	};
};

void sortie__f(Inst_t * inst, float ** x__d, uint * ts__d, uint mega_t) {
	uint Y = inst->Y;
	//
	kerd__sortie<<<dim3(KERD(Y,16), KERD(GRAND_T,16)), dim3(16,16)>>>(
		inst->x_t[0], inst->x_Y[0], x__d[0],
		//
		inst->Y,
		inst->y__d,
		//
		ts__d, mega_t
	);
};