#!/bin/sh

if diff aaa bbb >/dev/null ; then
  echo Same
else
  echo Different
fi
