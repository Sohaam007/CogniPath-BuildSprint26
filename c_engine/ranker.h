#ifndef RANKER_H
#define RANKER_H

typedef struct {
    int id;
    float age;
    float cognitive_score;
    float ptau;
    float final_score;
} PatientRecord;

void rank_patients(PatientRecord* records, int count, float w_age, float w_moca, float w_ptau);

#endif // RANKER_H
