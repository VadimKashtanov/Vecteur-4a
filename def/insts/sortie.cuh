#pragma once

#include "insts.cuh"

#define sortie__Xs INTERVS//1
#define sortie__Ys 1
#define sortie__PARAMS 0
#define sortie__Nom "sortie"

uint sortie__calculer_P(uint X[MAX_XS], uint x[MAX_XS], uint t[MAX_XS], uint Y, uint params[MAX_PARAMS]);
uint sortie__calculer_L(uint X[MAX_XS], uint x[MAX_XS], uint t[MAX_XS], uint Y, uint params[MAX_PARAMS]);

void sortie__init_poids(Inst_t * inst);

void sortie__f(Inst_t * inst, float ** x__d, uint * ts__d, uint mega_t);
void sortie__df(Inst_t * inst, float ** x__d, float ** dx__d, uint * ts__d, uint mega_t);

void sortie__pre_f(Inst_t * inst);

static fonctions_insts_t fi_sortie = {
	.Xs    =sortie__Xs,
	.PARAMS=sortie__PARAMS,
	.Nom   =sortie__Nom,
	//
	.calculer_P=sortie__calculer_P,
	.calculer_L=sortie__calculer_L,
	//
	.init_poids=sortie__init_poids,
	//
	.f =sortie__f,
	.df=sortie__df,
	//
	.pre_f=sortie__pre_f
};