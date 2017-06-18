import time, json, subprocess
from urllib import request
from celery import Celery


app = Celery('worker', broker='amqp://admin:mypass@rabbit:5672')
# url_root = 'http://proxy/api/task/'
url_root = 'http://dispatcher_backend/task/'


@app.task(bind=True, name='subprocess')
def subprocess_run(self, script: str):
    def update_status(status: str, return_code: int=None, stdout: str=None, stderr: str=None):
        url = url_root + self.request.id
        payload = {
            'status': status,
            'return_code': return_code,
            'stdout': stdout,
            'stderr': stderr
        }
        req = request.Request(url, headers={'content-type': 'application/json'},
                              data=json.dumps(payload).encode('utf-8'))
        with request.urlopen(req) as response:
            pass
            # code = response.getcode()
            # charset = response.headers.get_content_charset('utf-8')
            # body = json.loads(response.read().decode(charset))
            # print('{}, {}'.format(code, body))
            # TODO: retry if a POST failed (code != 200)
    
    def decode_bin_stream(bin) -> str:
        return bin.decode('utf-8') if bin is not None else None

    update_status('STARTED')
    process = subprocess.run(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = process.returncode
    stdout = decode_bin_stream(process.stdout)
    stderr = decode_bin_stream(process.stderr)
    update_status('FINISHED', return_code, stdout, stderr)


# @app.task(bind=True, name='mwoffliner')
# def mwoffliner(self, config: dict):
#     def update_status(status:str, command: str=None, returncode: int=None, stdout: str=None, stderr: str=None, error: str=None):
#         url = 'http://proxy/api/task/' + self.request.id
#         payload = {
#             'status': status,
#             'command': command,
#             'returncode': returncode,
#             'stdout': stdout,
#             'stderr': stderr,
#             'error': error
#         }
#         req = request.Request(url,
#                               headers={'content-type': 'application/json'},
#                               data=json.dumps(payload).encode('utf-8'))
#         with request.urlopen(req) as response:
#             code = response.getcode()
#             charset = response.headers.get_content_charset('utf-8')
#             body = json.loads(response.read().decode(charset))
#             # print('{}, {}'.format(code, body))
#             # TODO: retry if a POST failed (code != 200)
#
#     def decode_bin_stream(bin) -> str:
#         return bin.decode('utf-8') if bin is not None else None
#
#     def assemble_command(config: dict) -> [str]:
#         whitelist = ['mwUrl', 'adminEmail', 'verbose']
#         command = ['mwoffliner']
#         for key, value in config.items():
#             if key not in whitelist:
#                 raise MWOfflinerConfigKeyError(key)
#             command.append("--{}={}".format(key, value))
#         return command
#
#     command_str = None
#     returncode = None
#
#     try:
#         update_status(status='STARTED')
#
#         command = assemble_command(config)
#         command_str = ' '.join(command)
#
#         process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         returncode = process.returncode
#         stdout = decode_bin_stream(process.stdout)
#         stderr = decode_bin_stream(process.stderr)
#
#         process.check_returncode()
#         update_status(status='UPLOADING', command=command_str, returncode=returncode, stdout=stdout, stderr=stderr)
#         time.sleep(5)
#         update_status(status='SUCCESS', command=command_str, returncode=returncode, stdout=stdout, stderr=stderr)
#
#     except MWOfflinerConfigKeyError as error:
#         update_status(status='ERROR', error=error.message)
#     except subprocess.CalledProcessError as error:
#         update_status(status='ERROR', command=command_str, returncode=error.returncode,
#                       stdout=decode_bin_stream(error.stdout),
#                       stderr=decode_bin_stream(error.stderr))
#     except:
#         message = "Unexpected error: {}".format(sys.exc_info()[0])
#         update_status(status='ERROR', command=command_str, returncode=returncode, error=message)
#
#
# class MWOfflinerConfigKeyError(Exception):
#     def __init__(self, key: str):
#         self.message = 'The flag "{}" for mwoffliner is not supported.'.format(key)
#
#
# class MWOfflinerUploadError(Exception):
#     def __init__(self):
#         pass