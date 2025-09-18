from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from indexApp.models import *
from dashboard.models import Admin
from django.contrib import messages
from django.utils.text import slugify

############ start related image module ##########
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import RelatedImageFormSet


def camping_banners(request):
    camping_banner = CampingBanner.objects.last()
    all_camping_banners = CampingBanner.objects.all()
    return render(request, 'dashboard/camping_banner/view_camping_banners.html', {
        'camping_banner': camping_banner,
        'all_camping_banners': all_camping_banners
    })

def add_camping_banners(request):
    if request.method == 'POST':
        form = CampingBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Camping Banner added successfully.')
            return redirect('camping_banners')
    else:
        form = CampingBannerForm()
    return render(request, 'dashboard/camping_banner/add_camping_banner.html', {'form': form})

def delete_camping_banner(request, id):
    banner = get_object_or_404(CampingBanner, id=id)
    banner.delete()
    messages.success(request, 'Camping Banner deleted successfully.')
    return redirect('camping_banners')



def sister_concerns_banners(request):
    sister_concerns_banner = SisterConcernBanner.objects.last()
    all_sister_concerns_banners = SisterConcernBanner.objects.all()

    return render(request, 'dashboard/sister_concerns/view_sister_concerns_banners.html', {
        'sister_concerns_banner': sister_concerns_banner,
        'all_sister_concerns_banners': all_sister_concerns_banners
    })

def add_sister_concerns_banners(request):
    if request.method == 'POST':
        form = SisterConcernBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sister Concerns Banner added successfully.')
            return redirect('sister_concerns_banners')
    else:
        form = SisterConcernBannerForm()
    return render(request, 'dashboard/sister_concerns/sister_concerns_banner_add.html', {'form': form})



def delete_sister_concerns_banner(request, id):
    banner = get_object_or_404(SisterConcernBanner, id=id)
    banner.delete()
    messages.success(request, 'Sister Concerns Banner deleted successfully.')
    return redirect('sister_concerns_banners')





def dashboard(request):
    if request.user.is_authenticated:
        property_count = PropertyPost.objects.count()
        feedback_q  = FeedBack.objects.filter(is_feedback_show=True).order_by('-id')
        job_query = JobApplication.objects.all()
        contact = ContactUs.objects.all()
        context = {
            'property_count':property_count,
            'feedback':feedback_q,
            'job_query':job_query,
            'contact':contact,
        }
        return render(request,'dashboard/index.html',context)
    else:
        return redirect('auth_login')



# Admin Profile
def admin_profile_add(request):
    form = AdminForm()
    if request.method=='POST':
        form = AdminForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('admin_profile_view')
        else:
            form = AdminForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/admin/admin_profile_add.html',{'form':form})
    return render(request,'dashboard/admin/admin_profile_add.html',{'form':form})


def admin_profile_edit(request,id):
    query = get_object_or_404(Admin, id=id)
    form = AdminForm(instance =query)
    if request.method=='POST':
        form = AdminForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('admin_profile_view')
        else:
            form = AdminForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/admin/admin_profile_edit.html',{'form':form})
    return render(request,'dashboard/admin/admin_profile_edit.html',{'form':form})


def admin_profile_view(request):
    query = Admin.objects.all()
    return render(request,'dashboard/admin/admin_profile_view.html',{'query':query})


def admin_profile_delete(request,id):
    admin_delete =  Admin.objects.filter(id=id)
    admin_delete.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('admin_profile_view')


# Feedback
def feedback_view(request):
    feedback_view  = FeedBack.objects.all()
    context ={
        'feedback_view':feedback_view,
    }
    return render(request,'dashboard/feedback/feedback_view.html',context)

def feedback_edit(request,id):
    query = get_object_or_404(FeedBack, id=id)
    form = FeedBackForm(instance =query)
    if request.method=='POST':

        form = FeedBackForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
        else:
            form = FeedBackForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/feedback/feedback_edit.html',{'form':form})
    return render(request,'dashboard/feedback/feedback_edit.html',{'form':form,'query':query,})


def feedback_approved(request,id):
    query = get_object_or_404(FeedBack, id=id)
    query.is_feedback_show = True
    query.save()
    messages.success(request,'Successfully Approved')
    return redirect('feedback_view')

def feedback_delete(request,id):
    feedBack_delete =  FeedBack.objects.filter(id=id)
    feedBack_delete.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('feedback_view')




############ start related image inlineformset functionality ##########

class PropertyPostList(ListView):
    model = PropertyPost
    template_name='dashboard/Postprofile/profile_list.html'


