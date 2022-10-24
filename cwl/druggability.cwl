arguments:
- position: 0
  prefix: --output-dir
  valueFrom: output
- position: 0
  prefix: --druggability-dir
  valueFrom: /pecgs-druggability/src/druggability
- position: 0
  prefix: --d
baseCommand:
- /usr/bin/python
- /pecgs-druggability/src/run_druggability.py
class: CommandLineTool
cwlVersion: v1.0
id: druggability
inputs:
- id: tumor_sample_name
  inputBinding:
    position: 1
  type: string
- id: variant_filepath
  inputBinding:
    position: 2
  type: File
- default: maf
  id: variant_file_type
  inputBinding:
    position: 3
  type: string?
- id: normal_sample_name
  inputBinding:
    position: 0
    prefix: --normal-sample-name
  type: string
- default: CHOL
  id: annotate_trials_keyword
  inputBinding:
    position: 0
    prefix: --annotate-trials-keyword
  type: string?
- default: /miniconda/envs/druggability/bin:$PATH
  id: environ_PATH
  type: string?
label: druggability
outputs:
- id: output
  outputBinding:
    glob: output/output.txt
  type: File
- id: aux_trials_output
  outputBinding:
    glob: output/aux_trials_output.txt
  type: File
requirements:
- class: DockerRequirement
  dockerPull: estorrs/pecgs-neoscan:0.0.1
- class: ResourceRequirement
  coresMin: 4
  ramMin: 28000
- class: EnvVarRequirement
  envDef:
    PATH: $(inputs.environ_PATH)
