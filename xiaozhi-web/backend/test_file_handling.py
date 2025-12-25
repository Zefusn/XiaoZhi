#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件处理功能
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import allowed_file, read_excel_with_python_libs

def test_allowed_file():
    """测试文件扩展名验证功能"""
    print("测试文件扩展名验证功能...")
    
    test_cases = [
        ("test.xlsx", True),
        ("test.xls", True),
        ("test.xlsm", True),
        ("test.xltx", True),
        ("test.xltm", True),
        ("test.csv", False),
        ("test.txt", False),
        ("test", False),  # 没有扩展名
        ("test.XLSX", True),  # 大写扩展名
        ("test.XLS", True),   # 大写扩展名
    ]
    
    for filename, expected in test_cases:
        result = allowed_file(filename)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {filename}: {result} (期望: {expected})")
    
    print()

def test_file_extension_detection():
    """测试文件扩展名检测功能"""
    print("测试文件扩展名检测功能...")
    
    import os
    test_cases = [
        ("test.xlsx", ".xlsx"),
        ("test.xls", ".xls"),
        ("test.xlsm", ".xlsm"),
        ("test.xltx", ".xltx"),
        ("test.xltm", ".xltm"),
        ("test", ""),  # 没有扩展名
        ("test.csv", ".csv"),
    ]
    
    for filename, expected_ext in test_cases:
        actual_ext = os.path.splitext(filename)[1].lower()
        expected_ext = expected_ext.lower()
        status = "✓" if actual_ext == expected_ext else "✗"
        print(f"  {status} {filename}: '{actual_ext}' (期望: '{expected_ext}')")
    
    print()

if __name__ == "__main__":
    print("文件处理功能测试")
    print("=" * 50)
    
    test_allowed_file()
    test_file_extension_detection()
    
    print("测试完成！")