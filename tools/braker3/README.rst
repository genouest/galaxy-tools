Braker3
=======

This tool is not in IUC because of the license issues with GeneMark and
ProtHint that makes it impossible to test it using CI.

GeneMark and ProtHint
---------------------

Braker requires GeneMark to predict gene, but due to licensing issues, we
are not allowed to distribute GeneMark automatically.

Braker also requires ProtHint to use protein sequences as hints to predict
genes, but, again, due to licensing issues, we are not allowed to distribute
ProtHint automatically.

To use Braker3, the Galaxy administrator needs to install
GeneMark, and set the ``GENEMARK_PATH`` variable on the job destination.

The only working version of GeneMark to install needs to be downloaded from
http://topaz.gatech.edu/GeneMark/etp.for_braker.tar.gz
This archive also contains ProtHint and various other tools in specific versions needed by Braker3.

Unzip it, and set the ``GENEMARK_PATH`` variable to point to the extracted ``bin``
directory.

Also set the ``PROTHINT_PATH`` variable on the job destination, pointing to the extracted
``bin/gmes/ProtHint/bin/`` directory

Running tests
-------------

Tests require working GeneMark and ProtHint installations, which means
both GENEMARK_PATH and PROTHINT_PATH are set in job_conf_braker3.xml.

You should then use the ``--job_config_file job_conf_braker3.xml``
option for planemo commands.

You should also copy a valid GeneMark license (from
http://topaz.gatech.edu/GeneMark/license_download.cgi) in
test-data/gm_key_64.
