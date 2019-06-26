from django.http import HttpResponse

from query import request_repair
from django.shortcuts import render

from django.http.response import JsonResponse
import json
import time


def query(request):
    if request.method == 'GET':
        try:
            imei = request.GET.get('imei')
            if imei:
                start_time = time.time()
                query_data = request_repair.main(imei)
                if query_data == "snError":
                    return HttpResponse("SN Error")
                elif enumerate(query_data, dict):
                    magic_time = time.time() - start_time
                    if magic_time < 5:
                        time.sleep(5 - magic_time)
                    json_ = {
                        "status": "success",
                        # "imei":imei,
                        "msg": query_data
                    }
                    return HttpResponse(
                        json.dumps(json_, ensure_ascii=False),
                        content_type="application/json;charset=utf-8")
                else:
                    return HttpResponse("403 error")
            else:
                return HttpResponse("您的输入不合法，请重新输入")
        except Exception as exc:
            print("The error is {}. Open query html now.".format(exc))
            return render(request, "query/query_data.html")
