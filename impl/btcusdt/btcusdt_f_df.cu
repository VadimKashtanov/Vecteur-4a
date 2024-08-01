#include "btcusdt.cuh"

#include "../../impl_template/tmpl_etc.cu"

static __global__ void k__f_df_btcusdt(
	float * S,
	//
	float * y, float * dy,
	float * w,
	//
	uint * ts__d,
	//
	uint I, uint T, uint L, uint N)
{
	uint _y = threadIdx.x + blockIdx.x * blockDim.x; 
	//uint _t = threadIdx.y + blockIdx.y * blockDim.y;
	//uint  i = threadIdx.z + blockIdx.z * blockDim.z;
	//
	if (_y < (L*N)/* && _t < T *//*&& i < I*/) {
		float s = 0;
		FOR(0, i, I) {
			FOR(0, _t, GRAND_T) {
				FOR(0, mega_t, MEGA_T) {
					uint ty        = t_MODE(_t, mega_t);
					uint t_btcusdt = ts__d[_t] + 1 + mega_t;
					assert(t_btcusdt < T);
					//
					float __y = y[ty*I*L*N + i*L*N + _y];
					float __w = w[i*T*L*N  + t_btcusdt*L*N  +  _y];
					assert(__y >= -100 && __y <= +100);
					//
					float coef = (float)(GRAND_T * MEGA_T * (I*L*N));
					s       += ( score_p2(__y, __w, 2));
					float ds = (dscore_p2(__y, __w, 2)) / coef;
					//
					atomicAdd(&dy[ty*I*N*L + i*L*N + _y], ds);
				}
			}
		}
		//
		atomicAdd(&S[0], s);
	}
};

/*
A fair :
	1) Finir d'ajouter les jour, mois année
	2) Tester le .T dar.bin
	3) ajouter le module de séparation des I (et embede et positionnal)
	4) Ajouter une union 4
*/

float f_df_btcusdt(BTCUSDT_t * btcusdt, float * y__d, float * dy__d, uint * ts__d) {
	uint I=btcusdt->I;
	uint L=btcusdt->L;
	uint N=btcusdt->N;
	uint T=btcusdt->T;
	//
	float * S__d = cudalloc<float>(1);
	k__f_df_btcusdt<<<dim3(KERD((L*N), 8)/*,KERD(GRAND_T, 8), *//*KERD(I,4)*/), dim3(8/*,8,*//*4*/)>>>(
		S__d,
		y__d, dy__d,
		btcusdt->serie__d,
		ts__d,
		btcusdt->I, btcusdt->T, btcusdt->L, btcusdt->N
	);
	ATTENDRE_CUDA();
	//
	//
	float * S = gpu_vers_cpu<float>(S__d, 1);
	//
	float coef = (float)(GRAND_T * MEGA_T * (I*L*N));
	float score = S[0]/coef;// / ((float)(MEGA_T * btcusdt->I * btcusdt->L * btcusdt->N));
	//
	//
	cudafree<float>(S__d);
	    free       (S   );
	//
	return score;
};