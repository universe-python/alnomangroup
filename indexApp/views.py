from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, FormView
)


class HomeView(TemplateView):
    template_name = 'tindex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data for the context
        camping_banner = CampingBanner.objects.last()

        banner_query = Banner.objects.all().order_by('-id')
        location_query = Location.objects.all()
        sister_concerns = SisterConcern.objects.all()

        location_filter = self.request.GET.get('location')
        page_number = self.request.GET.get('page', 1)

        if location_filter:
            feature_query = PropertyPost.objects.filter(
                post_location__location_name=location_filter)
        else:
            feature_query = PropertyPost.objects.filter(
                post_type__name='Feature Property')

        # Paginate the feature query
        paginator = Paginator(feature_query, 10)
        page_obj = paginator.get_page(page_number)

        # Fetch other queries
        recent_query = PropertyPost.objects.filter(
            post_type__name='Recent Property')
        choose_the_best = PropertyPost.objects.filter(
            post_type__name='Choose The Best')
        about_testimonial = AboutTestimotial.objects.all()
        why_chosse_us_q = Why_chosse_us.objects.all()
        counters = Counters.objects.all()
        agent_query = Agent.objects.all()
        blog_query = Blog.objects.all()
        faq_query = Faq.objects.all()

        cupofcoffeee = Cup_of_Coffee.objects.all()[:6]
        # Add data to context
        context.update({
            'camping_banner':camping_banner,
            'banner_details': banner_query,
            'feature_details': page_obj,
            'page_number': int(page_number),
            'paginator': paginator,
            'counters_details': counters,
            'location_details': location_query,
            'agent_details': agent_query,
            'recent_property': recent_query,
            'blog_querys': blog_query,
            'why_chosse_us_q': why_chosse_us_q,
            'faq_query': faq_query,
            'about_testimonial': about_testimonial,
            # 'cupofcoffeee':cupofcoffeee,
            'choose_the_best': choose_the_best,
            'sister_concerns': sister_concerns,
        })
        return context


def newsletter(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsLetterForm()
    return render(request, 'tindex.html', {'form': form})


# def landprojectpage(request):
#     project_types = request.GET.getlist('project_types')
#     property_types = request.GET.getlist('property_types')
#     division = request.GET.get('division')
#     district = request.GET.get('district')
#     sub_district = request.GET.get('sub_district')

#     feature_details = PropertyPost.objects.filter(post_type__name='Land Property')

#     if project_types:
#         feature_details = feature_details.filter(project_type_filter__in=project_types)
#     if property_types:
#         feature_details = feature_details.filter(property_type_filter__in=property_types)
#     if division:
#         feature_details = feature_details.filter(division=division)
#     if district:
#         feature_details = feature_details.filter(district=district)
#     if sub_district:
#         feature_details = feature_details.filter(sub_district=sub_district)

#     # Pagination
#     paginator = Paginator(feature_details, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)


#     context = {
#         'projecttype': ProjectTypeFilter.objects.all(),
#         'propertytype': PropertyTypeFilter.objects.all(),
#         'feature_details': page_obj,
#         'form': AreaForm(),
#         'project_types': project_types,
#         'property_types': property_types,
#         'division': division,
#         'district': district,
#         'sub_district': sub_district
#     }

#     return render(request, 'property/tland_project.html', context)


def video_gallery(request):
    query = Video_Galary.objects.all()
    return render(request, 'gallery/tvideo.html', {'query': query})


def landprojectpage(request):
    project_types = request.GET.getlist('project_types')
    property_types = request.GET.getlist('property_types')
    division = request.GET.get('division')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')

    feature_details = PropertyPost.objects.filter(
        post_type__name='Land Property')

    if project_types:
        feature_details = feature_details.filter(
            project_type_filter__in=project_types)
    if property_types:
        feature_details = feature_details.filter(
            property_type_filter__in=property_types)
    if division:
        feature_details = feature_details.filter(division=division)
    if district:
        feature_details = feature_details.filter(district=district)
    if sub_district:
        feature_details = feature_details.filter(sub_district=sub_district)

    # Pagination
    paginator = Paginator(feature_details, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'property/property_grid.html', {'feature_details': page_obj})
        return JsonResponse({'html': html})

    context = {
        'projecttype': ProjectTypeFilter.objects.all(),
        'propertytype': PropertyTypeFilter.objects.all(),
        'feature_details': page_obj,
        'form': AreaForm(),
        'project_types': project_types,
        'property_types': property_types,
        'division': division,
        'district': district,
        'sub_district': sub_district
    }

    return render(request, 'property/tland_project.html', context)


def apartmentprojectpage(request):
    project_types = request.GET.getlist('project_types')
    property_types = request.GET.getlist('property_types')
    division = request.GET.get('division')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')

    feature_details = PropertyPost.objects.filter(
        post_type__name="Apartment Property")

    if project_types:
        feature_details = feature_details.filter(
            project_type_filter__in=project_types)
    if property_types:
        feature_details = feature_details.filter(
            property_type_filter__in=property_types)
    if division:
        feature_details = feature_details.filter(division=division)
    if district:
        feature_details = feature_details.filter(district=district)
    if sub_district:
        feature_details = feature_details.filter(sub_district=sub_district)

    # Pagination
    paginator = Paginator(feature_details, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'property/property_grid.html', {'feature_details': page_obj})
        return JsonResponse({'html': html})

    context = {
        'projecttype': ProjectTypeFilter.objects.all(),
        'propertytype': PropertyTypeFilter.objects.all(),

        'feature_details': page_obj,
        'form': AreaForm(),
        'project_types': project_types,
        'property_types': property_types,
        'division': division,
        'district': district,
        'sub_district': sub_district

    }

    return render(request, 'property/tapartment_project.html', context)


class LandProjectView(ListView):
    model = PropertyPost
    template_name = 'property/land_project.html'
    context_object_name = 'feature_details'
    paginate_by = 9
    paginate_orphans = 1

    def get_queryset(self):
        return PropertyPost.objects.filter(post_type__name='Land Property')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projecttype': ProjectTypeFilter.objects.all(),
            'propertytype': PropertyTypeFilter.objects.all(),
            'form': AreaForm(),
            'page_number': int(self.request.GET.get('page', 1)),
        })
        return context


