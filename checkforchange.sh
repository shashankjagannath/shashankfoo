#!/bin/sh

if diff lastip newip >/dev/null ; then
  echo Same
else
  echo Different
  cat newip | mail -s "PI's new ip address" shashankjagannath@gmail.com
  cp newip lastip

fi
