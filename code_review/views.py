from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from code_review.forms import UploadFileForm, ModifyForm
from code_review.models import File, StatusType, Log


@login_required
def get_files(request):
    files = File.objects.filter(user_id=request.user.pk).all()

    context = {
        'files': files,
        'page': 'files'
    }
    return render(request, 'code_review/list_files.html', context)


@login_required
def get_file_log(request, file_id):
    file_logs = Log.objects.filter(
        file_id=file_id,
        user_id=request.user.pk
    ).all()

    context = {
        'file_logs': file_logs,
        'page': 'files'
    }

    return render(request, 'code_review/file.html', context)


@login_required
def upload_file(request):
    form = UploadFileForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        pre_save_files = []
        # Помешаем все файлы в список чтобы
        # одним запросом их создать в базе.
        for file in form.files.getlist('files'):
            instance = File(
                name=file.name,
                status=StatusType.NEW,
                file=file,
                user_id=request.user.pk
            )
            pre_save_files.append(instance)

        # создаем все записи за один запрос
        File.objects.bulk_create(pre_save_files)

        return redirect('code_review:get_files')

    return render(request, 'code_review/upload_file.html', {'form': form})


@login_required
def modify_file(request, pk):
    form = ModifyForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        file_instance = get_object_or_404(File, pk=pk)

        data = form.cleaned_data.copy()
        data['name'] = form.cleaned_data['file'].name
        data['status'] = StatusType.MODIFIED

        for field, value in data.items():
            setattr(file_instance, field, value)

        file_instance.save()
        return redirect('code_review:get_files')

    return render(request, 'code_review/modify_file.html', {'form': form})


@login_required
def delete_file(request, pk):
    File.objects.filter(pk=pk).delete()
    return redirect('code_review:get_files')
