#!/usr/bin/python
#
# Brave git

import os

class BraveGit:
  def add_untracked_changes(self):
    exit_code = os.system('git add . >>output.log 2>&1')
    if exit_code != 0:
      print "Failed to add untracked changes to the local Git branch, please see output.log"
      exit(exit_code)

  def diff(self):
    exit_code = os.system('git diff --cached --exit-code >>output.log 2>&1')
    if exit_code == 0:
      print "There are no untracked changes"
      exit(exit_code)

  def commit(self, message):
    exit_code = os.system('git commit -m "' + message + '" >>output.log 2>&1')
    if exit_code != 0:
      print "Failed to commit changes to the local Git branch, please see output.log"
      exit(exit_code)

  def push(self):
    exit_code = os.system('git push >>output.log 2>&1')
    if exit_code != 0:
      print "Failed to push changes to the remote Git repository, please see output.log"
      exit(exit_code)
