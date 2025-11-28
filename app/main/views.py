from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = "Цветы с любовью"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = "О нас"
        context['text_on_page'] = [
            {
                'text': 'В названии нашего магазина есть слово «Amore», означающее «любовь» на итальянском языке. Это слово прекрасно передает нашу главную миссию: дарить радость, нежность и тепло через каждую цветочную композицию. В «Amore. Цветы со любовью» мы создаём не просто букеты, а символы чувств, которые делают особенными любые моменты жизни.'
            },
            {
                'text': 'Наш магазин — это место, где каждая цветочная идея наполнена любовью и заботой, ведь именно так мы выражаем свои самые искренние эмоции.'
            }
        ]
        context['additional_benefits'] = [
            "Почему выбирают нас:",
            "- Возможность заказать букет на любой бюджет",
            "- Только свежие цветы высокого качества",
            "- Быстрая доставка и выгодные цены",
            "- Индивидуальный подход к каждому заказу",
        ]
        return context


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Контакты'
        context['content'] = "Контакты"
        context['additional_benefits'] = [
            "Адрес: Улица Умурская, 82, цокольный этаж",
        ]
        return context