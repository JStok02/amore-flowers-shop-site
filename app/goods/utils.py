from django.db.models import Q
from django.http import Http404
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from goods.models import Products


def q_search(query):
    if not query.strip():
        raise Http404("По вашему запросу ничего не найдено.")


    if query.isdigit() and len(query) <= 5:
        # return Products.objects.filter(id=int(query))
        # Выполняем поиск по ID товара
        result = Products.objects.filter(id=int(query))

        # Если товары с таким ID не найдены, выбрасываем Http404
        if not result.exists():
            raise Http404("Товары с таким ID не найдены.")

        return result

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    if not result.exists():
        raise Http404("Нет товаров, соответствующих запросу.")

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result