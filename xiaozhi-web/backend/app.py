from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from werkzeug.utils import secure_filename
import json
import sys
import csv
from io import StringIO
import time
from pathlib import Path

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 全局数据存储
data_store = {
    'page1_data': None,
    'page2_data': None,
    'conn': None
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}


def cleanup_old_files():
    """清理超过1小时的旧文件"""
    uploads_path = Path(UPLOAD_FOLDER)
    current_time = time.time()
    for file_path in uploads_path.iterdir():
        if file_path.is_file():
            # 检查文件修改时间
            if current_time - file_path.stat().st_mtime > 3600:  # 1小时
                try:
                    file_path.unlink()
                except OSError:
                    pass  # 如果文件被占用，跳过删除


def read_excel_with_python_libs(filepath):
    """使用 openpyxl 读取 Excel 文件"""
    from openpyxl import load_workbook
    
    wb = None
    try:
        # 使用只读模式确保文件被正确处理
        wb = load_workbook(filepath, read_only=True)
        ws = wb.active
        
        # 读取所有数据
        data = []
        headers = []
        
        for row_idx, row in enumerate(ws.iter_rows(values_only=True)):
            if row_idx == 0:
                # 第一行作为列名
                headers = [str(cell) if cell is not None else f'Column_{i}' for i, cell in enumerate(row)]
            else:
                # 数据行
                data.append({headers[i]: (cell if cell is not None else '') for i, cell in enumerate(row)})
        
        return data, headers
    finally:
        # 确保工作簿被关闭
        if wb is not None:
            try:
                wb.close()
            except:
                pass


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Excel 数据分析接口"""
    try:
        # 清理旧文件
        cleanup_old_files()
        
        # 获取上传的文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 读取 Excel 文件
        data, headers = read_excel_with_python_libs(filepath)
        
        # 获取参数
        device_ids = request.form.get('deviceIds', '')
        data_types = json.loads(request.form.get('dataTypes', '[]'))
        platform = request.form.get('platform', '安卓')
        
        # 处理设备ID过滤
        device_id_list = [id.strip() for id in device_ids.split(',')] if device_ids else []
        
        # 根据平台过滤
        if platform == '安卓':
            pkg_name = 'com.helloxj.xlook'
        else:
            pkg_name = 'cs.zero.waterCamera'
        
        # 初始数据
        initial_data = [row for row in data if 'pkgName' in row and row['pkgName'] == pkg_name]
        
        # 用户数据（过滤设备ID）
        if device_id_list:
            user_data = [row for row in data 
                        if 'pkgName' in row and row['pkgName'] == pkg_name and 
                        'deviceId' in row and row['deviceId'] not in device_id_list]
        else:
            user_data = [row for row in data if 'pkgName' in row and row['pkgName'] == pkg_name]
        
        # 统计数据
        # 初始数据统计
        initial_device_ids = set()
        initial_directives_count = 0
        initial_helpful_count = 0
        initial_unhelpful_count = 0
        
        for row in initial_data:
            if 'deviceId' in row and row['deviceId']:
                initial_device_ids.add(row['deviceId'])
            if 'directives' in row and row['directives'] is not None and str(row['directives']).strip() != '':
                initial_directives_count += 1
            if 'avail' in row and row['avail'] == '有帮助':
                initial_helpful_count += 1
            elif 'avail' in row and row['avail'] == '无帮助':
                initial_unhelpful_count += 1
        
        # 用户数据统计
        user_device_ids = set()
        user_directives_count = 0
        user_helpful_count = 0
        user_unhelpful_count = 0
        
        for row in user_data:
            if 'deviceId' in row and row['deviceId']:
                user_device_ids.add(row['deviceId'])
            if 'directives' in row and row['directives'] is not None and str(row['directives']).strip() != '':
                user_directives_count += 1
            if 'avail' in row and row['avail'] == '有帮助':
                user_helpful_count += 1
            elif 'avail' in row and row['avail'] == '无帮助':
                user_unhelpful_count += 1
        
        initial_stats = {
            '总数据量': len(initial_data),
            '使用人数': len(initial_device_ids),
            '给出指令次数': initial_directives_count,
            '有帮助次数': initial_helpful_count,
            '无帮助次数': initial_unhelpful_count
        }
        
        user_stats = {
            '总数据量': len(user_data),
            '使用人数': len(user_device_ids),
            '给出指令次数': user_directives_count,
            '有帮助次数': user_helpful_count,
            '无帮助次数': user_unhelpful_count
        }
        
        # 构造返回结果
        results = []
        for key in initial_stats.keys():
            results.append({
                'metric': f'{platform} - {key}',
                'initialData': initial_stats[key] if 'initial' in data_types else '',
                'userData': user_stats[key] if 'user' in data_types else ''
            })
        
        # 存储数据到内存数据库供 SQL 查询使用
        data_store['page1_data'] = user_data
        if data_store['conn']:
            data_store['conn'].close()
        data_store['conn'] = sqlite3.connect(':memory:', check_same_thread=False)
        
        # 创建表并插入数据
        cursor = data_store['conn'].cursor()
        
        # 创建表结构（基于数据的列）
        if user_data:
            columns = list(user_data[0].keys())
            # 生成 SQL 创建语句
            create_sql = f"CREATE TABLE data ({', '.join([f'{col} TEXT' for col in columns])})"
            cursor.execute(create_sql)
            
            # 插入数据
            for row in user_data:
                placeholders = ','.join(['?' for _ in columns])
                values = [str(row.get(col, '')) for col in columns]
                cursor.execute(f"INSERT INTO data VALUES ({placeholders})", values)
        
        data_store['conn'].commit()
        
        # 删除上传的文件
        try:
            os.remove(filepath)
        except OSError:
            # 如果文件被占用，跳过删除（后续会被覆盖）
            pass

        return jsonify({'data': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/label-process', methods=['POST'])
def label_process():
    """小志标签处理接口"""
    try:
        # 清理旧文件
        cleanup_old_files()
        
        # 获取上传的文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 读取 Excel 文件
        data, headers = read_excel_with_python_libs(filepath)
        
        # 检查必需字段
        required_columns = ['question', 'pkgName', 'deviceId']
        if not all(col in headers for col in required_columns):
            return jsonify({'error': f'Excel 文件中缺少必需字段: {", ".join(required_columns)}'}), 400
        
        # 获取参数
        device_ids = request.form.get('deviceIds', '')
        platform = request.form.get('platform', '安卓')
        analysis_type = request.form.get('analysisType', 'default')
        
        # 处理设备ID过滤
        device_id_list = [id.strip() for id in device_ids.split(',')] if device_ids else []
        
        # 根据平台过滤
        if platform == '安卓':
            pkg_name = 'com.helloxj.xlook'
        else:
            pkg_name = 'cs.zero.waterCamera'
        
        # 过滤数据
        if device_id_list:
            filtered_data = [row for row in data 
                            if 'pkgName' in row and row['pkgName'] == pkg_name and 
                            'deviceId' in row and row['deviceId'] not in device_id_list]
        else:
            filtered_data = [row for row in data if 'pkgName' in row and row['pkgName'] == pkg_name]
        
        # 统计问题/标签出现次数
        question_counts = {}
        for row in filtered_data:
            if 'question' in row and row['question']:
                question = str(row['question'])
                question_counts[question] = question_counts.get(question, 0) + 1
        
        # 根据分析类型过滤
        if analysis_type == 'lowVolume':
            # 过滤低量标签（小于10）
            question_counts = {k: v for k, v in question_counts.items() if v < 10}
        
        # 转换为前端需要的格式
        results = [{'label': label, 'count': count} for label, count in question_counts.items()]
        
        # 按数量排序
        results.sort(key=lambda x: x['count'], reverse=True)
        
        # 存储数据到内存数据库供 SQL 查询使用
        data_store['page2_data'] = filtered_data
        if data_store['conn']:
            data_store['conn'].close()
        data_store['conn'] = sqlite3.connect(':memory:', check_same_thread=False)
        
        # 创建表并插入数据
        cursor = data_store['conn'].cursor()
        
        # 创建表结构（基于数据的列）
        if filtered_data:
            columns = list(filtered_data[0].keys())
            # 生成 SQL 创建语句
            create_sql = f"CREATE TABLE data ({', '.join([f'{col} TEXT' for col in columns])})"
            cursor.execute(create_sql)
            
            # 插入数据
            for row in filtered_data:
                placeholders = ','.join(['?' for _ in columns])
                values = [str(row.get(col, '')) for col in columns]
                cursor.execute(f"INSERT INTO data VALUES ({placeholders})", values)
        
        data_store['conn'].commit()
        
        # 删除上传的文件
        try:
            os.remove(filepath)
        except OSError:
            # 如果文件被占用，跳过删除（后续会被覆盖）
            pass
        
        return jsonify({'data': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sql-query', methods=['POST'])
def sql_query():
    """SQL 查询接口"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'SQL 查询语句不能为空'}), 400
        
        if not data_store['conn']:
            return jsonify({'error': '没有可用的数据，请先加载数据'}), 400
        
        # 执行 SQL 查询
        cursor = data_store['conn'].cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # 获取列名
        column_names = [description[0] for description in cursor.description]
        
        # 转换为字典列表
        results = [dict(zip(column_names, row)) for row in rows]
        
        return jsonify({'data': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
