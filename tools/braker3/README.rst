Braker3
=======

This wrapper runs BRAKER3 using the official Docker image: ``teambraker/braker3``.

It does not require any longer a custom installation of GeneMark on the host system, as these are bundled inside the container.

Docker container
----------------

BRAKER3 depends on GeneMark for gene prediction from RNA-Seq and protein evidence.
Due to licensing issues, these tools could not be redistributed directly, but the official BRAKER3 Docker image includes the required versions.

The wrapper uses this image via the Galaxy `<container type="docker">` mechanism:

.. code-block:: xml

    <container type="docker">teambraker/braker3:v3.0.7.6</container>

2025.07.01: The licensing issue seems to be gone (https://github.com/Gaius-Augustus/BRAKER/issues/629), but using Conda packages is broken at the moment,
and not supported by the authors of Braker (https://github.com/Gaius-Augustus/BRAKER/commit/ece9e0f28ea2634b5abbfd0b7cf0a6be5f1bf8db).

Running
-------

To run this tool during development, use Planemo with Docker support enabled:

.. code-block:: bash

    planemo serve --docker
    planemo test --docker

There is no longer any need to manually set ``GENEMARK_PATH`` or ``PROTHINT_PATH`` via the job configuration.

Testing
-------

Tests no longer rely on custom environment variables. Docker ensures a reproducible and portable environment for development and execution.

``job_conf_braker3.xml`` is now obsolete for this wrapper version.
