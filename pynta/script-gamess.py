from pynta.main import Pynta
import sys
print(sys.prefix)

pyn = Pynta(path="/home/shikim/pynta_blodgett/production/han-qe",launchpad_path="/home/shikim/local_launchpad.yaml",
                fworker_path="/home/shikim/my_fworker.yaml",
                queue_adapter_path="/home/shikim/local_qadapter.yaml",
                rxns_file="/home/shikim/pynta_blodgett/production/han-qe/han.yaml",
                surface_type="fcc111",metal="Cu",socket=False,queue=True,njobs_queue=10,a=3.6336459335607296,
                repeats=[(1,1,1),(3,3,4)],label="han",bonding_software="gamess_us",
                software_kwargs={'kpts': (3, 3, 1), 'tprnfor': True, 'occupations': 'smearing',
                            'smearing':  'marzari-vanderbilt', 'input_dft': 'BEEF-vdW',
                            'degauss': 0.01, 'ecutwfc': 40, 'nosym': True,
                            'conv_thr': 1e-6, 'mixing_mode': 'local-TF',
                            "pseudopotentials": {"Cu": 'Cu.pbe-spn-kjpaw_psl.1.0.0.UPF',"H": 'H.pbe-kjpaw_psl.1.0.0.UPF',"O": 'O.pbe-n-kjpaw_psl.1.0.0.UPF',"C": 'C.pbe-n-kjpaw_psl.1.0.0.UPF',"N": 'N.pbe-n-kjpaw_psl.1.0.0.UPF',
                            },
                            "command": '/home/shikim/qe-7.1/bin/pw.x < PREFIX.pwi > PREFIX.pwo'},
                software_kwargs_gas={'kpts': 'gamma', 'tprnfor': True, 'occupations': 'smearing',
                            'smearing':  'gauss', 'input_dft': 'BEEF-vdW',
                            'degauss': 0.005, 'ecutwfc': 40, 'nosym': True,
                            'conv_thr': 1e-6, 'mixing_mode': 'local-TF',
                            'mixing_beta': 0.2, 'mixing_ndim': 10,
                            "pseudopotentials": {"Cu": 'Cu.pbe-spn-kjpaw_psl.1.0.0.UPF',"H": 'H.pbe-kjpaw_psl.1.0.0.UPF',"O": 'O.pbe-n-kjpaw_psl.1.0.0.UPF',"C": 'C.pbe-n-kjpaw_psl.1.0.0.UPF',"N": 'N.pbe-n-kjpaw_psl.1.0.0.UPF',
                            },
                            "command": '/home/shikim/qe-7.1/bin/pw.x < PREFIX.pwi > PREFIX.pwo'},
               TS_opt_software_kwargs={"conv_thr":1e-11}, 
               lattice_opt_software_kwargs={'kpts': (25,25,25), 'ecutwfc': 70, 'degauss':0.02, 'mixing_mode': 'plain'},
               bonding_software_kwargs={"contrl":{'scftyp':'rhf','runtyp':'energy','local':'svd','mult':'1','exetyp':'run','ispher':'1',
                                                'icharg':'0'},
                                        "guess":{'guess':'huckel'},
                                        "system":{'mwords':'300'},
                                        "basis":{'gbasis':'midi'},
                                        "scf":{'fdiff':False, 'diis':True, 'dirscf':True, 'vvo':True, 'damp':True},
                                        "local":{'orient':True},
                                        "data":{'','pynta':'bonding analysis','c1'},
                            "command": '/home/gamess/rungms -input PREFIX.inp > PREFIX.log'},
               slab_path = "/home/shikim/pynta_blodgett/production/han-qe/slab.xyz",
               )
#pyn.execute_from_initial_ad_guesses()
pyn.execute(generate_initial_ad_guesses=False,calculate_adsorbates=False,
                calculate_transition_states=True)

#pyn.generate_slab()

#modified input script for pynta: 
#include gamess keyword
#depending on the system, some keywords (e.g., mult, icharg, basis...) can be changed as users' preferences.
