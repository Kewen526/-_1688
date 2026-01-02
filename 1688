#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1688订单支付API - 本地测试版本
功能：
1. 获取支付链接 - 调用1688开放平台跨境宝支付API
2. 获取订单支付状态 - 调用1688开放平台订单详情API

使用方法：
    python 1688_api_local.py
"""

import time
import json
import hmac
import hashlib
import requests
import re

# ==================== API配置 ====================
# 支付链接API配置（跨境宝支付）
PAY_URL_CONFIG = {
    'app_key': '2019459',
    'secret': 'XgepZVNu5iz',
    'access_token': '1c87e807-03ff-4d1e-a08f-72746cb06c64'
}

# 订单状态API配置
ORDER_STATUS_CONFIG = {
    'app_key': '2019459',
    'secret': 'XgepZVNu5iz',
    'access_token': '1c87e807-03ff-4d1e-a08f-72746cb06c64'
}


# ==================== 辅助函数 ====================
def is_api_success(result):
    """
    判断API调用是否成功
    输入: result - API返回结果
    输出: (是否成功, 支付链接)
    """
    success_value = result.get('success')
    if success_value == True or success_value == 'true':
        pay_url = result.get('payUrl') or (
            result.get('result', {}).get('url') if isinstance(result.get('result'), dict) else None)
        return True, pay_url

    if result.get('payUrl'):
        return True, result.get('payUrl')

    if isinstance(result.get('result'), dict) and result['result'].get('url'):
        return True, result['result']['url']

    return False, None


def extract_failed_order_ids(error_msg):
    """
    从错误消息中提取失败的订单ID列表
    输入: error_msg - 错误消息字符串
    输出: 订单ID列表
    """
    match = re.search(r'\[(.*?)\]', error_msg)
    if match:
        order_ids_str = match.group(1)
        failed_ids = [order_id.strip() for order_id in order_ids_str.split(',')]
        return failed_ids
    return []


# ==================== 核心API函数 ====================
def get_order_details(order_id, config=None):
    """
    获取订单详情 - 调用1688开放平台API
    
    参数:
        order_id: 订单号
        config: API配置字典，默认使用ORDER_STATUS_CONFIG
    
    返回:
        JSON响应数据
    """
    if config is None:
        config = ORDER_STATUS_CONFIG
    
    secret = config['secret']
    access_token = config['access_token']
    app_key = config['app_key']
    
    api_url = f'https://gw.open.1688.com/openapi/param2/1/com.alibaba.trade/alibaba.trade.get.buyerView/{app_key}'
    url_path = f'param2/1/com.alibaba.trade/alibaba.trade.get.buyerView/{app_key}'
    
    print(f"[订单详情] 获取订单: {order_id}")
    
    try:
        # 请求参数
        params = {
            'webSite': '1688',
            'orderId': order_id,
            'includeFields': 'GuaranteesTerms,NativeLogistics,RateDetail,OrderInvoice',
            'attributeKeys': '[]',
            'access_token': access_token,
            '_aop_timestamp': str(int(time.time() * 1000)),
        }
        
        # 拼装参数
        sorted_params = sorted(params.items())
        query_string = ''.join(f"{k}{v}" for k, v in sorted_params)
        
        # 合并签名因子和拼装参数
        sign_string = url_path + query_string
        
        # 生成HMAC-SHA1签名
        signature = hmac.new(
            secret.encode('utf-8'), 
            sign_string.encode('utf-8'), 
            hashlib.sha1
        ).hexdigest().upper()
        params['_aop_signature'] = signature
        
        # 发送请求
        response = requests.post(api_url, data=params, timeout=10)
        result = response.json()
        
        print(f"[订单详情] 请求成功: {order_id}")
        return result
        
    except Exception as e:
        print(f"[订单详情] 请求失败: {order_id}, 错误: {str(e)}")
        return {'error': str(e), 'success': False}


def get_pay_status(order_id, config=None):
    """
    获取订单支付状态
    
    参数:
        order_id: 订单号
        config: API配置字典
    
    返回:
        支付状态描述字符串，如 "已付款"、"等待买家付款" 等
    """
    result = get_order_details(order_id, config)
    
    if result.get('success') == 'true' or result.get('success') == True:
        trade_terms = result.get('result', {}).get('tradeTerms', [])
        if trade_terms and isinstance(trade_terms, list):
            pay_status_desc = trade_terms[0].get('payStatusDesc', '')
            return pay_status_desc
    
    return None


def get_crossborder_pay_url(order_id_list, config=None):
    """
    获取跨境宝支付链接
    
    参数:
        order_id_list: 订单ID列表（最多30个）
        config: API配置字典，默认使用PAY_URL_CONFIG
    
    返回:
        API响应数据
    """
    if config is None:
        config = PAY_URL_CONFIG
    
    secret = config['secret']
    access_token = config['access_token']
    app_key = config['app_key']
    
    api_url = f'https://gw.open.1688.com/openapi/param2/1/com.alibaba.trade/alibaba.crossBorderPay.url.get/{app_key}'
    url_path = f'param2/1/com.alibaba.trade/alibaba.crossBorderPay.url.get/{app_key}'
    
    print(f"[支付链接] 获取订单列表: {order_id_list}")
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 请求参数
            params = {
                'orderIdList': json.dumps(order_id_list),
                'access_token': access_token,
                '_aop_timestamp': str(int(time.time() * 1000)),
            }
            
            # 拼装参数（按字母排序）
            sorted_params = sorted(params.items())
            query_string = ''.join(f"{k}{v}" for k, v in sorted_params)
            
            # 合并签名因子和拼装参数
            sign_string = url_path + query_string
            
            # 生成HMAC-SHA1签名
            signature = hmac.new(
                secret.encode('utf-8'),
                sign_string.encode('utf-8'),
                hashlib.sha1
            ).hexdigest().upper()
            params['_aop_signature'] = signature
            
            # 发送请求
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            response = requests.post(
                api_url, 
                data=params, 
                headers=headers, 
                timeout=15
            )
            result = response.json()
            
            print(f"[支付链接] API响应: {json.dumps(result, ensure_ascii=False)}")
            return result
            
        except Exception as e:
            retry_count += 1
            print(f"[支付链接] 请求异常 (尝试 {retry_count}/{max_retries}): {str(e)}")
            if retry_count >= max_retries:
                return {"error": str(e), "success": False}
            time.sleep(1)
    
    return {"error": "所有重试均失败", "success": False}


def get_pay_url(order_ids, config=None):
    """
    智能获取支付链接（支持部分成功重试）
    
    参数:
        order_ids: 订单ID列表（支持字符串或列表）
        config: API配置字典
    
    返回:
        包含支付链接和订单处理结果的字典
    """
    # 参数处理
    if isinstance(order_ids, str):
        order_ids = [order_ids.strip()] if order_ids.strip() else []
    elif isinstance(order_ids, list):
        order_ids = [str(oid).strip() for oid in order_ids if str(oid).strip()]
    
    if not order_ids:
        return {'success': False, 'errorMsg': '订单ID列表不能为空'}
    
    if len(order_ids) > 30:
        return {'success': False, 'errorMsg': '订单数量不能超过30个'}
    
    print(f"\n{'='*60}")
    print(f"开始获取支付链接，总订单数: {len(order_ids)}")
    print(f"{'='*60}")
    
    # 第一次调用API
    result = get_crossborder_pay_url(order_ids, config)
    
    # 情况1: 完全成功
    is_success, pay_url = is_api_success(result)
    if is_success:
        print(f"✅ 全部订单支付链接获取成功!")
        return {
            'success': True,
            'payUrl': pay_url,
            'successOrderIds': order_ids,
            'successCount': len(order_ids),
            'totalCount': len(order_ids),
            'failedCount': 0,
            'failedOrderIds': []
        }
    
    # 情况2: 有错误，尝试从错误消息中提取失败的订单
    error_msg = result.get('errorMsg', '')
    if error_msg:
        print(f"⚠️ 首次请求部分订单失败: {error_msg}")
        
        failed_order_ids = extract_failed_order_ids(error_msg)
        
        if failed_order_ids:
            print(f"🔍 识别到失败的订单ID ({len(failed_order_ids)}个): {failed_order_ids}")
            
            success_order_ids = [oid for oid in order_ids if oid not in failed_order_ids]
            print(f"✅ 成功的订单ID ({len(success_order_ids)}个): {success_order_ids}")
            
            if success_order_ids:
                print(f"🔄 使用 {len(success_order_ids)} 个有效订单重新获取支付链接...")
                
                retry_result = get_crossborder_pay_url(success_order_ids, config)
                retry_success, retry_pay_url = is_api_success(retry_result)
                
                if retry_success:
                    print(f"🎉 部分订单支付链接获取成功!")
                    return {
                        'success': True,
                        'payUrl': retry_pay_url,
                        'successOrderIds': success_order_ids,
                        'failedOrderIds': failed_order_ids,
                        'successCount': len(success_order_ids),
                        'failedCount': len(failed_order_ids),
                        'totalCount': len(order_ids),
                        'errorMsg': error_msg
                    }
                else:
                    print(f"❌ 重试仍然失败")
                    return {
                        'success': False,
                        'errorMsg': retry_result.get('errorMsg', '未知错误'),
                        'failedOrderIds': order_ids,
                        'failedCount': len(order_ids),
                        'totalCount': len(order_ids),
                        'successCount': 0,
                        'successOrderIds': []
                    }
            else:
                print(f"❌ 全部订单都无法支付!")
                return {
                    'success': False,
                    'errorMsg': error_msg,
                    'failedOrderIds': failed_order_ids,
                    'failedCount': len(failed_order_ids),
                    'totalCount': len(order_ids),
                    'successCount': 0,
                    'successOrderIds': []
                }
        else:
            return {
                'success': False,
                'errorMsg': error_msg,
                'failedOrderIds': order_ids,
                'failedCount': len(order_ids),
                'totalCount': len(order_ids),
                'successCount': 0,
                'successOrderIds': []
            }
    
    # 其他情况
    return {
        'success': False,
        'errorMsg': result.get('error', '未知错误'),
        'failedOrderIds': order_ids,
        'failedCount': len(order_ids),
        'totalCount': len(order_ids),
        'successCount': 0,
        'successOrderIds': []
    }


# ==================== 测试函数 ====================
def test_get_order_details():
    """测试获取订单详情"""
    print("\n" + "="*60)
    print("测试: 获取订单详情")
    print("="*60)
    
    order_id = "123456789"  # 替换为真实订单号
    result = get_order_details(order_id)
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


def test_get_pay_status():
    """测试获取订单支付状态"""
    print("\n" + "="*60)
    print("测试: 获取订单支付状态")
    print("="*60)
    
    order_id = "123456789"  # 替换为真实订单号
    status = get_pay_status(order_id)
    print(f"支付状态: {status}")
    return status


def test_get_pay_url():
    """测试获取支付链接"""
    print("\n" + "="*60)
    print("测试: 获取支付链接")
    print("="*60)
    
    order_ids = ["123456789", "987654321"]  # 替换为真实订单号
    result = get_pay_url(order_ids)
    print(f"\n最终结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


# ==================== 主函数 ====================
if __name__ == '__main__':
    print("="*60)
    print("1688订单支付API - 本地测试")
    print("="*60)
    print("\n可用函数:")
    print("  1. get_order_details(order_id)     - 获取订单详情")
    print("  2. get_pay_status(order_id)        - 获取支付状态")
    print("  3. get_crossborder_pay_url(ids)    - 获取跨境宝支付链接(原始)")
    print("  4. get_pay_url(order_ids)          - 智能获取支付链接(推荐)")
    print("="*60)
    
    # 运行测试 - 取消注释以运行
    # test_get_order_details()
    # test_get_pay_status()
    # test_get_pay_url()
    
    # 交互式测试示例
    print("\n示例用法:")
    print(">>> from 1688_api_local import *")
    print(">>> result = get_order_details('你的订单号')")
    print(">>> status = get_pay_status('你的订单号')")
    print(">>> pay_result = get_pay_url(['订单1', '订单2'])")
