.. _comparison:

===============================
Comparison to similar solutions
===============================

**Note**: this page is work in progress.

Kibitzr can be bent to user's needs to great extent.
But the common problems, that can be solved with Kibitzr, also can be solved with other products.

This page strives to provide objective comparison of existing solutions.

Kibitzr vs Huginn
-----------------

`Huginn`_ is a system for building agents that perform automated tasks for you online.

Huginn started in 2013 and have built a broad community with hundreds of contributors
and collected thousands of stars.

Huginn organises directed graphs of events passing between different types of agents.
There are more than 50 types of agents.
User builds pipelines of predefined agent types inside the browser.

Agents are written in Ruby language and are stored inside Huginn's subdirectory.

One Huginn service can serve multiple users authenticated with username and password.

For operating Huginn requires MySQL database and Nginx server.
Installation is pretty involved, but well documented.


**Kibitzr** started in 2017 and has a long way of growing user base.

It serves a flat list of checks for a single user.
All checks have fixed structure: fetch-transform-notify, and can't be combined.

There is no web service or user interface.
Instead Kibitzr stores whole configuration in one YAML file.

It has a limited set of predefined fetchers, transformers and notifiers,
but allows inserting arbitrary Python/Bash code at each step.
Also Kibitzr can be extended with Python packages.

Kibitzr doesn't use database (but requires git to store history of content changes).

Kibitzr has strong support for browser automation and web scraping.

.. _Huginn: https://github.com/huginn/huginn


Kibitzr vs Trigger Happy
------------------------

`Trigger Happy`_ is similar to Huginn, but is written as a Django app and thus can be integrated inside Django projects.

...

Kibitzr vs bip.io
-----------------

As Huginn and Trigger Happy, bip.io started in 2013.
As of 2017 the project accumulated 808 GitHub stars and 11 contributors.

bip.io is an open source RESTful JSON API.
It's an API orchestration and HTTP endpoint server.
bip.io is written in Javascript and is extendable through npm packages.

When a message is received from a web hook, incoming email or generated from a trigger,
it appears on a bips graph from the 'source' node.
The source data is then normalized into a JSON structure and
'exported' via RabbitMQ for consumption as 'imports' by adjacent nodes.
This pipeline continues until all nodes have been visited.
A node in a bip usually represents a Remote Procedure Call (RPC) on an external service,
which is a discrete 'action' provided by a 'pod'.

Operationally bip.io requires Node.js, MongoDB and RabbitMQ.

bip.io has dozens of integrations for popular services.

.. _`Trigger Happy`: https://trigger-happy.eu/
