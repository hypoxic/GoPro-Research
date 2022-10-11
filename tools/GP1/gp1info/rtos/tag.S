.global _tag
.extern _start
.extern patch_dest
.extern overwrite_loc

#define __ASSEMBLY__
#include "readsec.h"

    .text
_tag:
.string "HYPOXIC"
.word   patch_dest
.word   patch_dest_size
.word   _start
.word   overwrite_loc

    .end

