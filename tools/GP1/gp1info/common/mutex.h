#ifndef MUTEX_DOT_H
#define MUTEX_DOT_H

#include <stdint.h>

#define LOCKED      1
#define UNLOCKED    0

typedef uint32_t mutex_t;

extern void unlock_mutex(void * mutex);
extern void lock_mutex(void * mutex);
extern void synchronize(void);
extern void iflush(void);

#endif
