.. _gcp:

============================
Try kibitzr on GCP Free Tier
============================

Kibitzr can be run on `f1-micro`_ instance, which is included in `GCP Free Tier`_.
Launch Ubuntu 16.04 and execute following commands:

.. code-block:: bash

	sudo apt -qqy update
	sudo apt -y install curl firefox=45.0.2+build1-0ubuntu1 libcanberra-gtk*
	sudo apt -y install git jq xvfb
	sudo apt -y install python-lazy-object-proxy python-lxml python-pip python-yaml
	sudo pip install kibitzr 'selenium<3'

Define a simple check:

.. code-block:: bash
    
    cat >kibitzr.yml <<EOF
    checks:
      - name: Kibitzr GitHub release
        url: https://api.github.com/repos/kibitzr/kibitzr/releases/latest
        transform:
          - jq: .tag_name + " " + .name
          - changes: verbose
        notify:
          - python: print(text)
    EOF

Run kibitzr:

.. code-block:: bash

    kibitzr

.. _f1-micro: https://cloud.google.com/compute/docs/machine-types#sharedcore
.. _`GCP Free Tier`: https://cloud.google.com/free/
