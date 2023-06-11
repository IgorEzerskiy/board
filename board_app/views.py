from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from board_app.forms import UserLoginForm, UserCreateForm, CardCreateForm
from board_app.models import Card, Category
from django.contrib import messages

from django import forms

# Create your views here.


class CardsListView(LoginRequiredMixin, ListView):
    template_name = 'board.html'
    extra_context = {'category': Category.objects.all(),
                     'users': User.objects.all(),
                     'card_create_form': CardCreateForm()}
    queryset = Card.objects.all()
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.extra_context is not None:
            if not self.request.user.is_staff:
                card_for_user = CardCreateForm()
                user = User.objects.filter(username=self.request.user.username)
                card_for_user.fields['assignee'] = forms.ModelChoiceField(queryset=user)
                card_for_user.fields['assignee'].widget.attrs.update({'class': 'form-control'})
                context['card_create_form'] = card_for_user
        return context


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'


class CardCreateView(CreateView):
    model = Card
    form_class = CardCreateForm
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.reporter = self.request.user
        messages.success(self.request,
                         'Card was create successfully')
        return super().form_valid(form=form)


class CardUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        try:
            card = Card.objects.filter(id=self.request.POST.get('card_id'))
            update_data = {}

            if self.request.POST.get('card_title'):
                if len(self.request.POST.get('card_title')) > 100:
                    messages.error(self.request, 'Title must be less than 100 characters.')
                    raise ValidationError(message='Title must be less than 100 characters.')
                else:
                    update_data['title'] = self.request.POST.get('card_title')

            if self.request.POST.get('card_text'):
                if len(self.request.POST.get('card_text')) > 400:
                    messages.error(self.request, 'Text must be less than 400 characters.')
                    raise ValidationError(message='Text must be less than 400 characters.')
                else:
                    update_data['text'] = self.request.POST.get('card_text')

            if self.request.POST.get('category'):
                try:
                    category = Category.objects.get(id=self.request.POST.get('category'))
                    if (self.request.user.is_staff or self.request.user.is_superuser) \
                            and category.name in ('New', 'In progress', 'In QA'):
                        messages.error(self.request,
                                       'Staff can not move card to status: New, In progress, In QA.')
                        raise ValidationError(
                            message='Staff can not move card to status: New, In progress, In QA.'
                        )

                    if (not self.request.user.is_staff or not self.request.user.is_superuser) \
                            and category.name == 'Done':
                        messages.error(self.request,
                                       'User can not move card to status: Done.')
                        raise ValidationError(
                            message='User can not move card to status: Done.'
                        )

                    if card.first().category.name == 'New' and category.name not in ('New', 'In progress'):
                        messages.error(self.request,
                                       f'You can not move card to status: {category.name}.')
                        raise ValidationError(
                            message=f'You can not move card to status: {category.name}.'
                        )

                    if card.first().category.name == 'In progress' and \
                            category.name not in ('New', 'In progress', 'In QA'):
                        messages.error(self.request,
                                       f'You can not move card to status: {category.name}.')
                        raise ValidationError(
                            message=f'You can not move card to status: {category.name}.'
                        )

                    if card.first().category.name == 'In QA' and category.name not in ('In progress', 'In QA', 'Ready'):
                        messages.error(self.request,
                                       f'You can not move card to status: {category.name}.')
                        raise ValidationError(
                            message=f'You can not move card to status: {category.name}.'
                        )

                    if card.first().category.name == 'Ready' and category.name not in ('In QA', 'Ready')\
                            and (not self.request.user.is_superuser or not self.request.user.is_staff):
                        messages.error(self.request,
                                       f'You can not move card to status: {category.name}.')
                        raise ValidationError(
                            message=f'You can not move card to status: {category.name}.'
                        )

                    update_data['category'] = self.request.POST.get('category')
                except Category.DoesNotExist:
                    messages.error(self.request,
                                   f'Category does not exist.')

            try:
                user = User.objects.get(id=self.request.POST.get('assignee'))
                update_data['assignee'] = user.id
            except User.DoesNotExist:
                pass

            card.update(**update_data)
        except Card.DoesNotExist:
            messages.error(self.request,
                           f'Card does not exist.')

        messages.success(self.request,
                         'Card was update successfully')
        return HttpResponseRedirect(self.success_url)


class CardDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            card = Card.objects.get(id=self.request.POST.get('del_card_id'))
            card.delete()
            messages.success(self.request,
                             'Card was delete successfully')
        except Card.DoesNotExist:
            messages.error(self.request,
                           f'Card does not exist.')
        return HttpResponseRedirect(self.success_url)
