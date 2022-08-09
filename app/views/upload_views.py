import logging
import os
import shutil
import urllib

from app import app
from flask import request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from app.config import UPLOAD_FILE_PATH, TMP_STORAGE_PATH

logger = logging.getLogger(__name__)


def read_in_chunks(file_obj, file_size, size=1024 * 1024):
    start_size = 0
    content_length = size
    while True:
        chunk = file_obj.read(size)
        end_size = start_size + size
        if end_size > file_size:
            end_size = file_size
            content_length = end_size - start_size
        content_range = f'bytes {start_size}-{end_size}/{file_size}'
        start_size += size + 1
        if not chunk:
            file_obj.close()
            break
        yield chunk, content_length, content_range


@app.route('/upload')
def upload():
    # if request.method == 'POST':
    #     ret = {
    #         'code': 200,
    #         'msg': 'ok',
    #         'data': {}
    #     }
    #     print(request.files)
    #     file_obj = request.files['file']
    #     file_save_path = os.path.join(UPLOAD_FILE_PATH, secure_filename(file_obj.filename))
    #     file_obj.save(file_save_path)  # 名称一样的文件不会覆盖，会跳过保存
    #     ret.update({
    #         'msg': '上传成功！',
    #     })
    #     return jsonify(ret)
    return render_template('upload.html')


@app.route('/upload/file', methods=['POST'])
def upload_file():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    try:
        filename = request.headers.get('File-Name')
        filename = urllib.parse.unquote(filename)
        file_save_path = os.path.join(UPLOAD_FILE_PATH, secure_filename(filename))
        # secure_filename(filename) 会把中文字符给去掉
        # 需要修改源码.\Lib\site-packages\werkzeug\utils.py 中
        # 改1：_filename_ascii_strip_re = re.compile(u"[^\u4e00-\u9fa5A-Za-z0-9_.-]")
        # 改2（这个在secure_filename方法中）：encode("ascii", "ignore") decode("ascii")中的ascii全部换成utf-8
        with open(file_save_path, mode='wb') as f:
            f.write(request.data)
        ret.update({
            'msg': 'upload success'
        })
    except Exception as e:
        ret.update({
            'msg': str(e)
        })
    finally:
        return jsonify(ret)


def empty_folder(directory):
    # 清空文件夹
    if not os.path.exists(directory):
        pass
    else:
        shutil.rmtree(directory)
        os.mkdir(directory)


def merge_file(new_filepath, *args):
    # new_filepath 新的文件路径
    # args 为文件路径序列，有序的
    for arg in args:
        try:
            with open(arg, 'rb') as rf:
                data = rf.read()
            with open(new_filepath, 'ab') as wf:
                wf.write(data)
        except Exception as e:
            logger.error(str(e))
            return False, str(e)
    return True, 'merge success'


@app.route('/upload/breakpoint/http', methods=['POST'])
def breakpoint_http():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    filename = request.headers.get('Content-Disposition').split(';')[-1].split('=')[-1]
    filename = urllib.parse.unquote(filename)
    content_index = request.headers.get('Content-Index')
    index, count = content_index.split('-')
    tmp_save_path = os.path.join(TMP_STORAGE_PATH, f"{secure_filename(filename)}_{index}")
    block_data = request.data
    with open(tmp_save_path, mode='wb') as f:
        f.write(block_data)
    if index == count:
        file_save_path = os.path.join(UPLOAD_FILE_PATH, filename)
        tmp_list = [os.path.join(TMP_STORAGE_PATH, filename) for filename in os.listdir(TMP_STORAGE_PATH)]
        res, msg = merge_file(file_save_path, *tmp_list)
        empty_folder(TMP_STORAGE_PATH)  # 合并之后清空临时存储分片的文件夹
        if res:
            ret.update({
                'data': {
                    'filepath': file_save_path
                },
            })
        else:
            ret.update({
                'msg': msg
            })
        return jsonify(ret)
    return jsonify(ret)
