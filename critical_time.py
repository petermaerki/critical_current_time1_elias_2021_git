import time
import pathlib

from mp import pyboard_query


DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).absolute().parent

try:
    import mp
    import mp.version
    import mp.micropythonshell
except ModuleNotFoundError as ex:
    raise Exception(f'The module "mpfshell2" is missing ({str(ex)}). Did you call "pip -r requirements.txt"?')

REQUIRED_MPFSHELL_VERSION='100.9.10'
if mp.version.FULL < REQUIRED_MPFSHELL_VERSION:
    raise Exception(f'Your "mpfshell" has version "{mp.version.FULL}" but should be higher than "{REQUIRED_MPFSHELL_VERSION}". Call "pip install --upgrade mpfshell2"!')

class CritialTime:
    def __init__(self):
        self._board = pyboard_query.ConnectPyboard(hwtype='critical_time')
        #self._board = pyboard_query.ConnectComport('COM5')

        self._board.mpfshell.sync_folder(DIRECTORY_OF_THIS_FILE / 'micropython')
        self._exec('import mp_critical_time')
        self._exec('mp_critical_time.singleton.reset()')

    def measure_button_ms(self):
        cmd = f'mp_critical_time.singleton.measure_button_ms()'
        ret = self._eval(cmd)
        time_ms = eval(ret)
        return time_ms

    def measure_times_us(self, timeout_us=5e6):
        cmd = f'mp_critical_time.singleton.measure_times_us(timeout_us={int(timeout_us)})'
        ret = self._eval(cmd)
        try:
            ZERO1_us, TRIP_us, ZERO2_us = eval(ret)
        except SyntaxError as ex:
            raise Exception(f'Micropython "{cmd}" -> "{ret}" ({ex})') from ex
        return ZERO1_us, TRIP_us, ZERO2_us

    def _eval(self, cmd):
        return self._board.mpfshell.MpFileExplorer.eval(cmd)

    def _exec(self, cmd):
        return self._board.mpfshell.MpFileExplorer.exec(cmd)

