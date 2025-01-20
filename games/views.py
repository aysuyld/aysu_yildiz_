# games/views.py

from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView


def base_view(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    return render(request, 'home/index.html')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileView(TemplateView):
    template_name = "home/profile.html"  # Profil sayfası için HTML şablonunu belirtin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Profil"  # Şablona özel bir değişken ekleme
        # Kullanıcı bilgilerini eklemek için context'e veri ekleyebilirsiniz
        context['user'] = self.request.user
        return context

class GamesHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'games/games_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Oyunların listesini context'e ekleyelim
        context['games'] = [
            {
                'title': 'Python Başlangıç',
                'description': 'Python programlamanın temellerini öğren',
                'level': 'Başlangıç',
                'icon': '🐍',
                'url': 'python_basics'
            },
            {
                'title': 'Algoritma Macerası',
                'description': 'Algoritma ve problem çözme becerilerini geliştir',
                'level': 'Orta',
                'icon': '🎯',
                'url': 'algorithm_adventure'
            },
            {
                'title': 'Kod Bulmacaları',
                'description': 'Eğlenceli bulmacalarla kodlama mantığını öğren',
                'level': 'Başlangıç',
                'icon': '🧩',
                'url': 'code_puzzles'
            },
            {
                'title': 'Mini Projeler',
                'description': 'Kendi oyun ve uygulamalarını geliştir',
                'level': 'İleri',
                'icon': '🎮',
                'url': 'mini_projects'
            }
        ]
        return context

class MazeCodingView(LoginRequiredMixin, TemplateView):
    template_name = 'games/maze_coding.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Oyun seviyeleri
        context['levels'] = [
            {
                'number': 1,
                'title': 'Başlangıç',
                'description': 'Karakteri yıldıza ulaştır!',
                'hint': 'İpucu: move_forward(3) komutu ile 3 adım ileri gidebilirsin.',
                'max_steps': 5,
                'grid': [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 'S', 0, 0, 0, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 'F', 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ],
                'start_direction': 'right'
            },
            {
                'number': 2,
                'title': 'Dönüşler',
                'description': 'Dönüşleri kullanarak hedefe ulaş!',
                'hint': 'İpucu: turn_left() ile sola dönebilirsin.',
                'max_steps': 8,
                'grid': [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 'S', 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 'F', 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ],
                'start_direction': 'right'
            },
            # Daha fazla seviye eklenebilir
        ]

        # Kullanılabilir komutlar
        context['commands'] = {
            'move_forward': {
                'name': 'İleri Git',
                'syntax': 'move_forward(n)',
                'description': 'n adım ileri git',
                'example': 'move_forward(3)'
            },
            'turn_left': {
                'name': 'Sola Dön',
                'syntax': 'turn_left()',
                'description': 'Sola dön',
                'example': 'turn_left()'
            },
            'turn_right': {
                'name': 'Sağa Dön',
                'syntax': 'turn_right()',
                'description': 'Sağa dön',
                'example': 'turn_right()'
            }
        }

        # Kullanıcının seviye ilerlemesi
        if self.request.user.is_authenticated:
            # Burada kullanıcının kaydettiği ilerlemeyi veritabanından çekebilirsiniz
            context['user_progress'] = {
                'current_level': 1,
                'stars': 0,
                'completed_levels': []
            }

        return context

    def post(self, request, *args, **kwargs):
        """
        Kullanıcının kod gönderilerini işlemek için
        (İleride kullanıcının kodunu kaydetmek veya ilerlemeyi güncellemek için kullanılabilir)
        """
        if request.is_ajax():
            code = request.POST.get('code')
            level = request.POST.get('level')
            # Burada kod değerlendirmesi yapılabilir
            # Başarı durumu kaydedilebilir
            return JsonResponse({'success': True})
        return super().post(request, *args, **kwargs)

"""  
class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planets = Planet.objects.all().order_by('order')
        
        if self.request.user.is_authenticated:
            user_points = self.request.user.userprofile.points
            # Her gezegen için kullanıcının erişimi olup olmadığını kontrol et
            for planet in planets:
                planet.is_accessible = user_points >= planet.required_points
        else:
            # Giriş yapmamış kullanıcılar için sadece ilk gezegen erişilebilir
            for i, planet in enumerate(planets):
                planet.is_accessible = i == 0

        context['planets'] = planets
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        context['completed_challenges'] = UserChallenge.objects.filter(
            user=self.request.user.userprofile,
            completed=True
        ).order_by('-completed_date')
        return context

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Kayıt başarılı! Hoş geldiniz!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Kayıt Ol'
        return context
    
class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'  # login.html şablonunun yolu
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True  # Zaten giriş yapmış kullanıcıları yönlendir

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, 'Başarıyla giriş yaptınız!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Kullanıcı adı veya şifre hatalı!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Giriş Yap'
        return context

class PlanetDetailView(LoginRequiredMixin, DetailView):
    model = Planet
    template_name = 'games/planet_detail.html'
    context_object_name = 'planet'
    slug_field = 'code'
    slug_url_kwarg = 'planet_code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = self.object.challenges.all().order_by('position')
        context['user_profile'] = self.request.user.userprofile
        return context

class ChallengeView(LoginRequiredMixin, DetailView):
    model = Challenge
    template_name = 'games/challenge.html'
    context_object_name = 'challenge'
    slug_field = 'code'
    slug_url_kwarg = 'challenge_code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_challenge, created = UserChallenge.objects.get_or_create(
            user=self.request.user.userprofile,
            challenge=self.object
        )
        context['user_challenge'] = user_challenge
        return context

class AchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'games/achievements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        context['achievements'] = UserChallenge.objects.filter(
            user=self.request.user.userprofile
        ).select_related('challenge')
        return context

"""