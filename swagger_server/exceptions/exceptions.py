from connexion import ProblemException


class NotSupportedLanguageProblem(ProblemException):
    def __init__(self, status, title=None, **kwargs):
        super(NotSupportedLanguageProblem, self).__init__(status=status, title=title, **kwargs)

class LanguageNotSupportedException(Exception):
    def __init__(self, lang):
        self.lang = lang

    def __str__(self):
        return "Language {} not supported".format(self.lang)
