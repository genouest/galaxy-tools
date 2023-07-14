# Braker

This tool is not in IUC because of the license issues with GeneMark and ProtHint that makes it impossible to test it using CI.

## GeneMark

Braker can use GeneMark to predict gene, but due to licensing issues, we are not allowed to distribute GeneMark automatically.

If you want to use it, the Galaxy administrator needs to install GeneMark, and set the `GENEMARK_PATH` variable on the job destination.

## ProtHint

Braker can use ProtHint to use protein sequences as hints to predict genes, but due to licensing issues, we are not allowed to distribute ProtHint automatically.

If you want to use it, the Galaxy administrator needs to install ProtHint, and set the `PROTHINT_PATH` variable on the job destination.

## Running tests

Tests require working GeneMark and ProtHint installations, which means both GENEMARK_PATH and PROTHINT_PATH are set in job_conf_braker3.xml.

You should then use the `--job_config_file job_conf_braker3.xml` option for planemo commands.

You should also copy a valid GeneMark license (from http://topaz.gatech.edu/GeneMark/license_download.cgi) in test-data/gm_key_64.
