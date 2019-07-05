#include "tc_wkld4_config.h"

#define PREFIX __PREFIX "wker:"

int main(void) {
    TCBDB *bdb = NULL;
    int ecode = 0;

    /* config */
    config();

    /* PFE_LOG_DIR */
    char *log_dir = getenv(PFE_LOG_DIR);
    FILE *cmfp = NULL;
    if (log_dir == NULL) {
        fprintf(stderr, PREFIX "main:%s doesn't exist:"
                "commit timestamps won't be printed\n",
                PFE_LOG_DIR);
        log_dir = NULL;
    } else {
        char cm_tm_file[LONG_PATH];
        sprintf((char*)cm_tm_file, "%s/%s",
                log_dir, COMMIT_TM_FILE);
        if ((cmfp = fopen(cm_tm_file, "w")) == NULL) {
            fprintf(stderr, PREFIX "main:%s open failed:"
                    "commit timestamps won't be printed\n",
                    cm_tm_file);
            cmfp = NULL;
        }
    }

    /* create the object */
    bdb = tcbdbnew();

    /* open db */
    if (!tcbdbopen(bdb, db_file, BDBOWRITER | BDBOCREAT)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, PREFIX "main:open error:%s\n", 
                tcbdberrmsg(ecode));
    }

    //char keystr[BUF_SIZE], valstr[BUF_SIZE];

    char keystr[W4_KEY_BUFSIZE];
    char valstr[W4_VAL_BUFSIZE];
    ////////////////////////// A Transaction
    tcbdbtranbegin(bdb);

    /*int i = 0;
    for (i = 1; i <= txn_size; i++) {
        memset(keystr, 0, BUF_SIZE);
        memset(valstr, 0, BUF_SIZE);
        sprintf(keystr, "%s%d", KEYPRE, i);
        sprintf(valstr, "%s%d", VALPRE, i);
        tcbdbput2(bdb, keystr, valstr);
    }*/

    //init meta rows
    int thr_id = 0;
    for(thr_id = 1; thr_id <= n_thr; ++ thr_id) {
        int txn_id = 0;
        for(txn_id = 1; txn_id <= n_txn_per_thr; ++ txn_id) {
            int meta_i = (thr_id - 1) * n_txn_per_thr + txn_id;
            memset(keystr, 0, W4_KEY_BUFSIZE);
            memset(valstr, 0, W4_VAL_BUFSIZE);

            sprintf((char*)keystr, "k-%d-meta-thr-%d-txn-%d", meta_i, thr_id, txn_id);
            sprintf((char*)valstr, "v-%d", meta_i);

            tcbdbput2(bdb, keystr, valstr);

        }
    }

    //init work rows
    int work_i = 0;
    for(work_i = work_key_start; work_i <= work_key_end; ++ work_i) {
        memset(keystr, 0, W4_KEY_BUFSIZE);
        memset(valstr, 0, W4_VAL_BUFSIZE);

        sprintf((char*)keystr, "k-%d", work_i);
        sprintf((char*)valstr, "v-%d", work_i);

        tcbdbput2(bdb, keystr, valstr);
    }



    //commit txn
    tcbdbtrancommit(bdb);
    /////////////////////////////////


    /* close the db */
    if (!tcbdbclose(bdb)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, PREFIX "main:close error:%s\n",
                tcbdberrmsg(ecode));
    }

    /* del the obj */
    tcbdbdel(bdb);

    return 0;
}