# class LandDetailsPropertyView(DetailView):
#     model = PropertyPost
#     template_name = 'property_details/tland_details_property.html'
#     context_object_name = 'land_details'
#     # pk_url_kwarg = 'id'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         single_post = self.object
#         context.update({
#             'related_images': Post_related_images.objects.filter(post=single_post),
#             'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
#             'form': UserFeedbackForm(),
#         })
#         return context


class LandDetailsPropertyView(DetailView):
    model = PropertyPost
    template_name = 'property_details/tland_details_property.html'
    context_object_name = 'land_details'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_post = self.object

        feature = single_post.feature or ""
        feature_list = [item.strip() for item in feature.replace("➔", "\n").split("\n") if item.strip()]

        context.update({
            'related_images': Post_related_images.objects.filter(post=single_post),
            'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
            'form': UserFeedbackForm(),
            'feature_list': feature_list,  
        })
        return context



    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.instance.property_id = self.object.id
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('land_details_property', slug=self.object.slug)
        else:
            messages.error(request, 'Message Not Submitted')
            return redirect('land_details_property', slug=self.object.slug)


class ApartmentProject(ListView):
    model = PropertyPost
    template_name = "property/tapartment_project.html"
    context_object_name = "feature_details"
    paginate_by = 9
    paginate_orphans = 1

    def get_queryset(self):
        return PropertyPost.objects.filter(post_type__name="Apartment Property")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projecttype': ProjectTypeFilter.objects.all(),
            'propertytype': PropertyTypeFilter.objects.all(),
            'form': AreaForm(),
            'page_number': int(self.request.GET.get('page', 1))
        })
        return context


