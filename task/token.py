from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """ Generate a token hash by leveraging PasswordResetTokenGenerator.
        This token is used for account activation """
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
