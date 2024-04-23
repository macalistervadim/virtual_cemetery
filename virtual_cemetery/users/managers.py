import django.contrib.auth.models
import django.db


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
    }

    DOTS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        user_related = django.contrib.auth.models.User.profile.related.name
        return (
            super()
            .get_queryset()
            .select_related(
                user_related,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        normilized_email = self.normalize_email(mail)
        return self.get(email=normilized_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()

        return email
