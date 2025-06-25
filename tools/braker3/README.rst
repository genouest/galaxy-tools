Braker3
=======

This wrapper runs BRAKER3 using the official Docker image: ``teambraker/braker3:v3.0.7.5``.

It no longer requires a custom installation of GeneMark or ProtHint on the host system, as these are bundled inside the container.

Docker container
----------------

BRAKER3 depends on GeneMark and ProtHint for gene prediction from RNA-Seq and protein evidence.
Due to licensing issues, these tools cannot be redistributed directly, but the official BRAKER3 Docker image includes the required versions.

The wrapper uses this image via the Galaxy `<container type="docker">` mechanism:

.. code-block:: xml

    <container type="docker">teambraker/braker3:v3.0.7.5</container>

Running
-------

To run this tool during development, use Planemo with Docker support enabled:

.. code-block:: bash

    planemo serve --docker
    planemo test --docker

There is no longer any need to manually set ``GENEMARK_PATH`` or ``PROTHINT_PATH`` via the job configuration.

License
-------

A valid GeneMark license is still required **inside the container**, but the official Docker image ships with compatible versions and is prepared accordingly by the authors.

Testing
-------

Tests no longer rely on custom environment variables. Docker ensures a reproducible and portable environment for development and execution.

``job_conf_braker3.xml`` is now obsolete for this wrapper version.