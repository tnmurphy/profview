#!/usr/bin/env bash
export MAKE_PROFILE_BASE


MAKE_PROFILE_BASE=test_serial
gmake-p --profile-targets -f test_serial.mk
mv $MAKE_PROFILE_BASE-*.csv $MAKE_PROFILE_BASE.csv

MAKE_PROFILE_BASE=test_2par
gmake-p --profile-targets -j2 -f test_2par.mk
mv $MAKE_PROFILE_BASE-*.csv $MAKE_PROFILE_BASE.csv

MAKE_PROFILE_BASE=test_2par_gap
gmake-p --profile-targets -j2 -f test_2par_gap.mk
mv $MAKE_PROFILE_BASE-*.csv $MAKE_PROFILE_BASE.csv
