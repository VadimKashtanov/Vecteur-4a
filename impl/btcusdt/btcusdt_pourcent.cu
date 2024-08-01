#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

static __global__ void k__pourcent_btcusdt_stricte(
	float * inconnue_____somme,
	float *   connue_____somme,
	//
	float * y, float * w,
	uint * ts__d,
	//
	uint i,	//	Interv
	//
	uint I, uint T, uint L, uint N)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x;
	uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//
	if (_y%N!=0 && _y < L*N && _t < GRAND_T) {
		FOR(0, mega_t, MEGA_T) {
			uint ty        = t_MODE(_t, mega_t);
			uint t_btcusdt = ts__d[_t] + 1 + mega_t;
			//
			uint wpos = i*T*L*N + t_btcusdt*L*N + _y;
			//
			float delat_w = w[wpos     ] / w[wpos     -1] - 1;
			float delta_y = y[ty*I*L*N + i*L*N + _y] / y[ty*I*L*N + i*L*N + _y-1] - 1;
			//
			float a_t_il_predit = (float)(sng(delat_w) == sng(delta_y));
			//
			if (_y % N == N-1) atomicAdd(&inconnue_____somme[i], a_t_il_predit);
			else               atomicAdd(&  connue_____somme[i], a_t_il_predit);
		}
	}
};

float* pourcent_btcusdt(BTCUSDT_t * btcusdt, float * y__d, uint * ts__d) {
	uint I=btcusdt->I;
	uint L=btcusdt->L;
	uint N=btcusdt->N;
	uint T=btcusdt->T;
	//
	float * inconnue_____somme__d = cudalloc<float>(btcusdt->I);
	float *   connue_____somme__d = cudalloc<float>(btcusdt->I);
	//
	FOR(0, i, btcusdt->I) {
		k__pourcent_btcusdt_stricte<<<dim3(KERD((L*N), 16), KERD(GRAND_T, 16)), dim3(16,16)>>>(
			inconnue_____somme__d,
			  connue_____somme__d,
			y__d, btcusdt->serie__d,
			ts__d,
			i,
			btcusdt->I, btcusdt->T, btcusdt->L, btcusdt->N
		);
	}
	ATTENDRE_CUDA();
	//
	float * inconnue_____somme = gpu_vers_cpu<float>(inconnue_____somme__d, btcusdt->I);
	float *   connue_____somme = gpu_vers_cpu<float>(  connue_____somme__d, btcusdt->I);
	//
	float * ret = alloc<float>(btcusdt->I * 2);
	FOR(0, i, btcusdt->I) {
		inconnue_____somme[i] = inconnue_____somme[i] / (float)(MEGA_T*I*(L*N-1-1));
		  connue_____somme[i] =   connue_____somme[i] / (float)(MEGA_T*I*(+1     ));
		//
		ret[0*btcusdt->I + i] = inconnue_____somme[i];
		ret[1*btcusdt->I + i] =   connue_____somme[i];
	}
	//
	cudafree<float>(inconnue_____somme__d);
	cudafree<float>(  connue_____somme__d);
	    free       (inconnue_____somme   );
	    free       (  connue_____somme   );
	//
	return ret;
};
