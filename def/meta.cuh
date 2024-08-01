#pragma once

#include "etc.cuh"

//	Les Parantèses () sont importantes.

#define INTERVS 4

#define GRAND_T 16

#define MEGA_T 1

#define PLUS_DECALAGE 1

#define t_MODE(t, mega_t) ( (t)*(MEGA_T) + (mega_t) )