from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404

class UserMixin(CreateView):
    model = User
    form_class = UserForm
    template_name = 'User/User.html'
    success_url = reverse_lazy('User:list')
    
class UserCreateView(UserMixin, CreateView):
    pass

class UserListView(ListView):
    model = User
    ordering = 'id'
    paginate_by = 10

class UserUpdateView(UserMixin, UpdateView):
    pass

class UserDeleteView(DeleteView):
    model = User
    template_name = 'User/User.html'
    success_url = reverse_lazy('User:list')



class UploadedImageMixin(CreateView):
    model = UploadedImage
    form_class = UploadedImageForm
    template_name = 'UploadedImage/UploadedImage.html'
    success_url = reverse_lazy('UploadedImage:list')
    
class UploadedImageCreateView(UploadedImageMixin, CreateView):
    pass

class UploadedImageListView(ListView):
    model = UploadedImage
    ordering = 'id'
    paginate_by = 10

class UploadedImageUpdateView(UploadedImageMixin, UpdateView):
    pass

class UploadedImageDeleteView(DeleteView):
    model = UploadedImage
    template_name = 'UploadedImage/UploadedImage.html'
    success_url = reverse_lazy('UploadedImage:list')



class ProcessedImageMixin(CreateView):
    model = ProcessedImage
    form_class = ProcessedImageForm
    template_name = 'ProcessedImage/ProcessedImage.html'
    success_url = reverse_lazy('ProcessedImage:list')
    
class ProcessedImageCreateView(ProcessedImageMixin, CreateView):
    pass

class ProcessedImageListView(ListView):
    model = ProcessedImage
    ordering = 'id'
    paginate_by = 10

class ProcessedImageUpdateView(ProcessedImageMixin, UpdateView):
    pass

class ProcessedImageDeleteView(DeleteView):
    model = ProcessedImage
    template_name = 'ProcessedImage/ProcessedImage.html'
    success_url = reverse_lazy('ProcessedImage:list')



class AnalysisRequestMixin(CreateView):
    model = AnalysisRequest
    form_class = AnalysisRequestForm
    template_name = 'AnalysisRequest/AnalysisRequest.html'
    success_url = reverse_lazy('AnalysisRequest:list')
    
class AnalysisRequestCreateView(AnalysisRequestMixin, CreateView):
    pass

class AnalysisRequestListView(ListView):
    model = AnalysisRequest
    ordering = 'id'
    paginate_by = 10

class AnalysisRequestUpdateView(AnalysisRequestMixin, UpdateView):
    pass

class AnalysisRequestDeleteView(DeleteView):
    model = AnalysisRequest
    template_name = 'AnalysisRequest/AnalysisRequest.html'
    success_url = reverse_lazy('AnalysisRequest:list')



class ReportMixin(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'Report/Report.html'
    success_url = reverse_lazy('Report:list')
    
class ReportCreateView(AnalysisRequestMixin, CreateView):
    pass

class ReportListView(ListView):
    model = Report
    ordering = 'id'
    paginate_by = 10

class ReportUpdateView(ReportMixin, UpdateView):
    pass

class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'Report/Report.html'
    success_url = reverse_lazy('Report:list')