class PropertyPostCreate(CreateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'


class PropertyPostRelatedImageCreate(CreateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyPostRelatedImageCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES)
        else:
            data['relatedimages'] = RelatedImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()

            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
                messages.success(self.request,'Upload Successfully')
        return super(PropertyPostRelatedImageCreate, self).form_valid(form)


class PropertyPostUpdate(UpdateView):
    model = PropertyPost
    success_url = '/'
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'


class PropertyPostRelatedImageUpdate(UpdateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/property_edit.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyPostRelatedImageUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES, instance=self.object)
        else:
            data['relatedimages'] = RelatedImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()
            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
                messages.success(self.request,'Update Successfully')
        return super(PropertyPostRelatedImageUpdate, self).form_valid(form)



class PropertyDetailsView(UpdateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/property-details-view.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyDetailsView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES, instance=self.object)
        else:
            data['relatedimages'] = RelatedImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()
            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
        return super(PropertyDetailsView, self).form_valid(form)




# class PropertyPostDelete(DeleteView):
#     model = PropertyPost
#     success_url = reverse_lazy('PropertyPost-list')



def property_delete(request,id):
    property_views = get_object_or_404(PropertyPost, id=id)
    property_views.delete()
    messages.success(request,'Delete Successfully')
    return redirect('PropertyPost-list')


############ end related image inlineformset functionality ##########


# why choose us
def why_choose_us_add(request):
    form = WhyChooseUsForm()
    if request.method=='POST':
        form = WhyChooseUsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('why_choose_us_view')
        else:
            form = WhyChooseUsForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/why_choose_us/why_choose_us_add.html',{'form':form})
    return render(request,'dashboard/why_choose_us/why_choose_us_add.html',{'form':form})

def why_choose_us_view(request):
    query = Why_chosse_us.objects.all()
    return render(request,'dashboard/why_choose_us/why_choose_us_view.html',{'query':query})

def why_choose_us_edit(request,id):
    query = get_object_or_404(Why_chosse_us, id=id)
    form = WhyChooseUsForm(instance =query)
    if request.method=='POST':

        form = WhyChooseUsForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('why_choose_us_view')
        else:
            form = WhyChooseUsForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/why_choose_us/why_choose_us_edit.html',{'form':form})

    return render(request,'dashboard/why_choose_us/why_choose_us_edit.html',{'form':form})

def why_choose_us_delete(request,id):
    query = get_object_or_404(Why_chosse_us, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('why_choose_us_view')



# Faq functionality
def faq_add(request):
    form = FaqForm()
    if request.method=='POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('faq_view')
        else:
            form = FaqForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/faq/faq_add.html',{'form':form})
    return render(request,'dashboard/faq/faq_add.html',{'form':form})

def faq_view(request):
    query = Faq.objects.all()
    return render(request,'dashboard/faq/faq_view.html',{'query':query})

def faq_edit(request,id):
    query = get_object_or_404(Faq, id=id)
    form = FaqForm(instance =query)
    if request.method=='POST':

        form = FaqForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('faq_view')
        else:
            form = FaqForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/faq/faq_edit.html',{'form':form})

    return render(request,'dashboard/faq/faq_edit.html',{'form':form})

def faq_delete(request,id):
    query = get_object_or_404(Faq, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('faq_view')


# Counter functionality
def counter_add(request):
    form = CountersForm()
    if request.method=='POST':
        form = CountersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('counter_view')
        else:
            form = FaqForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/counter/counter_add.html',{'form':form})
    return render(request,'dashboard/counter/counter_add.html',{'form':form})

def counter_view(request):
    query = Counters.objects.all()
    return render(request,'dashboard/counter/counter_view.html',{'query':query})

def counter_edit(request,id):
    query = get_object_or_404(Counters, id=id)
    form = CountersForm(instance =query)
    if request.method=='POST':

        form = CountersForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('counter_view')
        else:
            form = CountersForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/counter/counter_edit.html',{'form':form})

    return render(request,'dashboard/counter/counter_edit.html',{'form':form})

def counter_delete(request,id):
    query = get_object_or_404(Counters, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('counter_view')


# Blog functionality
def blog_add(request):
    form = BlogForm()
    if request.method=='POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('blog_view')
        else:
            form = BlogForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/blog/blog_add.html',{'form':form})
    return render(request,'dashboard/blog/blog_add.html',{'form':form})

def blog_view(request):
    query = Blog.objects.all()
    return render(request,'dashboard/blog/blog_view.html',{'query':query})

def blog_edit(request,id):
    query = get_object_or_404(Blog, id=id)
    form = BlogForm(instance =query)
    if request.method=='POST':

        form = BlogForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('blog_view')
        else:
            form = BlogForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/blog/blog_edit.html',{'form':form})

    return render(request,'dashboard/blog/blog_edit.html',{'form':form})

def blog_delete(request,id):
    query = get_object_or_404(Blog, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('blog_view')


# Service functionality
def service_add(request):
    form = ServicePostForm()
    if request.method=='POST':
        form = ServicePostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('service_view')
        else:
            form = ServicePostForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/service/service_add.html',{'form':form})
    return render(request,'dashboard/service/service_add.html',{'form':form})

def service_view(request):
    query = ServicePost.objects.all()
    return render(request,'dashboard/service/service_view.html',{'query':query})

def service_edit(request,id):
    query = get_object_or_404(ServicePost, id=id)
    form = ServicePostForm(instance =query)
    if request.method=='POST':

        form = ServicePostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('service_view')
        else:
            form = ServicePostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/service/service_edit.html',{'form':form})

    return render(request,'dashboard/service/service_edit.html',{'form':form})

def service_delete(request,id):
    query = get_object_or_404(ServicePost, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('service_view')


# Gallery functionality
def gallery_add(request):
    form = GalleryPostForm()
    if request.method=='POST':
        form = GalleryPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_add.html',{'form':form})
    return render(request,'dashboard/gallery/gallery_add.html',{'form':form})

def gallery_view(request):
    query = Gallery.objects.all()
    return render(request,'dashboard/gallery/gallery_view.html',{'query':query})

def gallery_edit(request,id):
    query = get_object_or_404(Gallery, id=id)
    form = GalleryPostForm(instance =query)
    if request.method=='POST':

        form = GalleryPostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_edit.html',{'form':form})

    return render(request,'dashboard/gallery/gallery_edit.html',{'form':form})

def gallery_delete(request,id):
    query = get_object_or_404(Gallery, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('gallery_view')

# Gallery functionality
def gallery_add(request):
    form = GalleryPostForm()
    if request.method=='POST':
        form = GalleryPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_add.html',{'form':form})
    return render(request,'dashboard/gallery/gallery_add.html',{'form':form})

def gallery_view(request):
    query = Gallery.objects.all()
    return render(request,'dashboard/gallery/gallery_view.html',{'query':query})

def gallery_edit(request,id):
    query = get_object_or_404(Gallery, id=id)
    form = GalleryPostForm(instance =query)
    if request.method=='POST':

        form = GalleryPostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_edit.html',{'form':form})

    return render(request,'dashboard/gallery/gallery_edit.html',{'form':form})

def gallery_delete(request,id):
    query = get_object_or_404(Gallery, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('gallery_view')

# Gallery functionality
def gallery_add(request):
    form = GalleryPostForm()
    if request.method=='POST':
        form = GalleryPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_add.html',{'form':form})
    return render(request,'dashboard/gallery/gallery_add.html',{'form':form})

def gallery_view(request):
    query = Gallery.objects.all()
    return render(request,'dashboard/gallery/gallery_view.html',{'query':query})

def gallery_edit(request,id):
    query = get_object_or_404(Gallery, id=id)
    form = GalleryPostForm(instance =query)
    if request.method=='POST':

        form = GalleryPostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/gallery/gallery_edit.html',{'form':form})

    return render(request,'dashboard/gallery/gallery_edit.html',{'form':form})

def gallery_delete(request,id):
    query = get_object_or_404(Gallery, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('gallery_view')

# Album functionality
def album_add(request):
    form = AlbumPostForm()
    if request.method=='POST':
        form = AlbumPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('album_view')
        else:
            form = AlbumPostForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/album/add.html',{'form':form})
    return render(request,'dashboard/album/add.html',{'form':form})

def album_view(request):
    query = Album.objects.all()
    return render(request,'dashboard/album/view.html',{'query':query})

def album_edit(request,id):
    query = get_object_or_404(Album, id=id)
    form = AlbumPostForm(instance =query)
    if request.method=='POST':

        form = AlbumPostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('album_view')
        else:
            form = AlbumPostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/album/edit.html',{'form':form})

    return render(request,'dashboard/album/edit.html',{'form':form})

def album_delete(request,id):
    query = get_object_or_404(Album, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('album_view')


# get in touch functionality
# Career
def career_add(request):
    form = CareerForm()
    if request.method=='POST':
        form = CareerForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            #assign the current slug and user to the post
            # new_post.title = request.user
            new_post.slug = slugify(new_post.title)
            #save post to database
            new_post.save()
            messages.success(request,'Successfully Submit')
            return redirect('career_view')
        else:
            form = CareerForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/career/career_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/career/career_add.html',{'form':form})

def career_view(request):
    query = Career.objects.all()
    return render(request,'dashboard/get_in_touch/career/career_view.html',{'query':query})

def career_edit(request,id):
    query = get_object_or_404(Career, id=id)
    form = CareerForm(instance =query)
    if request.method=='POST':

        form = CareerForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('career_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/career/career_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/career/career_edit.html',{'form':form})

def career_delete(request,id):
    query = get_object_or_404(Career, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('career_view')



# Job Application 
def job_application_view(request):
    query = JobApplication.objects.all()
    return render(request,'dashboard/get_in_touch/job-application/job_application_view.html',{'query':query})


def job_application_edit(request,id):
    query = get_object_or_404(JobApplication, id=id)
    form = JobApplicationForm(instance=query)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
        else:
            form = JobApplicationForm(request.POST)
            return render(request, 'dashboard/get_in_touch/job-application/job_application_edit.html',{'form':form})
    return render(request,'dashboard/get_in_touch/job-application/job_application_edit.html',{'form':form,'query':query})


def  job_application_delete(request,id):
    query = get_object_or_404(JobApplication, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('job_application_view')
    


# Our team functionality
def team_add(request):
    form = OurTeamForm()
    if request.method=='POST':
        form = OurTeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('team_view')
        else:
            form = OurTeamForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/team/team_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/team/team_add.html',{'form':form})

def team_view(request):
    query = OurTeam.objects.all()
    return render(request,'dashboard/get_in_touch/team/team_view.html',{'query':query})

def team_edit(request,id):
    query = get_object_or_404(OurTeam, id=id)
    form = OurTeamForm(instance =query)
    if request.method=='POST':

        form = OurTeamForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('team_view')
        else:
            form = OurTeamForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/team/team_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/team/team_edit.html',{'form':form})

def team_delete(request,id):
    query = get_object_or_404(OurTeam, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('team_view')


# Notice functionality
def notice_add(request):
    form = NoticeForm()
    if request.method=='POST':
        form = NoticeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('notice_view')
        else:
            form = NoticeForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/notice/notice_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/notice/notice_add.html',{'form':form})

def notice_view(request):
    query = Notice.objects.all()
    return render(request,'dashboard/get_in_touch/notice/notice_view.html',{'query':query})

def notice_edit(request,id):
    query = get_object_or_404(Notice, id=id)
    form = NoticeForm(instance =query)
    if request.method=='POST':

        form = NoticeForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('notice_view')
        else:
            form = NoticeForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/notice/notice_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/notice/notice_edit.html',{'form':form})

def notice_delete(request,id):
    query = get_object_or_404(Notice, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('notice_view')

# contact funtionality
def contact_view(request):
    query = ContactUs.objects.all()
    context ={
        'query':query,
    }
    return render(request,'dashboard/get_in_touch/contact/contact_view.html',context)

def contact_update(request,id):
    query = get_object_or_404(ContactUs, id=id)
    form = ContactForm(instance=query)
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
        else:
            form = ContactForm(request.POST)
            return render(request, 'dashboard/get_in_touch/contact/contact_update.html',{'form':form})
    return render(request,'dashboard/get_in_touch/contact/contact_update.html',{'form':form,'query':query})

def contact_delete(request,id):
    query = get_object_or_404(ContactUs, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('contact_view')


# About Area
def about_head_add(request):
    form = AboutHeadForm()
    if request.method=='POST':
        form = AboutHeadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_head_view')
        else:
            form = AboutHeadForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_head_section/about_head_add.html',{'form':form})
    return render(request,'dashboard/about/about_head_section/about_head_add.html',{'form':form})

def about_head_view(request):
    query = AboutUs.objects.all()
    return render(request,'dashboard/about/about_head_section/about_head_view.html',{'query':query})

def about_head_edit(request,id):
    query = get_object_or_404(AboutUs, id=id)
    form = AboutHeadForm(instance =query)
    if request.method=='POST':

        form = AboutHeadForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_head_view')
        else:
            form = AboutHeadForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_head_section/about_head_edit.html',{'form':form})

    return render(request,'dashboard/about/about_head_section/about_head_edit.html',{'form':form})

def about_head_delete(request,id):
    query = get_object_or_404(AboutUs, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_head_view')

# about looking section
def about_looking_add(request):
    form = AboutLookingSectionForm()
    if request.method=='POST':
        form = AboutLookingSectionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_looking_view')
        else:
            form = AboutHeadForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_looking_section/about_looking_add.html',{'form':form})
    return render(request,'dashboard/about/about_looking_section/about_looking_add.html',{'form':form})

def about_looking_view(request):
    query = AboutLookingSection.objects.all()
    return render(request,'dashboard/about/about_looking_section/about_looking_view.html',{'query':query})

def about_looking_edit(request,id):
    query = get_object_or_404(AboutLookingSection, id=id)
    form = AboutLookingSectionForm(instance =query)
    if request.method=='POST':

        form = AboutLookingSectionForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_looking_view')
        else:
            form = AboutLookingSectionForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_looking_section/about_looking_edit.html',{'form':form})

    return render(request,'dashboard/about/about_looking_section/about_looking_edit.html',{'form':form})

def about_looking_delete(request,id):
    query = get_object_or_404(AboutLookingSection, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_looking_view')

# about testimonial section
def about_testimonial_add(request):
    form = AboutTestimotialForm()
    if request.method=='POST':
        form = AboutTestimotialForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_testimonial_view')
        else:
            form = AboutTestimotialForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_testimonial_section/about_testimonial_add.html',{'form':form})
    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_add.html',{'form':form})

def about_testimonial_view(request):
    query = AboutTestimotial.objects.all()
    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_view.html',{'query':query})

def about_testimonial_edit(request,id):
    query = get_object_or_404(AboutTestimotial, id=id)
    form = AboutTestimotialForm(instance =query)
    if request.method=='POST':

        form = AboutTestimotialForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_testimonial_view')
        else:
            form = AboutTestimotialForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/about/about_testimonial_section/about_testimonial_edit.html',{'form':form})

    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_edit.html',{'form':form})

def about_testimonial_delete(request,id):
    query = get_object_or_404(AboutTestimotial, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_testimonial_view')


# Project type section
def project_type_add(request):
    form = ProjectTypeFilterForm()
    if request.method=='POST':
        form = ProjectTypeFilterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('project_type_view')
        else:
            form = ProjectTypeFilterForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/project_type/project_type_add.html',{'form':form})
    return render(request,'dashboard/project_type/project_type_add.html',{'form':form})

def project_type_view(request):
    query = ProjectTypeFilter.objects.all()
    return render(request,'dashboard/project_type/project_type_view.html',{'query':query})

def project_type_edit(request,id):
    query = get_object_or_404(ProjectTypeFilter, id=id)
    form = ProjectTypeFilterForm(instance =query)
    if request.method=='POST':

        form = ProjectTypeFilterForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('project_type_view')
        else:
            form = ProjectTypeFilterForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/project_type/project_type_edit.html',{'form':form})

    return render(request,'dashboard/project_type/project_type_edit.html',{'form':form})

def project_type_delete(request,id):
    query = get_object_or_404(ProjectTypeFilter, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('project_type_view')


# Property type section
def property_type_add(request):
    form = PropertyTypeFilterForm()
    if request.method=='POST':
        form = PropertyTypeFilterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('property_type_view')
        else:
            form = PropertyTypeFilterForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/property_type/property_type_add.html',{'form':form})
    return render(request,'dashboard/property_type/property_type_add.html',{'form':form})

def property_type_view(request):
    query = PropertyTypeFilter.objects.all()
    return render(request,'dashboard/property_type/property_type_view.html',{'query':query})

def property_type_edit(request,id):
    query = get_object_or_404(PropertyTypeFilter, id=id)
    form = PropertyTypeFilterForm(instance =query)
    if request.method=='POST':

        form = PropertyTypeFilterForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('property_type_view')
        else:
            form = PropertyTypeFilterForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/property_type/property_type_edit.html',{'form':form})

    return render(request,'dashboard/property_type/property_type_edit.html',{'form':form})

def property_type_delete(request,id):
    query = get_object_or_404(PropertyTypeFilter, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('property_type_view')


# Division section
def division_add(request):
    form = DivisionForm()
    if request.method=='POST':
        form = DivisionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('division_view')
        else:
            form = DivisionForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/division/division_add.html',{'form':form})
    return render(request,'dashboard/division/division_add.html',{'form':form})

def division_view(request):
    query = Division.objects.all()
    return render(request,'dashboard/division/division_view.html',{'query':query})

def division_edit(request,id):
    query = get_object_or_404(Division, id=id)
    form = DivisionForm(instance =query)
    if request.method=='POST':

        form = DivisionForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('division_view')
        else:
            form = DivisionForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/division/division_edit.html',{'form':form})

    return render(request,'dashboard/division/division_edit.html',{'form':form})

def division_delete(request,id):
    query =get_object_or_404(Division, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('division_view')


# District section
def district_add(request):
    form = DistrictForm()
    if request.method=='POST':
        form = DistrictForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('district_view')
        else:
            form = DistrictForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/district/district_add.html',{'form':form})
    return render(request,'dashboard/district/district_add.html',{'form':form})

def district_view(request):
    query = District.objects.all()
    return render(request,'dashboard/district/district_view.html',{'query':query})

def district_edit(request,id):
    query = get_object_or_404(District, id=id)
    form = DistrictForm(instance =query)
    if request.method=='POST':

        form = DistrictForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('district_view')
        else:
            form = DistrictForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/district/district_edit.html',{'form':form})

    return render(request,'dashboard/district/district_edit.html',{'form':form})

def district_delete(request,id):
    query =get_object_or_404(District, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('district_view')


# subdistrict section
def subdistrict_add(request):
    form = SubDistrictForm()
    if request.method=='POST':
        form = SubDistrictForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('subdistrict_view')
        else:
            form = DistrictForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/subdistrict/subdistrict_add.html',{'form':form})
    return render(request,'dashboard/subdistrict/subdistrict_add.html',{'form':form})

def subdistrict_view(request):
    query = SubDistrict.objects.all()
    return render(request,'dashboard/subdistrict/subdistrict_view.html',{'query':query})

def subdistrict_edit(request,id):
    query = get_object_or_404(SubDistrict, id=id)
    form = SubDistrictForm(instance =query)
    if request.method=='POST':

        form = SubDistrictForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('subdistrict_view')
        else:
            form = SubDistrictForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/subdistrict/subdistrict_edit.html',{'form':form})

    return render(request,'dashboard/subdistrict/subdistrict_edit.html',{'form':form})

def subdistrict_delete(request,id):
    query =get_object_or_404(SubDistrict, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('subdistrict_view')



# property location section
def property_location_add(request):
    form = LocationForm()
    if request.method=='POST':
        form = LocationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('property_location_view')
        else:
            form = LocationForm(request.POST)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/property_location/property_location_add.html',{'form':form})
    return render(request,'dashboard/property_location/property_location_add.html',{'form':form})

def property_location_view(request):
    query = Location.objects.all()
    return render(request,'dashboard/property_location/property_location_view.html',{'query':query})

def property_location_edit(request,id):
    query = get_object_or_404(Location, id=id)
    form = LocationForm(instance =query)
    if request.method=='POST':

        form = LocationForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('property_location_view')
        else:
            form = LocationForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/property_location/property_location_edit.html',{'form':form})

    return render(request,'dashboard/property_location/property_location_edit.html',{'form':form})

def property_location_delete(request,id):
    query =get_object_or_404(Location, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('property_location_view')



# booking now
def booking_view(request):
    query = BookingNow.objects.all()
    return render(request,'dashboard/booking_now/booking_view.html',{'query':query})
    
def booking_details(request,id):
    query = get_object_or_404(BookingNow, id=id)
    query.read_status = True
    query.save()
    return render(request,'dashboard/booking_now/booking_details.html',{'query':query})
    
def booking_delete(request,id):
    query = get_object_or_404(BookingNow, id=id)
    query.delete()
    return redirect('booking_view')



# social media link
def social_link_add(request):
    form = SocialMediaLinkForm()
    if request.method=='POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('social_link_view')
        else:
            form = SocialMediaLinkForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/social_link/social_link_add.html',{'form':form})
    return render(request,'dashboard/social_link/social_link_add.html',{'form':form})

def social_link_view(request):
    query = SocialMediaLink.objects.all().order_by('-id')
    return render(request,'dashboard/social_link/social_link_view.html',{'query':query})

def social_link_edit(request,id):
    query = get_object_or_404(SocialMediaLink, id=id)
    form = SocialMediaLinkForm(instance =query)
    if request.method=='POST':

        form = SocialMediaLinkForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('social_link_view')
        else:
            form = SocialMediaLinkForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/social_link/social_link_edit.html',{'form':form})

    return render(request,'dashboard/social_link/social_link_edit.html',{'form':form})

def social_link_delete(request,id):
    query = get_object_or_404(SocialMediaLink, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('social_link_view')



# banner video section
def banner_video_add(request):
    form = BannerForm()
    if request.method=='POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('banner_video_view')
        else:
            form = BannerForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/banner_video/banner_add.html',{'form':form})
    return render(request,'dashboard/banner_video/banner_add.html',{'form':form})

def banner_video_view(request):
    query = Banner.objects.all().order_by('-id')
    return render(request,'dashboard/banner_video/banner_view.html',{'query':query})

def banner_video_edit(request,id):
    query = get_object_or_404(Banner, id=id)
    form = BannerForm(instance =query)
    if request.method=='POST':

        form = BannerForm(request.POST,request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('banner_video_view')
        else:
            form = BannerForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/banner_video/banner_edit.html',{'form':form})

    return render(request,'dashboard/banner_video/banner_edit.html',{'form':form})

def banner_video_delete(request,id):
    query = get_object_or_404(Banner, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('banner_video_view')


# Service Type section
def service_type_add(request):
    form = ServiceTypeForm()
    if request.method=='POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('service_type_view')
        else:
            form = ServiceTypeForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/service_type/service_type_add.html',{'form':form})
    return render(request,'dashboard/service_type/service_type_add.html',{'form':form})

def service_type_view(request):
    query = ServiceType.objects.all().order_by('-id')
    return render(request,'dashboard/service_type/service_type_view.html',{'query':query})

def service_type_edit(request,id):
    query = get_object_or_404(ServiceType, id=id)
    form = ServiceTypeForm(instance =query)
    if request.method=='POST':

        form = ServiceTypeForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('service_type_view')
        else:
            form = ServiceTypeForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/service_type/service_type_edit.html',{'form':form})

    return render(request,'dashboard/service_type/service_type_edit.html',{'form':form})

def service_type_delete(request,id):
    query = get_object_or_404(ServiceType, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('service_type_view')



# CSR section
def csr_add(request):
    form = CsrForm()
    if request.method=='POST':
        form = CsrForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('csr_view')
        else:
            form = CsrForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/csr/csr_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/csr/csr_add.html',{'form':form})

def csr_view(request):
    query = CSR.objects.all().order_by('-id')
    return render(request,'dashboard/get_in_touch/csr/csr_view.html',{'query':query})

def csr_edit(request,id):
    query = get_object_or_404(CSR, id=id)
    form = CsrForm(instance =query)
    if request.method=='POST':

        form = CsrForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('csr_view')
        else:
            form = CsrForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/get_in_touch/csr/csr_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/csr/csr_edit.html',{'form':form})

def csr_delete(request,id):
    query = get_object_or_404(CSR, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('csr_view')


# MissionVision section
def missionvision_add(request):
    form = MissionVisionForm()
    if request.method=='POST':
        form = MissionVisionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('missionvision_view')
        else:
            form = MissionVisionForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/missionvision/missionvision_add.html',{'form':form})
    return render(request,'dashboard/missionvision/missionvision_add.html',{'form':form})

def missionvision_view(request):
    query = MissionVision.objects.all().order_by('-id')
    return render(request,'dashboard/missionvision/missionvision_view.html',{'query':query})

def missionvision_edit(request,id):
    query = get_object_or_404(MissionVision, id=id)
    form = MissionVisionForm(instance =query)
    if request.method=='POST':

        form = MissionVisionForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('missionvision_view')
        else:
            form = MissionVisionForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/missionvision/missionvision_edit.html',{'form':form})

    return render(request,'dashboard/missionvision/missionvision_edit.html',{'form':form})

def missionvision_delete(request,id):
    query = get_object_or_404(MissionVision, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('missionvision_view')

# MD_Message section
def md_message_add(request):
    form = MD_MessageForm()
    if request.method=='POST':
        form = MD_MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('md_message_view')
        else:
            form = MD_MessageForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/md_message/md_message_add.html',{'form':form})
    return render(request,'dashboard/md_message/md_message_add.html',{'form':form})

def md_message_view(request):
    query = MD_Message.objects.all().order_by('-id')
    return render(request,'dashboard/md_message/md_message_view.html',{'query':query})

def md_message_edit(request,id):
    query = get_object_or_404(MD_Message, id=id)
    form = MD_MessageForm(instance =query)
    if request.method=='POST':

        form = MD_MessageForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('md_message_view')
        else:
            form = MD_MessageForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/md_message/md_message_edit.html',{'form':form})

    return render(request,'dashboard/md_message/md_message_edit.html',{'form':form})

def md_message_delete(request,id):
    query = get_object_or_404(MD_Message, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('md_message_view')


#privacy section

def privacy_add(request):
    form = PrivacyForm()
    if request.method=='POST':
        form = PrivacyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('privacy_view')
        else:
            form = PrivacyForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/privacy/privacy_add.html',{'form':form})
    return render(request,'dashboard/privacy/privacy_add.html',{'form':form})

def privacy_view(request):
    query = Privacy.objects.all().order_by('-id')
    return render(request,'dashboard/privacy/privacy_view.html',{'query':query})

def privacy_edit(request,id):
    query = get_object_or_404(Privacy, id=id)
    form = PrivacyForm(instance =query)
    if request.method=='POST':

        form = PrivacyForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('privacy_view')
        else:
            form = PrivacyForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/privacy/privacy_edit.html',{'form':form})

    return render(request,'dashboard/privacy/privacy_edit.html',{'form':form})

def privacy_delete(request,id):
    query = get_object_or_404(Privacy, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('privacy_view')

# Social Responsibility section
def social_responsibility_add(request):
    form = Social_ResponsibilityForm()
    if request.method=='POST':
        form = Social_ResponsibilityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('social_responsibility_view')
        else:
            form = Social_ResponsibilityForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/social_responsibility/social_responsibility_add.html',{'form':form})
    return render(request,'dashboard/social_responsibility/social_responsibility_add.html',{'form':form})

def social_responsibility_view(request):
    query = Social_Responsibility.objects.all().order_by('-id')
    return render(request,'dashboard/social_responsibility/social_responsibility_view.html',{'query':query})

def social_responsibility_edit(request,id):
    query = get_object_or_404(Social_Responsibility, id=id)
    form = Social_ResponsibilityForm(instance =query)
    if request.method=='POST':

        form = Social_ResponsibilityForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('social_responsibility_view')
        else:
            form = Social_ResponsibilityForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/social_responsibility/social_responsibility_edit.html',{'form':form})

    return render(request,'dashboard/social_responsibility/social_responsibility_edit.html',{'form':form})

def social_responsibility_delete(request,id):
    query = get_object_or_404(Social_Responsibility, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('social_responsibility_view')

# Testimonialsection
def testimonial_add(request):
    form = TestimonialForm()
    if request.method=='POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('testimonial_view')
        else:
            form = TestimonialForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/testimonial/testimonial_add.html',{'form':form})
    return render(request,'dashboard/testimonial/testimonial_add.html',{'form':form})

def testimonial_view(request):
    query = Testimonial.objects.all().order_by('-id')
    return render(request,'dashboard/testimonial/testimonial_view.html',{'query':query})

def testimonial_edit(request,id):
    query = get_object_or_404(Testimonial, id=id)
    form = TestimonialForm(instance =query)
    if request.method=='POST':

        form = TestimonialForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('testimonial_view')
        else:
            form = TestimonialForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/testimonial/testimonial_edit.html',{'form':form})

    return render(request,'dashboard/testimonial/testimonial_edit.html',{'form':form})

def testimonial_delete(request,id):
    query = get_object_or_404(Testimonial, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('testimonial_view')

# Awards section
def awards_add(request):
    form = AwardsForm()
    if request.method=='POST':
        form = AwardsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('awards_view')
        else:
            form = AwardsForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/awards/awards_add.html',{'form':form})
    return render(request,'dashboard/awards/awards_add.html',{'form':form})

def awards_view(request):
    query = Awards.objects.all().order_by('-id')
    return render(request,'dashboard/awards/awards_view.html',{'query':query})

def awards_edit(request,id):
    query = get_object_or_404(Awards, id=id)
    form = AwardsForm(instance =query)
    if request.method=='POST':

        form = AwardsForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('awards_view')
        else:
            form = AwardsForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/awards/awards_edit.html',{'form':form})

    return render(request,'dashboard/awards/awards_edit.html',{'form':form})

def awards_delete(request,id):
    query = get_object_or_404(Awards, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('awards_view')

# Land Wanted section
def land_wanted_add(request):
    form = Land_WantedForm()
    if request.method=='POST':
        form = Land_WantedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('land_wanted_view')
        else:
            form = Land_WantedForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/land_wanted/land_wanted_add.html',{'form':form})
    return render(request,'dashboard/land_wanted/land_wanted_add.html',{'form':form})

def land_wanted_view(request):
    query = Land_Wanted.objects.all().order_by('-id')
    return render(request,'dashboard/land_wanted/land_wanted_view.html',{'query':query})

def land_wanted_edit(request,id):
    query = get_object_or_404(Land_Wanted, id=id)
    form = Land_WantedForm(instance =query)
    if request.method=='POST':

        form = Land_WantedForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('land_wanted_view')
        else:
            form = Land_WantedForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/land_wanted/land_wanted_edit.html',{'form':form})

    return render(request,'dashboard/land_wanted/land_wanted_edit.html',{'form':form})

def land_wanted_delete(request,id):
    query = get_object_or_404(Land_Wanted, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('land_wanted_view')

# Corparate Structure section
def corparate_structure_add(request):
    form = Corparate_StructureForm()
    if request.method=='POST':
        form = Corparate_StructureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('corparate_structure_view')
        else:
            form = Corparate_StructureForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/corparate_structure/corparate_structure_add.html',{'form':form})
    return render(request,'dashboard/corparate_structure/corparate_structure_add.html',{'form':form})

def corparate_structure_view(request):
    query = Corparate_Structure.objects.all().order_by('-id')
    return render(request,'dashboard/corparate_structure/corparate_structure_view.html',{'query':query})

def corparate_structure_edit(request,id):
    query = get_object_or_404(Corparate_Structure, id=id)
    form = Corparate_StructureForm(instance =query)
    if request.method=='POST':

        form = Corparate_StructureForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('corparate_structure_view')
        else:
            form = Corparate_StructureForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/corparate_structure/corparate_structure_edit.html',{'form':form})

    return render(request,'dashboard/corparate_structure/corparate_structure_edit.html',{'form':form})

def corparate_structure_delete(request,id):
    query = get_object_or_404(Corparate_Structure, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('corparate_structure_view')

# Our Certificate section
def our_certificate_add(request):
    form = Our_CertificateForm()
    if request.method=='POST':
        form = Our_CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('our_certificate_view')
        else:
            form = Our_CertificateForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/our_certificate/our_certificate_add.html',{'form':form})
    return render(request,'dashboard/our_certificate/our_certificate_add.html',{'form':form})

def our_certificate_view(request):
    query = Our_Certificate.objects.all().order_by('-id')
    return render(request,'dashboard/our_certificate/our_certificate_view.html',{'query':query})

def our_certificate_edit(request,id):
    query = get_object_or_404(Our_Certificate, id=id)
    form = Our_CertificateForm(instance =query)
    if request.method=='POST':

        form = Our_CertificateForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('our_certificate_view')
        else:
            form = Our_CertificateForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/our_certificate/our_certificate_edit.html',{'form':form})

    return render(request,'dashboard/our_certificate/our_certificate_edit.html',{'form':form})

def our_certificate_delete(request,id):
    query = get_object_or_404(Our_Certificate, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('our_certificate_view')

# NewsLetter section
def newsletter_add(request):
    form = NewsLetterForm()
    if request.method=='POST':
        form = NewsLetterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('newsletter_view')
        else:
            form = NewsLetterForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/newsletter/newsletter_add.html',{'form':form})
    return render(request,'dashboard/newsletter/newsletter_add.html',{'form':form})

def newsletter_view(request):
    query = NewsLetter.objects.all().order_by('-id')
    return render(request,'dashboard/newsletter/newsletter_view.html',{'query':query})

def newsletter_edit(request,id):
    query = get_object_or_404(NewsLetter, id=id)
    form = NewsLetterForm(instance =query)
    if request.method=='POST':

        form = NewsLetterForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('newsletter_view')
        else:
            form = NewsLetterForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/newsletter/newsletter_edit.html',{'form':form})

    return render(request,'dashboard/newsletter/newsletter_edit.html',{'form':form})

def newsletter_delete(request,id):
    query = get_object_or_404(NewsLetter, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('newsletter_view')

# Cup of Coffee section
def cup_of_coffee_add(request):
    form = Cup_of_CoffeeForm()
    if request.method=='POST':
        form = Cup_of_CoffeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('cup_of_coffee_view')
        else:
            form = Cup_of_CoffeeForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/cup_of_coffee/cup_of_coffee_add.html',{'form':form})
    return render(request,'dashboard/cup_of_coffee/cup_of_coffee_add.html',{'form':form})

def cup_of_coffee_view(request):
    query = Cup_of_Coffee.objects.all().order_by('-id')
    return render(request,'dashboard/cup_of_coffee/cup_of_coffee_view.html',{'query':query})

def cup_of_coffee_edit(request,id):
    query = get_object_or_404(Cup_of_Coffee, id=id)
    form = Cup_of_CoffeeForm(instance =query)
    if request.method=='POST':

        form = Cup_of_CoffeeForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('cup_of_coffee_view')
        else:
            form = Cup_of_CoffeeForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/cup_of_coffee/cup_of_coffee_edit.html',{'form':form})

    return render(request,'dashboard/cup_of_coffee/cup_of_coffee_edit.html',{'form':form})

def cup_of_coffee_delete(request,id):
    query = get_object_or_404(Cup_of_Coffee, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('cup_of_coffee_view')

# Video Galary section
def video_galary_add(request):
    form = Video_GalaryForm()
    if request.method=='POST':
        form = Video_GalaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('video_galary_view')
        else:
            form = Video_GalaryForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/video_galary/video_galary_add.html',{'form':form})
    return render(request,'dashboard/video_galary/video_galary_add.html',{'form':form})

def video_galary_view(request):
    query = Video_Galary.objects.all().order_by('-id')
    return render(request,'dashboard/video_galary/video_galary_view.html',{'query':query})

def video_galary_edit(request,id):
    query = get_object_or_404(Video_Galary, id=id)
    form = Video_GalaryForm(instance =query)
    if request.method=='POST':

        form = Video_GalaryForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('video_galary_view')
        else:
            form = Video_GalaryForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/video_galary/video_galary_edit.html',{'form':form})

    return render(request,'dashboard/video_galary/video_galary_edit.html',{'form':form})

def video_galary_delete(request,id):
    query = get_object_or_404(Video_Galary, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('video_galary_view')







# Sister Concerns
def sister_concerns_add(request):
    form = SisterConcernForm()
    if request.method=='POST':
        form = SisterConcernForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('sister_concerns_view')
        else:
            form = SisterConcernForm()
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/sister_concerns/sister_concerns_add.html',{'form':form})
    return render(request,'dashboard/sister_concerns/sister_concerns_add.html',{'form':form})

def sister_concerns_view(request):
    query = SisterConcern.objects.all().order_by('-id')
    return render(request,'dashboard/sister_concerns/sister_concerns_view.html',{'query':query})

def sister_concerns_edit(request,id):
    query = get_object_or_404(SisterConcern, id=id)
    form = SisterConcernForm(instance =query)
    if request.method=='POST':

        form = SisterConcernForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('sister_concerns_view')
        else:
            form = SisterConcernForm(instance =query)
            messages.error(request,'Something went Wrong!!', form.errors)
            return render(request, 'dashboard/sister_concerns/sister_concerns_edit.html',{'form':form})

    return render(request,'dashboard/sister_concerns/sister_concerns_edit.html',{'form':form})

def testimonial_delete(request,id):
    query = get_object_or_404(SisterConcern, id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('sister_concerns_view')





# Booking From 
def bookingfrom_view(request):
    query = RealEstateApplication.objects.all()
    return render(request,'dashboard/bookingfrom/bookingfrom_view.html',{'query':query})
    
def bookingfrom_details(request,id):
    query = get_object_or_404(RealEstateApplication, id=id)
    query.read_status = True
    query.save()
    return render(request,'dashboard/bookingfrom/bookingfrom_details.html',{'query':query})
    
def bookingfrom_delete(request,id):
    query = get_object_or_404(RealEstateApplication, id=id)
    query.delete()
    return redirect('bookingfrom_view')

# Booking From 

def realstate_terms_view(request):
    query = RealstateTerms.objects.all().order_by('-id')
    return render(request, 'dashboard/booking_terms/booking_terms_view.html', {'query': query})


def realstate_terms_add(request):
    form = RealstateTermsForm()
    if request.method == 'POST':
        form = RealstateTermsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted")
            return redirect('realstate_terms_view')
        else:
            messages.error(request, "Something went wrong!", form.errors)
    return render(request, 'dashboard/booking_terms/booking_terms_add.html', {'form': form})


def realstate_terms_edit(request, id):
    query = get_object_or_404(RealstateTerms, id=id)
    form = RealstateTermsForm(instance=query)
    if request.method == 'POST':
        form = RealstateTermsForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect('realstate_terms_view')
        else:
            messages.error(request, "Something went wrong!", form.errors)
    return render(request, 'dashboard/booking_terms/terms_edit.html', {'form': form})


def realstate_terms_delete(request, id):
    query = get_object_or_404(RealstateTerms, id=id)
    query.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('realstate_terms_view')


# Booking From Pdf


def document_view(request):
    query = Document.objects.all().order_by('-id')
    return render(request, 'dashboard/bookingfrom_documents/document_view.html', {'query': query})


def document_add(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('document_view')
        else:
            messages.error(request, "Upload failed.", form.errors)
    return render(request, 'dashboard/bookingfrom_documents/document_add.html', {'form': form})


def document_edit(request, id):
    query = get_object_or_404(Document, id=id)
    form = DocumentForm(instance=query)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully.")
            return redirect('document_view')
        else:
            messages.error(request, "Update failed.", form.errors)
    return render(request, 'dashboard/bookingfrom_documents/document_edit.html', {'form': form})


def document_delete(request, id):
    query = get_object_or_404(Document, id=id)
    query.delete()
    messages.success(request, "Document deleted.")
    return redirect('document_view')

