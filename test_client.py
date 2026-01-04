#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1688订单支付API - 客户端测试
"""

import requests
import json

# ==================== 配置 ====================
SERVER_URL = "http://47.104.72.198:8000"

# 测试订单号
TEST_ORDER_ID = "4987103580454334805"


def test_pay_status(order_id):
    """测试获取支付状态"""
    url = f"{SERVER_URL}/api/pay-status/{order_id}"
    print(f"\n{'=' * 60}")
    print(f"💰 测试: 获取支付状态 - 订单号: {order_id}")
    print(f"{'=' * 60}")
    print(f"[请求] GET {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"\n[响应] HTTP状态码: {response.status_code}")
        print(f"[响应] 原始文本: {response.text}")

        result = response.json()
        print(f"\n[解析后的JSON结果]:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        if result.get('success'):
            print(f"\n✅ 订单状态: {result.get('pay_status')}")
        else:
            print(f"\n❌ 获取失败: {result.get('error_msg')}")

    except Exception as e:
        print(f"\n❌ 请求异常: {str(e)}")


if __name__ == '__main__':
    print("=" * 60)
    print("1688订单支付API - 客户端测试")
    print("=" * 60)

    test_pay_status(TEST_ORDER_ID)

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
