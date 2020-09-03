#!/usr/bin/env python3

import os

from pathlib import Path

from rmgcat_to_sella.irc import IRC
from rmgcat_to_sella.io import IO

from balsam.launcher.dag import BalsamJob, add_dependency

slab = '{slab}'
repeats = {repeats}
facetpath = '{facetpath}'
pytemplate_f = '{pytemplate_f}'
pytemplate_r = '{pytemplate_r}'
yamlfile = '{yamlfile}'
ts_estimate_dir = 'TS_estimate'
pseudopotentials = {pseudopotentials}
pseudo_dir = '{pseudo_dir}'
balsam_exe_settings = {balsam_exe_settings}
calc_keywords = {calc_keywords}
workflow_name = yamlfile+facetpath+'04'
dependency_workflow_name = yamlfile+facetpath+'03'
dependent_workflow_name = yamlfile+facetpath+'05'
creation_dir = '{creation_dir}'

irc = IRC(facetpath, slab, repeats, ts_estimate_dir, yamlfile,
          pseudopotentials, pseudo_dir, balsam_exe_settings,
          calc_keywords, creation_dir)
irc.set_up_irc_all(pytemplate_f, pytemplate_r)
all_rxns = IO().get_list_all_rxns_names(yamlfile)

pending_simulations = BalsamJob.objects.filter(
    workflow__contains=dependency_workflow_name
).exclude(state="JOB_FINISHED")

pending_simulations_dep = BalsamJob.objects.filter(
    workflow__contains=dependent_workflow_name
).exclude(state="JOB_FINISHED")
cwd = Path.cwd().as_posix()

for rxn in all_rxns:
    path_to_irc = os.path.join(facetpath, rxn, 'IRC')
    for py_script in Path(path_to_irc).glob('*.py'):
        print(py_script)
        job_dir, script_name = os.path.split(str(py_script))
        job_to_add = BalsamJob(
            name=script_name,
            workflow=workflow_name,
            application='python',
            args=cwd + '/' + str(py_script),
            input_files='',
            user_workdir=job_dir,
            node_packing_count=48,
            ranks_per_node=1,
        )
        job_to_add.save()
        for job in pending_simulations:
            add_dependency(job, job_to_add)  # parent, child
        for job in pending_simulations_dep:
            add_dependency(job_to_add, job)  # parent, child
