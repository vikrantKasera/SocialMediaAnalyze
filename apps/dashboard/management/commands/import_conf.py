"""Import legacy conf.py settings into the Django database."""

from importlib import import_module

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Import search, relevance, country, and posting criteria settings from conf.py."

    @transaction.atomic
    def handle(self, *args, **options):
        config = import_module("conf")

        from apps.countries.models import Country
        from apps.posting_criteria.models import PostingCriteria
        from apps.relevance_keywords.models import RelevanceKeyword
        from apps.search_keywords.models import SearchKeyword

        search_keywords = self._unique(getattr(config, "SEARCH_KEYWORDS", []))
        relevance_keywords = self._unique(getattr(config, "RELEVANCE_KEYWORDS", []))
        excluded_codes = {code.upper() for code in getattr(config, "EXCLUDED_COUNTRIES", set())}

        self._sync_keywords(SearchKeyword, search_keywords)
        self._sync_keywords(RelevanceKeyword, relevance_keywords)
        Country.objects.exclude(code__in=excluded_codes).update(is_active=False)

        country_count = 0
        for code in excluded_codes:
            country, created = Country.objects.get_or_create(
                code=code,
                defaults={"name": code, "is_active": True},
            )
            if not created and not country.is_active:
                country.is_active = True
                country.save(update_fields=["is_active"])
            country_count += 1

        criteria = PostingCriteria.objects.order_by("-updated_at").first()
        if criteria is None:
            criteria = PostingCriteria()
        criteria.min_views = getattr(config, "MIN_VIEWS", criteria.min_views or 0)
        criteria.max_days_since_posting = getattr(config, "RECENCY_DAYS", criteria.max_days_since_posting or 30)
        criteria.result_per_keyword = getattr(config, "RESULTS_PER_KEYWORD", criteria.result_per_keyword or 10)
        criteria.per_page_keyword = getattr(config, "PAGES_PER_KEYWORD", criteria.per_page_keyword or 1)
        criteria.video_to_check = getattr(config, "VIDEOS_TO_CHECK", criteria.video_to_check or 4)
        criteria.recent_days = getattr(config, "RECENCY_DAYS", criteria.recent_days or 100)
        criteria.shorts_max_second = getattr(config, "SHORTS_MAX_SECONDS", criteria.shorts_max_second or 180)
        criteria.is_active = True
        criteria.save()

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(search_keywords)} search keywords, "
            f"{len(relevance_keywords)} relevance keywords, {country_count} excluded countries, "
            f"and posting criteria."
        ))

    @staticmethod
    def _unique(values):
        result = []
        seen = set()
        for value in values:
            normalized = str(value).strip()
            if normalized and normalized.lower() not in seen:
                seen.add(normalized.lower())
                result.append(normalized)
        return result

    def _sync_keywords(self, model, values):
        model.objects.exclude(keyword__in=values).update(is_active=False)
        for value in values:
            item, created = model.objects.get_or_create(keyword=value)
            if created or not item.is_active:
                item.is_active = True
                item.save(update_fields=["is_active"])