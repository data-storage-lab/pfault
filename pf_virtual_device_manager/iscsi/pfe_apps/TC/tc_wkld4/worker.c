#include "tc_wkld4_config.h"

#define PREFIX  __PREFIX "wker:"

void *writer_thread(void*);

struct child {
    int tid;
    TCBDB *bdb;
    FILE *cmfp;
};

int main(void) {
    int i = 0, ecode;
    TCBDB *bdb = NULL;

    /* config */
    config();

    bdb = tcbdbnew();
    tcbdbsetmutex(bdb);
    if (!tcbdbopen(bdb, db_file, BDBOWRITER | BDBOCREAT | BDBOTSYNC)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, PREFIX "main:db open error: %s\n", tcbdberrmsg(ecode));
    }

    pthread_t *pts = NULL;
    struct child *chs = NULL;
    FILE **cmfps = NULL;

    pts = (pthread_t*)malloc(sizeof(pthread_t) * (thread_number + 1));
    chs = (struct child*)malloc(sizeof(struct child) * (thread_number + 1));
    cmfps = (FILE**)malloc(sizeof(FILE*) * (thread_number + 1));

    if (pts == NULL 
            || chs == NULL
            || cmfps == NULL) {
        fprintf(stderr, PREFIX "main:mm alloc error\n");
        return EXIT_FAILURE;
    }

    memset(pts, 0, sizeof(pthread_t) * (thread_number + 1));
    memset(chs, 0, sizeof(struct child) * (thread_number + 1));
    memset(cmfps, 0, sizeof(FILE*) * (thread_number + 1));

    for (i = 1; i <= thread_number; i++) {
        chs[i].bdb = bdb;
        chs[i].tid = i;
    }

    char *log_dir = getenv(PFE_LOG_DIR);
    if (log_dir == NULL) {
        fprintf(stderr, PREFIX "main:%s doesn't exist:"
                "all threads' commit timestamps won't be printed\n",
                PFE_LOG_DIR);
        log_dir = NULL;
    } else {
        char cm_tm_file[LONG_PATH];
        for (i = 1; i <= thread_number; i++) {
            /* the file name of cm_tm file */
            sprintf((char*)cm_tm_file, "%s/%d_%s", log_dir, i, COMMIT_TM_FILE);
            if ((cmfps[i] = fopen(cm_tm_file, "w")) == NULL) {
                fprintf(stderr, PREFIX "main:%s open failed:"
                        "commit timestamps won't be printed:%d\n",
                        cm_tm_file, i);
                cmfps[i] = NULL;
            } else {
                chs[i].cmfp = cmfps[i];
            }
        }
    }

    /* thread run */
    for (i = 1; i <= thread_number; i++) {
        pthread_create(&pts[i], NULL, writer_thread, (void*)(chs + i));
    }

    /* thread join */
    for (i = 1; i <= thread_number; i++) {
        pthread_join(pts[i], NULL);
    }

    /* close cm_tm files */
    for (i = 1; i <= thread_number; i++) {
        if (cmfps[i])
            fclose(cmfps[i]);
    }

    /* close db */
    if (!tcbdbclose(bdb)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, "db close error: %s\n", tcbdberrmsg(ecode));
    }

    /* delete db obj */
    tcbdbdel(bdb);

    return EXIT_SUCCESS;
}


/* Would like a semi-open interval [min, max) */
int random_in_range (unsigned int min, unsigned int max)
{
    //srand(time(NULL));
    int base_random = rand(); /* in [0, RAND_MAX] */
    if (RAND_MAX == base_random) 
        return random_in_range(min, max);
    /* now guaranteed to be in [0, RAND_MAX) */
    int range       = max - min,
        remainder   = RAND_MAX % range,
        bucket      = RAND_MAX / range;
    /* There are range buckets, plus one smaller interval
     *      within remainder of RAND_MAX */
    if (base_random < RAND_MAX - remainder) {
        return min + base_random/bucket;
    } else {
        return random_in_range (min, max);
    }
}

