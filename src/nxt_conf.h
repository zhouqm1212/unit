
/*
 * Copyright (C) Igor Sysoev
 * Copyright (C) Valentin V. Bartenev
 * Copyright (C) NGINX, Inc.
 */

#ifndef _NXT_CONF_INCLUDED_
#define _NXT_CONF_INCLUDED_


typedef struct nxt_conf_json_value_s  nxt_conf_json_value_t;
typedef struct nxt_conf_json_op_s     nxt_conf_json_op_t;


typedef struct {
    nxt_uint_t  level;
    nxt_bool_t  more_space;  /* 1 bit. */
} nxt_conf_json_pretty_t;


nxt_conf_json_value_t *nxt_conf_json_get_value(nxt_conf_json_value_t *value,
    nxt_str_t *path);
nxt_conf_json_value_t *nxt_conf_json_object_get_member(
    nxt_conf_json_value_t *value, nxt_str_t *name, uint32_t *index);

nxt_int_t nxt_conf_json_op_compile(nxt_conf_json_value_t *object,
    nxt_conf_json_value_t *value, nxt_conf_json_op_t **ops, nxt_str_t *path,
    nxt_mem_pool_t *pool);
nxt_conf_json_value_t *nxt_conf_json_clone_value(nxt_conf_json_value_t *value,
    nxt_conf_json_op_t *op, nxt_mem_pool_t *pool);

nxt_conf_json_value_t *nxt_conf_json_parse(u_char *pos, size_t length,
    nxt_mem_pool_t *pool);

uintptr_t nxt_conf_json_print_value(u_char *pos, nxt_conf_json_value_t *value,
    nxt_conf_json_pretty_t *pretty);


#endif /* _NXT_CONF_INCLUDED_ */