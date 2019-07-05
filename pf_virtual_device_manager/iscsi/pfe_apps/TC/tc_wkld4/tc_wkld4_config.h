#ifndef _TC_WKLD2_H
#define _TC_WKLD2_H

// non-zero: open
#define DEBUG_MODE  0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <stdint.h>
#include <inttypes.h>
#include <pthread.h>
#include <sys/time.h>
#include <tcutil.h>
#include <tcbdb.h>
#include <stdbool.h>

/* define */
#define BUF_SIZE  (100)
#define LONG_PATH (300)
#define __PREFIX  "tc_wkld4:"
#define PFE_LOG_DIR "PFE_LOG_DIR"
#define IO_CUT_TM_FILE  "formatted.io.txt"
#define COMMIT_TM_FILE  "hdc_cm_tm_file.txt"
#define CUT_IO_NUM  "CUT_IO_NUM"
#define KEYPRE  "key"
#define VALPRE  "value"

/* define failure msg */
#define APASSED "Atomicity passed"
#define AFAILED "Atomicity failed"
#define CPASSED "Consistency passed"
#define CFAILED "Consistency failed"
#define DPASSED "Durability passed"
#define DFAILED "Durability failed"
#define DCANCEL "Durability cancelled"
#define DUNKNOWN  "Durability unknown"

//wkld 4
#define W4_KEY_BUFSIZE (32)
#define W4_VAL_BUFSIZE (4096)
#define W4_MAX_N_KEY_PER_TXN (800)

/* extern */
extern const char *txn_size_environ;
extern const char *thread_number_environ;
extern const char *db_file_environ;

extern const char* n_thr_environ;
extern const char* n_txn_per_thr_environ;
extern const char* n_key_per_txn_environ;
extern const char* n_meta_keys_environ;
extern const char* n_work_keys_environ;
extern const char* n_tot_keys_environ;
extern const char* work_key_start_environ;
extern const char* work_key_end_environ;


extern int txn_size;
extern int thread_number;
extern char *db_file;
extern char *db_file;

extern int n_thr;
extern int n_txn_per_thr;
extern int n_key_per_txn;
extern int n_meta_keys;
extern int n_work_keys;
extern int n_tot_keys;
extern int work_key_start;
extern int work_key_end;



inline static void config_n_thr() {
    char *tmp = NULL;

    tmp = getenv(n_thr_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_thr:%s doesn't exist,"
                "use default value %d.\n",
                n_thr_environ, n_thr);
    } else {
        fprintf(stderr, __PREFIX "config_n_thr:%s exist,"
                "use its value %s.\n",
                n_thr_environ, tmp);
        n_thr = atoi(tmp);
    }
}

inline static void config_n_txn_per_thr() {
    char *tmp = NULL;

    tmp = getenv(n_txn_per_thr_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_txn_per_thr:%s doesn't exist,"
                "use default value %d.\n",
                n_txn_per_thr_environ, n_txn_per_thr);
    } else {
        fprintf(stderr, __PREFIX "config_n_txn_per_thr:%s exist,"
                "use its value %s.\n",
                n_txn_per_thr_environ, tmp);
        n_txn_per_thr = atoi(tmp);
    }
}

inline static void config_n_key_per_txn() {
    char *tmp = NULL;

    tmp = getenv(n_key_per_txn_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_key_per_txn:%s doesn't exist,"
                "use default value %d.\n",
                n_key_per_txn_environ, n_key_per_txn);
    } else {
        fprintf(stderr, __PREFIX "config_n_key_per_txn:%s exist,"
                "use its value %s.\n",
                n_key_per_txn_environ, tmp);
        n_key_per_txn = atoi(tmp);
    }
}

inline static void config_n_meta_keys() {
    char *tmp = NULL;

    tmp = getenv(n_meta_keys_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_meta_keys:%s doesn't exist,"
                "use default value %d.\n",
                n_meta_keys_environ, n_meta_keys);
    } else {
        fprintf(stderr, __PREFIX "config_n_meta_keys:%s exist,"
                "use its value %s.\n",
                n_meta_keys_environ, tmp);
        n_meta_keys = atoi(tmp);
    }
}

