#!/bin/bash

if [ -z $WORKSPACE_ROOT ]; then
  echo "Variable WORKSPACE_ROOT not set, make sure the workspace is set up properly!"
  exit
fi

echo "Installing CHRISLab Flexible Manipulation demonstration software setup for Kinova Robot ARM ..."

cd $WORKSPACE_ROOT

# List the rosinstall files containing any packages we wish to install here
wstool merge -t . src/chris_kinova_flexible_manipulation/install/chris_kinova_flexible_manipulation.rosinstall

#--------------------- common code below here ----------------------------
# Optionally check if update is requested. Not doing update saves some
# time when called from other scripts
while [ -n "$1" ]; do
  case $1 in
  --no_ws_update)
      UPDATE_WORKSPACE=1
      ;;
  esac

  shift
done

if [ -n "$UPDATE_WORKSPACE" ]; then
  echo "Not updating workspace as --no_ws_update was set"
else
  wstool update -t .
  rosdep update --include-eol-distros
  rosdep install -r --from-path . --ignore-src
fi
