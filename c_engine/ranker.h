#ifndef RANKER_H
#define RANKER_H

typedef struct {
    char patient_id[32];
    double risk_score;
} PatientScore;

// Sorts an array of PatientScore structs in descending order of risk_score
// returns 0 on success, non-zero on failure
int rank_patients(PatientScore* patients, int count);

#endif // RANKER_H