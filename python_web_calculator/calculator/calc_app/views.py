from django.shortcuts import render
# 上面这个导包引入render函数是为了页面渲染

# 下面是写完前端网页添加的内容
# 引入子进程模块，执行发送过来的计算公式
import subprocess

from django.views.decorators.http import require_POST

# 用于将计算的结果封装成JSON
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


# 首页
def home(request):
    return render(request, 'index.html')


# 公式计算函数
def run_code(code):
    try:
        code = 'print(' + code + ')'
        # 公式计算
        output = subprocess.check_output(['python', '-c', code], universal_newlines=True,
                                         stderr=subprocess.STDOUT, timeout=30)
    except subprocess.CalledProcessError as e:
        output = '公式输出有误'
    return output


@csrf_exempt  # 规避csrf校验（防止网站被跨站攻击）
@require_POST  # 引入装饰器获取后台服务器的POST请求权限
# 视图处理函数
def compute(request):
    code = request.POST.get('code')  # 获取计算公式
    result = run_code(code)
    return JsonResponse(data={'result': result})  # 封装成JSON