void *writer_thread(void *arg) {
    struct child *c = (struct child*)arg;
    int tid = c->tid;
    int pivot = (c->tid - 1) * txn_size;
    FILE *cmfp = c->cmfp;
    TCBDB *bdb = c->bdb;
    int r = 0, ecode = 0;

    //char keystr[BUF_SIZE], valstr[BUF_SIZE];
    char keystr[W4_KEY_BUFSIZE];
    char valstr[W4_VAL_BUFSIZE];

    if (DEBUG_MODE) {
        printf("tid = %d, pivot = %d\n", tid, pivot);
    }


    //iterate n txns
    int txn_id = 0;
    for (txn_id = 1; txn_id <= n_txn_per_thr; ++ txn_id) {

        /////////////////////////// begin a txn
        if ((r = tcbdbtranbegin(bdb)) == false) {
            ecode = tcbdbecode(bdb);
            fprintf(stderr, PREFIX "writer_thread:%d:"
                    "txn begin error:%s\n", tid,
                    tcbdberrmsg(ecode));
        }

        //store all ks in this txn
        char all_ks_buf[W4_VAL_BUFSIZE - 24] = "";
        
        //put n_key_per_txn ks
        int k_i = 0;
        for(k_i = 1; k_i <= n_key_per_txn; ++ k_i) {
            int r_min = work_key_start;
            int r_max = work_key_end;
            srand(time(NULL)%10000000 + tid*n_txn_per_thr*n_key_per_txn + txn_id*n_key_per_txn + k_i);
            int rand_k = random_in_range(r_min, r_max+1);


            memset((char*)keystr, 0, W4_KEY_BUFSIZE);
            memset((char*)valstr, 0, W4_VAL_BUFSIZE);
            //key string
            sprintf(keystr, "k-%d", rand_k);
            //value string
            sprintf(valstr, "v-%d-thr-%d-txn-%d-k-%d", rand_k, tid, txn_id, rand_k);

            //concat this k to all ks string for meta row
            char tmp_k_buf[10] = "";//max single k str should be <= 10 digits (including '-' and '\0')
            sprintf(tmp_k_buf, "%d-", rand_k);
            strcat(all_ks_buf, tmp_k_buf);

            tcbdbput2(bdb, keystr, valstr);
        }//end of putting n_keys_per_txn ks

        //put meta row
        uint64_t txn_meta_ts = get_ts(); 
        char tmp_ts_buf[20];
        sprintf(tmp_ts_buf, "%"PRIu64"", txn_meta_ts);
        int meta_i = (tid - 1) * n_txn_per_thr + txn_id;

        char meta_keystr_buf[W4_KEY_BUFSIZE] = "";
        char meta_valstr_buf[W4_VAL_BUFSIZE] = "";
        memset((char*)meta_keystr_buf, 0, W4_KEY_BUFSIZE);
        memset((char*)meta_valstr_buf, 0, W4_VAL_BUFSIZE);
        //key string
        sprintf(meta_keystr_buf, "k-%d-meta-thr-%d-txn-%d", meta_i, tid, txn_id);
        //value string
        sprintf(meta_valstr_buf, "v-%d-meta-thr-%d-txn-%d-k-", meta_i, tid, txn_id);

        strcat(meta_valstr_buf, all_ks_buf);
        strcat(meta_valstr_buf, "ts-");
        strcat(meta_valstr_buf, tmp_ts_buf);

        //put into tc
        tcbdbput2(bdb, meta_keystr_buf, meta_valstr_buf);


        /* before_cm_tm */
        /*if (cmfp) {
            uint64_t before_cm_tm = get_ts();
            fprintf(cmfp, "%" PRIu64 "\n", before_cm_tm);
            fflush(cmfp);
        }*/

        uint64_t before_cm_tm = get_ts();
        fflush(stdout);
        printf("k-%d-meta-thr-%d-txn-%d     %" PRIu64 "     beforecommit \n", meta_i, tid, txn_id, before_cm_tm);
        fflush(stdout);

        if ((r = tcbdbtrancommit(bdb)) == false) {
            ecode = tcbdbecode(bdb);
            fprintf(stderr, PREFIX "writer_thread:%d:txn commit error:%s\n",
                    tid, tcbdberrmsg(ecode));
            if ((r = tcbdbtranabort(bdb)) == false) {
                ecode = tcbdbecode(bdb);
                fprintf(stderr, PREFIX "writer_thread:%d:txn abort error: %s\n",
                        tid, tcbdberrmsg(ecode));
            }
        }

        /* after_cm_tm */
        uint64_t after_cm_tm = get_ts();
        fflush(stdout);
        printf("k-%d-meta-thr-%d-txn-%d     %" PRIu64 "\n", meta_i, tid, txn_id, after_cm_tm);
        fflush(stdout);
        ///////////////////////// end of a txn
    }

    return (void*)EXIT_SUCCESS;
}
