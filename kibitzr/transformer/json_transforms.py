import json
import logging

from .utils import wrap_dummy, bake_parametrized


logger = logging.getLogger(__name__)


def pretty_json(text):
    json_dump = json.dumps(
        json.loads(text),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        # encoding='utf-8',
    )
    return True, u'\n'.join([
        line.rstrip()
        for line in json_dump.splitlines()
    ])


def run_jq(query, text):
    from kibitzr.compat import sh
    jq = sh.Command("jq").bake('--monochrome-output', '--raw-output')
    logger.debug("Running jq query %s against %s", query, text)
    try:
        command = jq(query, _in=text)
        if not command.stderr:
            success, result = True, command.stdout.decode('utf-8')
        else:
            success, result = False, command.stderr.decode('utf-8')
    except sh.ErrorReturnCode as exc:
        logger.exception("jq failure")
        success, result = False, exc.stderr
    logger.debug("jq transform success: %r, content: %r",
                 success, result)
    return success, result


def register():
    return {
        'json': wrap_dummy(pretty_json),
        'jq': bake_parametrized(run_jq),
    }
