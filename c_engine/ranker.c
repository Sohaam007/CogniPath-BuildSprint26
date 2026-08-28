#include "ranker.h"
#include <stdlib.h>
#include <string.h>

// Comparison function for qsort to sort in descending order
static int compare_patient_scores(const void* a, const void* b) {
    const PatientScore* p1 = (const PatientScore*)a;
    const PatientScore* p2 = (const PatientScore*)b;
    
    if (p1->risk_score < p2->risk_score) return 1;
    if (p1->risk_score > p2->risk_score) return -1;
    return 0;
}

int rank_patients(PatientScore* patients, int count) {
    if (patients == NULL || count <= 0) {
        return -1; // Invalid input
    }
    
    qsort(patients, count, sizeof(PatientScore), compare_patient_scores);
    
    return 0; // Success
}