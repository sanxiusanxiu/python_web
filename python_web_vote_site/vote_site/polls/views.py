from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Choice, Question

from django.urls import reverse
from django.views import generic

from django.utils import timezone


# # 编写第一个视图，如果想看见视图的效果，需要在 polls/urls.py 下将一个 URL 映射到该视图
# def index(request):
#     return HttpResponse("你好。你现在正在 polls 应用的首页。")

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # 改进 get_queryset() 方法，
    # 将 pub_data 属性与 timezone.now() 相比较来判断是否应该显示此 Question
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


# 使用两个通用视图： ListView 和 DetailView
# 这两个视图分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    # 就算在发布日期时未来的那些投票不会在目录页 index 里出现，但是如果用户知道或者猜到正确的 URL ，还是可以访问到它们
    # 所以在 DetailView 里增加一些约束
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




# # def index(request):
# #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
# #     template = loader.get_template('polls/index.html')
# #     context = {
# #         'latest_question_list': latest_question_list,
# #     }
# #     return HttpResponse(template.render(context, request))
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
#
# # # 如果指定问题ID所对应的问题不存在，就抛出一个 Http404 异常
# # def detail(request, question_id):
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist")
# #     return render(request, 'polls/detail.html', {'question': question})
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
