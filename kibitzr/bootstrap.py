import os
import stat
import logging


logger = logging.getLogger(__name__)


KIBITZR_YML = """
# Format: http://kibitzr.readthedocs.io/en/latest/configuration.html
checks:
  - name: Kibitzr release
    url: https://pypi.python.org/pypi/kibitzr/json
    transform:
      - jinja: |
          {{ json["info"]["version"] }}
      - changes: verbose
    notify:
      - python: print(content)
    period: 5
""".lstrip()


KIBITZR_CREDS_YML = """
# Plain text credentials configuration
# Documentation and other options: http://kibitzr.readthedocs.io/en/latest/credentials.html
service:
  username: john
  password: doe
""".lstrip()


def create_boilerplate():
    """
    Create kibitzr.yml and kibitzr-creds.yml in current directory
    if they do not exist.
    """
    if not os.path.exists('kibitzr.yml'):
        with open('kibitzr.yml', 'wt') as fp:
            logger.info("Saving sample check in kibitzr.yml")
            fp.write(KIBITZR_YML)
    else:
        logger.info("kibitzr.yml already exists. Skipping")
    if not os.path.exists('kibitzr-creds.yml'):
        with open('kibitzr-creds.yml', 'wt') as fp:
            logger.info("Creating kibitzr-creds.yml")
            fp.write(KIBITZR_CREDS_YML)
        os.chmod('kibitzr-creds.yml', stat.S_IRUSR | stat.S_IWUSR)
    else:
        logger.info("kibitzr-creds.yml already exists. Skipping")
