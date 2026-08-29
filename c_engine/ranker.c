#include "ranker.h"
#include <stdlib.h>

#ifdef _OPENMP
#include <omp.h>
#endif

// Comparison function for qsort to sort in descending order of final_score
static int compare_records(const void* a, const void* b) {
    const PatientRecord* p1 = (const PatientRecord*)a;
    const PatientRecord* p2 = (const PatientRecord*)b;
    
    if (p1->final_score < p2->final_score) return 1;
    if (p1->final_score > p2->final_score) return -1;
    return 0;
}

void rank_patients(PatientRecord* records, int count, float w_age, float w_moca, float w_ptau) {
    if (records == NULL || count <= 0) {
        return;
    }

    #ifdef _OPENMP
    #pragma omp parallel for if(count > 500) schedule(static)
    #endif
    for (int i = 0; i < count; i++) {
        records[i].final_score = ((30.0f - records[i].cognitive_score) * w_moca) +
                                 (records[i].ptau * w_ptau) +
                                 ((records[i].age - 55.0f) * w_age);
    }

    qsort(records, count, sizeof(PatientRecord), compare_records);
}
