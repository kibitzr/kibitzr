============================
Try kibitzr on AWS Free Tier
============================

Kibitzr can be run on `t2.micro`_ instance, which is included in `AWS Free Tier`_.
Launch Amazon Linux AMI and execute following commands:

.. code-block:: bash

    sudo yum update -y
    sudo yum install -y docker
    sudo service docker start

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

Run kibitzr inside docker container:

.. code-block:: bash

    sudo docker run --rm -v $PWD:/root/.config/kibitzr -v $PWD/pages:/pages peterdemin/kibitzr

.. _t2.micro: https://aws.amazon.com/ec2/instance-types/
.. _`AWS Free Tier`: https://aws.amazon.com/free