inline static void config_n_work_keys() {
    char *tmp = NULL;

    tmp = getenv(n_work_keys_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_work_keys:%s doesn't exist,"
                "use default value %d.\n",
                n_work_keys_environ, n_work_keys);
    } else {
        fprintf(stderr, __PREFIX "config_n_work_keys:%s exist,"
                "use its value %s.\n",
                n_work_keys_environ, tmp);
        n_work_keys = atoi(tmp);
    }
}

inline static void config_n_tot_keys() {
    char *tmp = NULL;

    tmp = getenv(n_tot_keys_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_n_tot_keys:%s doesn't exist,"
                "use default value %d.\n",
                n_tot_keys_environ, n_tot_keys);
    } else {
        fprintf(stderr, __PREFIX "config_n_tot_keys:%s exist,"
                "use its value %s.\n",
                n_tot_keys_environ, tmp);
        n_tot_keys = atoi(tmp);
    }
}

inline static void config_work_key_start() {
    char *tmp = NULL;

    tmp = getenv(work_key_start_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_work_key_start:%s doesn't exist,"
                "use default value %d.\n",
                work_key_start_environ, work_key_start);
    } else {
        fprintf(stderr, __PREFIX "config_work_key_start:%s exist,"
                "use its value %s.\n",
                work_key_start_environ, tmp);
        work_key_start = atoi(tmp);
    }
}

inline static void config_work_key_end() {
    char *tmp = NULL;

    tmp = getenv(work_key_end_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_work_key_end:%s doesn't exist,"
                "use default value %d.\n",
                work_key_end_environ, work_key_end);
    } else {
        fprintf(stderr, __PREFIX "config_work_key_end:%s exist,"
                "use its value %s.\n",
                work_key_end_environ, tmp);
        work_key_end = atoi(tmp);
    }
}


inline static void config_txn_size() {
    char *tmp = NULL;

    tmp = getenv(txn_size_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_txn_size:%s doesn't exist,"
                "use default value %d.\n",
                txn_size_environ, txn_size);
    } else {
        fprintf(stderr, __PREFIX "config_txn_size:%s exist,"
                "use its value %s.\n",
                txn_size_environ, tmp);
        txn_size = atoi(tmp);
    }
}

inline static void config_thread_number() {
    char *tmp =  NULL;

    tmp = getenv(thread_number_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_thread_number:%s doesn't exist,"
                "use default value %d.\n",
                thread_number_environ, thread_number);
    } else {
        fprintf(stderr, __PREFIX "config_thread_number:%s exist,"
                "use its value %s.\n",
                thread_number_environ, tmp);
        thread_number = atoi(tmp);
    }
}

inline static void config_db_file() {
    char *tmp = NULL;

    tmp = getenv(db_file_environ);
    if (tmp == NULL) {
        fprintf(stderr, __PREFIX "config_db_file:%s doesn't exist,"
                "use default value %s.\n",
                db_file_environ, db_file);
    } else {
        fprintf(stderr, __PREFIX "config_db_file:%s exist,"
                "use its value %s.\n",
                db_file_environ, tmp);
        db_file = tmp;
    }
}

inline static void config() {

    config_n_thr();
    config_n_txn_per_thr();
    config_n_key_per_txn();
    config_n_meta_keys();
    config_n_work_keys();
    config_n_tot_keys();
    config_work_key_start();
    config_work_key_end();


    config_txn_size();
    config_thread_number();
    config_db_file();
}

inline static uint64_t get_ts(){
    uint64_t ts = 0; 
    struct timeval t;
    gettimeofday(&t, 0); 
    ts = t.tv_sec * 1000000ull + t.tv_usec;

    return ts; 
}

/*
   For int64_t type:

   int64_t t;
   printf("%" PRId64 "\n", t);

   for uint64_t type:

   uint64_t t;
   printf("%" PRIu64 "\n", t);
   */
#endif
