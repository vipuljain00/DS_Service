import re

class MessageUtil:

    def isBankSms(self, message):
        # Match word stems to catch variations like 'debit', 'debited', 'debiting'
        words_to_check = ['bank', 'debit', 'credit', 'transaction', 'expense', 'income', 'a/c', 'bal', 'upi', 'inr', 'neft', 'imps', 'transfer']
        pattern = re.compile(r'\b(' + '|'.join(words_to_check) + r')', re.IGNORECASE)
        return pattern.search(message)