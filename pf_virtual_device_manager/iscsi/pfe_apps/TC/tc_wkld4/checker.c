#include "tc_wkld4_config.h"

#define PREFIX  __PREFIX "cker:"
#define KEY_N_OFFSET  (3)
#define VALUE_N_OFFSET  (5)

#define MAX_KV_LEN  (20)

typedef struct record {
    char key[MAX_KV_LEN];
    char value[MAX_KV_LEN];
} Record;

typedef struct records {
    unsigned long n;
    unsigned long c;
    Record *head;
} Records;

int main(void) {
    /* var */
    TCBDB *bdb = NULL;
    BDBCUR *cur = NULL;
    int ecode = 0;
    char *key = NULL, *value = NULL;
    char keystr[W4_KEY_BUFSIZE];

    /* config */
    config();

    /* create the obj */
    bdb = tcbdbnew();

    /* open db */
    if (!tcbdbopen(bdb, db_file, BDBOREADER)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, PREFIX "main:db open error: %s\n", tcbdberrmsg(ecode));
        return EXIT_FAILURE;
    }

    ////////////////////////Read ByKey
    //read meta rows
    int thr_id = 0;
    for(thr_id = 1; thr_id <= n_thr; ++ thr_id) {
        int txn_id = 0;
        for(txn_id = 1; txn_id <= n_txn_per_thr; ++ txn_id) {
            int meta_i = (thr_id - 1) * n_txn_per_thr + txn_id;
            //key string
            memset((char*)keystr, 0, W4_KEY_BUFSIZE);
            sprintf((char*)keystr, "k-%d-meta-thr-%d-txn-%d", meta_i, thr_id, txn_id);

            //read tc 
            value = tcbdbget2(bdb, keystr);
            if (value == NULL) {
                continue;
            }

            printf("----------        ----------\n");
            printf("%s  %s\n", keystr, value);
            free(value);
        }
    }
    //read work rows
    int work_i = 0;
    for(work_i = work_key_start; work_i <= work_key_end; ++ work_i) {
        //key string
        memset((char*)keystr, 0, W4_KEY_BUFSIZE);
        sprintf((char*)keystr, "k-%d", work_i);
        //read db 
        value = tcbdbget2(bdb, keystr);
        if (value == NULL) {
            continue;
        }
        printf("----------        ----------\n");
        printf("%s  %s\n", keystr, value);
        free(value);
    }



    //////////////////// Read ByCursor
    cur = tcbdbcurnew(bdb);
    tcbdbcurfirst(cur);
    while ((key = tcbdbcurkey2(cur)) != NULL) {
        value = tcbdbcurval2(cur);

        printf("+++++++++++     +++++++++++\n");
        printf("%s  %s\n", key, value);

        free(value);
        free(key);
        tcbdbcurnext(cur);
    }
    tcbdbcurdel(cur);




    /* close db */
    if (!tcbdbclose(bdb)) {
        ecode = tcbdbecode(bdb);
        fprintf(stderr, PREFIX "close error:%s\n", tcbdberrmsg(ecode));
    }

    /* del obj */
    tcbdbdel(bdb);

    return EXIT_SUCCESS;
}