class ApartmentPropertyDetailView(DetailView):
    model = PropertyPost
    template_name = 'property_details/tapartment_details.html'
    context_object_name = 'apartment_details'
    # pk_url_kwarg = 'id'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_post = self.object
        context.update({
            'related_images': Post_related_images.objects.filter(post=single_post),
            'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
            'form': UserFeedbackForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.instance.property_id = self.object.id
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('details_property', slug=self.object.slug)
        else:
            messages.error(request, 'Message Not Submitted')
            return redirect('details_property', slug=self.object.slug)



class FeaturePropertyDetailView(DetailView):
    model = PropertyPost
    template_name = 'property_details/tfeature_details_property.html'
    context_object_name = 'feature_property_details'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_post = self.object
        context.update({
            'related_images': Post_related_images.objects.filter(post=single_post),
            'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
            'form': UserFeedbackForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.instance.property_id = self.object.id
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('feature_details_property', id=self.object.id)
        else:
            messages.error(request, 'Message Not Submitted')
            return redirect('feature_details_property', id=self.object.id)


class RecentPropertyDetailView(DetailView):
    model = PropertyPost
    template_name = 'property_details/trecent_details_property.html'
    context_object_name = 'recent_property_details'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_post = self.object
        context.update({
            'related_images': Post_related_images.objects.filter(post=single_post),
            'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
            'form': UserFeedbackForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.instance.property_id = self.object.id
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('recent_details_property', id=self.object.id)
        else:
            messages.error(request, 'Message Not Submitted')
            return redirect('recent_details_property', id=self.object.id)


class ChooseTheBestDetailView(DetailView):
    model = PropertyPost
    template_name = 'property_details/tchoose_details_property.html'
    context_object_name = 'choose_property_details'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_post = self.object
        context.update({
            'related_images': Post_related_images.objects.filter(post=single_post),
            'feedback_reply': FeedBack.objects.filter(is_feedback_show=True, property_id=single_post.id),
            'form': UserFeedbackForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.instance.property_id = self.object.id
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('choose_details_property', id=self.object.id)
        else:
            messages.error(request, 'Message Not Submitted')
            return redirect('choose_details_property', id=self.object.id)


class ServiceDetailView(DetailView):
    model = ServicePost
    template_name = 'service/service_details.html'
    context_object_name = 'service_detail_q'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_images'] = Service_related_images.objects.filter(
            service=self.object)
        return context


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/tblog.html'
    context_object_name = 'blog_query'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/tread_more.html'
    context_object_name = 'single_blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_blog = self.get_object()
        context['related_blogs'] = Blog.objects.exclude(
            slug=current_blog.slug)[:6]
        return context


class AboutView(TemplateView):
    template_name = 'about/tabout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'about_query': AboutUs.objects.all(),
            'LookingSections': AboutLookingSection.objects.all(),
            'about_testimotial': AboutTestimotial.objects.all(),
        })
        return context


# class AlbumView(ListView):
#     model = Album
#     template_name = 'gallery/tablum.html'
#     context_object_name = 'gallery_office'
# class GalleryView(ListView):
#     model = Gallery
#     template_name = 'gallery/toffice.html'
#     context_object_name = 'gallery_office'

#     def get_queryset(self):
#         album_id = self.kwargs.get('album_id')
#         return Gallery.objects.filter(album_id=album_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         album_id = self.kwargs.get('album_id')
#         context['album'] = Album.objects.get(id=album_id)
#         return context
def album(request):
    query = Album.objects.all()
    return render(request, 'gallery/tablum.html', {'albums': query})


def gallery(request, pk):
    print(pk)
    query = Gallery.objects.filter(album__id=pk)
    return render(request, 'gallery/toffice.html', {'query': query})


class VideoView(TemplateView):
    template_name = 'gallery/video.html'


class ContactView(FormView):
    template_name = 'get_in_touch/tcontact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contactus')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully Submitted')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form submission failed')
        return self.render_to_response(self.get_context_data(form=form))


class OurTeamView(ListView):
    model = OurTeam
    template_name = 'get_in_touch/tour_team.html'
    context_object_name = 'team_profile'


class CareerView(ListView):
    model = Career
    template_name = 'get_in_touch/tcareer.html'
    context_object_name = 'career'


class CareerDetailView(DetailView, FormView):
    model = Career
    template_name = 'get_in_touch/tcareer-details.html'
    context_object_name = 'careers'
    form_class = JobApplicationForm
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully Submitted')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form submission failed')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('career-detail', kwargs={'slug': self.object.slug, 'id': self.object.id})


class CSRView(ListView):
    model = CSR
    template_name = 'get_in_touch/tcsr.html'
    context_object_name = 'csr'


class CSRDetailView(DetailView):
    model = CSR
    template_name = 'get_in_touch/tcsr_details.html'
    context_object_name = 'csr_details'
    pk_url_kwarg = 'id'


class NoticeView(ListView):
    model = Notice
    template_name = 'get_in_touch/tnotice.html'
    context_object_name = 'notice'


class LocationView(TemplateView):
    template_name = 'location_wise_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_name = self.kwargs.get('location_name')
        if location_name:
            context['feature_details'] = PropertyPost.objects.filter(
                post_location__location_name=location_name)
        return context


class BookingNowView(FormView):
    template_name = 'booking_now.html'
    form_class = BookingNowForm
    success_url = reverse_lazy('booking_now')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully Submitted')
        return super().form_valid(form)


class FilterLandProjectView(View):
    def get(self, request, *args, **kwargs):
        project_type = request.GET.getlist('project_type[]')
        property_type = request.GET.getlist('property_type[]')
        division = request.GET.getlist('division')
        district = request.GET.getlist('district')
        sub_district = request.GET.getlist('sub_district')

        all_land_projects = PropertyPost.objects.filter(
            post_type__name='Land Property').order_by('-id')

        if project_type:
            all_land_projects = all_land_projects.filter(
                project_type_filter__id__in=project_type).distinct()

        if property_type:
            all_land_projects = all_land_projects.filter(
                property_type_filter__id__in=property_type).distinct()

        if division:
            all_land_projects = all_land_projects.filter(
                division__id__in=division).distinct()

        if district:
            all_land_projects = all_land_projects.filter(
                district__id__in=district).distinct()

        if sub_district:
            all_land_projects = all_land_projects.filter(
                sub_district__id__in=sub_district).distinct()

        rendered_template = render_to_string(
            'ajax/land_project_filter.html', {'project': all_land_projects})
        return JsonResponse({'data': rendered_template})


class FilterApartmentProjectView(View):
    def get(self, request, *args, **kwargs):
        project_type = request.GET.getlist('project_type[]')
        property_type = request.GET.getlist('property_type[]')
        division = request.GET.getlist('division')
        district = request.GET.getlist('district')
        sub_district = request.GET.getlist('sub_district')

        apartment_projects = PropertyPost.objects.filter(
            post_type__name='Apartment Property').order_by('-id')

        if project_type:
            apartment_projects = apartment_projects.filter(
                project_type_filter__id__in=project_type).distinct()

        if property_type:
            apartment_projects = apartment_projects.filter(
                property_type_filter__id__in=property_type).distinct()

        if division:
            apartment_projects = apartment_projects.filter(
                division__id__in=division).distinct()

        if district:
            apartment_projects = apartment_projects.filter(
                district__id__in=district).distinct()

        if sub_district:
            apartment_projects = apartment_projects.filter(
                sub_district__id__in=sub_district).distinct()

        rendered_template = render_to_string(
            'ajax/apartment_project_filter.html', {'project': apartment_projects})
        return JsonResponse({'data': rendered_template})


class LoadDistrictsView(TemplateView):
    template_name = 'ajax/district_dropdown_list_options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        division_id = self.request.GET.get('division')
        context['districts'] = District.objects.filter(
            division_id=division_id).order_by('name')
        return context


class LoadSubDistrictsView(TemplateView):
    template_name = 'ajax/subdistrict_dropdown_list_options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        district_id = self.request.GET.get('district')
        context['subdistricts'] = SubDistrict.objects.filter(
            district_id=district_id).order_by('name')
        return context


def awards(request):
    query = Awards.objects.all()
    return render(request, 'tawards.html', {'query': query})


def awards_details(request, pk):
    query = get_object_or_404(Awards, id=pk)
    return render(request, 'tawards-details.html', {'query': query})


def our_certificate(request):
    query = Our_Certificate.objects.all()
    print(query)
    return render(request, 'tour_certificate.html', {'query': query})


def our_certificate_details(request, pk):
    query = get_object_or_404(Our_Certificate, id=pk)
    return render(request, 'tour_certificate-details.html', {'query': query})


def testimonial(request):
    query = Testimonial.objects.all()
    return render(request, 'ttestimonial.html', {'query': query})


def mission_vission(request):
    query = MissionVision.objects.last()
    return render(request, 'tmission&vision.html', {'query': query})


def md_message(request):
    query = MD_Message.objects.last()
    return render(request, 'tmdmessage.html', {'query': query})


def corparate_structure(request):
    query = Corparate_Structure.objects.last()
    return render(request, 'tcorparate_structure.html', {'query': query})


def social_responsibility(request):
    query = Social_Responsibility.objects.last()
    return render(request, 'tsocial_responsibility.html', {'query': query})


def land_wanted(request):
    query = Land_Wanted.objects.last()
    return render(request, 'tland_wanted.html', {'query': query})


def sister_concerns(request):
    sister_concerns = SisterConcern.objects.all()
    sister_concern_banner = SisterConcernBanner.objects.last() 
    return render(request, 'tsister_concerns.html', {
        'sister_concerns': sister_concerns,
        'sister_concern_banner': sister_concern_banner
    })



def sister_concerns_details(request, slug):
    concern = get_object_or_404(SisterConcern, slug=slug)
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect(reverse_lazy('sister_concerns_details'))
        else:
            messages.error(request, 'Form submission failed')

    return render(request, 'tsister_concerns_details.html', {
        'concern': concern,
        'form': form,
    })


def realestate_apply(request):
    if request.method == 'POST':
        form = RealEstateApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('realestate_apply')
    else:
        form = RealEstateApplicationForm()

    sections = [
        ("Personal Information", [
            form['applicant_full_name'], form['mother_name'], form['date_of_birth'],
            form['nationality'], form['religion'],
            form['email'], form['permanent_address'],
        ]),
        ("Professional Information", [
            form['profession'], form['designation'], form['organization']
        ]),
        ("Project Information", [
            form['residence_type'], form['project_location'], form['total_price'],
            form['per_share_price'], form['total_project_area'], form['number_of_share'],
            form['instruction']
        ]),
    ]

    terms = RealstateTerms.objects.last()
    documents = Document.objects.all()
    return render(request, 'booking_form.html', {
        'form': form,
        'sections': sections,
        'terms': terms,
        'documents': documents,
    })


def privacy_policy(request):
    return render(request, 'tprivacy_policy.html', {"query": Privacy.objects.last()})
