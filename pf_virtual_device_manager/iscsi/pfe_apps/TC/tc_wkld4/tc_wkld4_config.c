#include "tc_wkld4_config.h"

/* config environment variable */
const char *txn_size_environ = "N_KEY_PER_TXN";
const char *thread_number_environ = "N_THR";

const char* n_thr_environ = "N_THR";
const char* n_txn_per_thr_environ = "N_TXN_PER_THR";
const char* n_key_per_txn_environ = "N_KEY_PER_TXN";
const char* n_meta_keys_environ = "N_META_KEYS";
const char* n_work_keys_environ = "N_WORK_KEYS";
const char* n_tot_keys_environ = "N_TOT_KEYS";
const char* work_key_start_environ = "WORK_KEY_START";
const char* work_key_end_environ = "WORK_KEY_END";


const char *db_file_environ = "TC_WKLD4_DB_FILE";

/* config variable, and its default value */
int thread_number = 10;
int txn_size = 10;

int n_thr = 10;
int n_txn_per_thr = 10;
int n_key_per_txn = 10;
int n_meta_keys = 100; //n_thr * n_txn_per_thr
int n_work_keys = 1000;
int n_tot_keys = 1100; //n_meta_keys + n_work_keys
int work_key_start = 101; //n_meta_keys + 1    
int work_key_end = 1100; //n_tot_keys


char *db_file = "/tmp/casket.tcb";
